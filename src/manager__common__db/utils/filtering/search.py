# type: ignore
# noqa
"""DB filtering + sorting util from Flask-Restless."""
import inspect
from api_utils.errors.api_simple_validate_error import ApiSimpleValidateError

from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy.ext.associationproxy import AssociationProxy
from sqlalchemy.orm import aliased, Query
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql import false as FALSE                       # noqa: N812

from src.manager__common__db.utils.filtering.helpers import get_model
from src.manager__common__db.utils.filtering.helpers import get_related_model
from src.manager__common__db.utils.filtering.helpers import get_related_association_proxy_model
from src.manager__common__db.utils.filtering.helpers import primary_key_names
from src.manager__common__db.utils.filtering.helpers import primary_key_value
from src.manager__common__db.utils.filtering.helpers import session_query
from src.manager__common__db.utils.filtering.helpers import string_to_datetime


class ComparisonToNull(Exception):
    """Raised when a client attempts to use a filter object that compares a
    resource's attribute to ``NULL`` using the ``==`` operator instead of using
    ``is_null``.

    """
    pass


class UnknownField(Exception):
    """Raised when the user attempts to reference a field that does not
    exist on a model in a search.

    """

    def __init__(self, field):

        #: The name of the unknown attribute.
        self.field = field


def _sub_operator(model, argument, fieldname):
    """Recursively calls :func:`create_operation` when argument is a dictionary
    of the form specified in :ref:`search`.

    This function is for use with the ``has`` and ``any`` search operations.

    """
    if isinstance(model, InstrumentedAttribute):
        submodel = model.property.mapper.class_
    elif isinstance(model, AssociationProxy):
        submodel = get_related_association_proxy_model(model)
    else:
        # TODO what do I here?
        pass
    fieldname = argument['name']
    operator = argument['op']
    argument = argument.get('val')
    return create_operation(submodel, fieldname, operator, argument)


OPERATORS = {
    # Operators which accept a single argument.
    'is_null': lambda f: f == None,         # noqa: E711
    'is_not_null': lambda f: f != None,     # noqa: E711
    # 'desc': lambda f: f.desc,
    # 'asc': lambda f: f.asc,
    # Operators which accept two arguments.
    '==': lambda f, a: f == a,
    'eq': lambda f, a: f == a,
    'equals': lambda f, a: f == a,
    'equal_to': lambda f, a: f == a,
    '!=': lambda f, a: f != a,
    'ne': lambda f, a: f != a,
    'neq': lambda f, a: f != a,
    'not_equal_to': lambda f, a: f != a,
    'does_not_equal': lambda f, a: f != a,
    '>': lambda f, a: f > a,
    'gt': lambda f, a: f > a,
    '<': lambda f, a: f < a,
    'lt': lambda f, a: f < a,
    '>=': lambda f, a: f >= a,
    'ge': lambda f, a: f >= a,
    'gte': lambda f, a: f >= a,
    'geq': lambda f, a: f >= a,
    '<=': lambda f, a: f <= a,
    'le': lambda f, a: f <= a,
    'lte': lambda f, a: f <= a,
    'leq': lambda f, a: f <= a,
    '<<': lambda f, a: f.op('<<')(a),
    '<<=': lambda f, a: f.op('<<=')(a),
    '>>': lambda f, a: f.op('>>')(a),
    '>>=': lambda f, a: f.op('>>=')(a),
    '<>': lambda f, a: f.op('<>')(a),
    '&&': lambda f, a: f.op('&&')(a),
    'ilike': lambda f, a: f.ilike(a),
    'like': lambda f, a: f.like(a),
    'not_like': lambda f, a: ~f.like(a),
    'in': lambda f, a: f.in_(a),
    'not_in': lambda f, a: ~f.in_(a),
    # Operators which accept three arguments.
    'has': lambda f, a, fn: f.has(_sub_operator(f, a, fn)),
    'any': lambda f, a, fn: f.any(_sub_operator(f, a, fn)),
}


class Filter(object):

    def __init__(self, fieldname, operator, argument=None, otherfield=None):
        self.fieldname = fieldname
        self.operator = operator
        self.argument = argument
        self.otherfield = otherfield

    @staticmethod
    def from_dictionary(model, dictionary):
        # If there are no ANDs or ORs, we are in the base case of the
        # recursion.
        if 'or' not in dictionary and 'and' not in dictionary:
            fieldname = dictionary.get('name')
            if not hasattr(model, fieldname):
                raise UnknownField(fieldname)
            operator = dictionary.get('op')
            otherfield = dictionary.get('field')
            argument = dictionary.get('val')
            # Need to deal with the special case of converting dates.
            argument = string_to_datetime(model, fieldname, argument)
            return Filter(fieldname, operator, argument, otherfield)
        # For the sake of brevity, rename this method.
        from_dict = Filter.from_dictionary
        # If there is an OR or an AND in the dictionary, recurse on the
        # provided list of filters.
        if 'or' in dictionary:
            subfilters = dictionary.get('or')
            return DisjunctionFilter(*[from_dict(model, filter_)
                                       for filter_ in subfilters])
        else:
            subfilters = dictionary.get('and')
            return ConjunctionFilter(*[from_dict(model, filter_)
                                       for filter_ in subfilters])


