import bcrypt
from sqlalchemy import types


class BHashedBinary(types.TypeDecorator):    # type:ignore
    '''
    Database field type which stores
    bcrypt hash of any string in LargeBinary

    comments "type:ignore" here because of
    unclear ways of describe typing from inheritance class sqlalchemy
    '''

    impl = types.LargeBinary

    cache_ok = True

    def process_bind_param(self, value, dialect) -> bytes:      # type:ignore
        '''set value before write method'''
        return bcrypt.hashpw(
            value.encode('utf8'),
            bcrypt.gensalt()
        )

    def process_result_value(self, value, dialect) -> bytes:    # type:ignore
        '''get value after write method'''
        return value

    def copy(self, **kw) -> 'BHashedBinary':    # type:ignore
        return BHashedBinary(self.impl.length)
