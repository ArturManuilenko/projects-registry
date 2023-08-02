def generate_project_cypher(
    customer_key: str,
    executor_key: str,
    project_key: str,
    project_name: str
) -> str:
    # UL_NE_IAA Учёт проектов
    return customer_key + '_' + executor_key + '_' + project_key + " " + project_name