class JunctionFilter(Filter):
    """A conjunction or disjunction of other filters.

    `subfilters` is a tuple of :class:`Filter` objects.

    """

    def __init__(self, *subfilters):
        self.subfilters = subfilters

    def __iter__(self):
        return iter(self.subfilters)


class ConjunctionFilter(JunctionFilter):
    """A conjunction of other filters."""

    # # This is useful for debugging purposes.
    # def __repr__(self):
    #     return 'and_{0}'.format(tuple(repr(f) for f in self))


class DisjunctionFilter(JunctionFilter):
    """A disjunction of other filters."""

    # # This is useful for debugging purposes.
    # def __repr__(self):
    #     return 'or_{0}'.format(tuple(repr(f) for f in self))


def create_operation(model, fieldname, operator, argument):
    # raises KeyError if operator not in OPERATORS
    opfunc = OPERATORS[operator]
    # In Python 3.0 or later, this should be `inspect.getfullargspec`
    # because `inspect.getargspec` is deprecated.
    numargs = len(inspect.getargspec(opfunc).args)
    # raises AttributeError if `fieldname` does not exist
    field = getattr(model, fieldname)
    # each of these will raise a TypeError if the wrong number of argments
    # is supplied to `opfunc`.
    if numargs == 1:
        return opfunc(field)
    if argument is None:
        msg = ('To compare a value to NULL, use the is_null/is_not_null '
               'operators.')
        raise ComparisonToNull(msg)
    if numargs == 2:
        return opfunc(field, argument)
    return opfunc(field, argument, fieldname)


def create_filter(model, filt):
    # If the filter is not a conjunction or a disjunction, simply proceed
    # as normal.
    if not isinstance(filt, JunctionFilter):
        fname = filt.fieldname
        val = filt.argument
        # get the other field to which to compare, if it exists
        if filt.otherfield:
            val = getattr(model, filt.otherfield)
        # for the sake of brevity...
        return create_operation(model, fname, filt.operator, val)
    # Otherwise, if this filter is a conjunction or a disjunction, make
    # sure to apply the appropriate filter operation.
    if isinstance(filt, ConjunctionFilter):
        return and_(create_filter(model, f) for f in filt)
    return or_(create_filter(model, f) for f in filt)


def search_relationship(session, instance, relation, filters=None, sort=None,
                        group_by=None):
    model = get_model(instance)
    related_model = get_related_model(model, relation)
    query = session_query(session, related_model)

    # Filter by only those related values that are related to `instance`.
    relationship = getattr(instance, relation)
    # TODO In Python 2.7+, this should be a set comprehension.
    primary_keys = set(primary_key_value(inst) for inst in relationship)
    # If the relationship is empty, we can avoid a potentially expensive
    # filtering operation by simply returning an intentionally empty
    # query.
    if not primary_keys:
        return query.filter(FALSE())
    query = query.filter(primary_key_value(related_model).in_(primary_keys))

    return db_search(
        session,
        related_model,
        filters=filters,
        sort=sort,
        group_by=group_by,
        _initial_query=query
    )


def db_search(session, model, filters=None, sort=None, group_by=None, _initial_query=None) -> Query:
    if _initial_query is not None:
        query = _initial_query
    else:
        query = session_query(session, model)

    # Filter the query.
    try:
        filters = [Filter.from_dictionary(model, f) for f in filters]
        # This function call may raise an exception.
        filters = [create_filter(model, f) for f in filters]
    except UnknownField as e:
        raise ApiSimpleValidateError(
            f"{model.__name__} has no '{e}' attribute to filter by it"
        )

    query = query.filter(*filters)

    # Order the query. If no order field is specified, order by primary
    # key.
    # if not _ignore_sort:
    if sort:
        for (symbol, field_name) in sort:
            direction_name = 'asc' if symbol == '+' else 'desc'
            if '.' in field_name:
                field_name, field_name_in_relation = field_name.split('.')
                relation_model = aliased(get_related_model(model, field_name))
                try:
                    field = getattr(relation_model, field_name_in_relation)
                except AttributeError:
                    raise ApiSimpleValidateError(
                        f"{relation_model.__name__} have not '{field_name_in_relation}' attribute to sort by it"
                    )
                direction = getattr(field, direction_name)
                query = query.join(relation_model)
                query = query.order_by(direction())
            else:
                try:
                    field = getattr(model, field_name)
                except AttributeError:
                    raise ApiSimpleValidateError(
                        f"{model.__name__} have not '{field_name}' attribute to sort by it"
                    )
                direction = getattr(field, direction_name)
                query = query.order_by(direction())
    else:
        pks = primary_key_names(model)
        pk_order = (getattr(model, field).asc() for field in pks)
        query = query.order_by(*pk_order)

    # Group the query.
    if group_by:
        for field_name in group_by:
            if '.' in field_name:
                field_name, field_name_in_relation = field_name.split('.')
                relation_model = get_related_model(model, field_name)
                field = getattr(relation_model, field_name_in_relation)
                query = query.join(relation_model)
                query = query.group_by(field)
            else:
                field = getattr(model, field_name)
                query = query.group_by(field)

    return query
