"""SQL queries.

This module contains all the SQL queries used in the project.

Functions:
    read_from_sql: Reads a query from a file and returns it as a string.

"""

import typing
from string import Template


def read_from_sql(filename: str, query_parameters: typing.Dict[str, typing.Union[str, int]]) -> str:
    """Read from sql.

    Reads a query from a file and returns it as a string.

    Args:
        filename (str): Path to the file containing the query.
        query_parameters (dict): Arguments to be passed to the query.

    Returns:
        str: Spark DataFrame if the read was successful

    """
    with open(filename, "r", encoding="utf-8") as file_object:
        # read file content
        query = file_object.read()

    query = Template(query).substitute(query_parameters)

    return query
