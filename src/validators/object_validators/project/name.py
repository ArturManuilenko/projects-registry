from src.manager__common__db.helpers.project.generate_project_cypher import generate_project_cypher
from src.service__api.main import jira
from src.utils.jira import JiraException


def project_name_format(
        customer_organization_id: str,
        executor_organization_id: str,
        key: str,
        name: str,
) -> bool:
    project_cypher = generate_project_cypher(
        customer_key=customer_organization_id,
        executor_key=executor_organization_id,
        project_key=key,
        project_name=name
    )
    try:
        jira_name = jira.get_project(key=key)['name']
        if jira_name == project_cypher:
            return True
        else:
            raise ValueError("project name have not correct format in Jira")
    except JiraException as e:
        raise ValueError(e)
