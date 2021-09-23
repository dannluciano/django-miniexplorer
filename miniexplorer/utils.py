import sqlparse
from collections import namedtuple
from django.db import connection


def raw_sql(query):
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            desc = cursor.description
            nt_result = namedtuple("Result", [col[0] for col in desc])
            return [nt_result(*row) for row in cursor.fetchall()]
        except Exception as e:
            nt_error = namedtuple("Error", "msg")
            return [
                nt_error(e),
            ]


def clean_mutable_commands(sql):
    mutable_commands = (
        'ALTER',
        'DROP',
        'INSERT',
        'UPDATE',
        'DELETE',
        'CREATE',
    )

    sql = sqlparse.format(sql, keyword_case='upper')
    
    sql = sql.replace('TRUNCATE', '')
    sql = sql.replace('RENAME', '')
    sql = sql.replace('REPLACE', '')
    sql = sql.replace('GRANT', '')
    sql = sql.replace('OWNER', '')

    statements = sqlparse.parse(sql)
    for statement in statements:
        stmt_type = statement.get_type()
        if stmt_type in mutable_commands:
            sql = sql.replace(stmt_type, '')

    return sql.strip()


def get_database_schema():
    tables = []
    cursor = connection.cursor()
    tables_info = connection.introspection.get_table_list(cursor)
    for table_info in tables_info:
        table_name = table_info.name
        columns = []

        primary_key = connection.introspection.get_primary_key_column(cursor, table_name)
            
        table_description = connection.introspection.get_table_description(cursor, table_name)
        for column_info in table_description:
            column = {
                'name': column_info.name,
                'type': connection.introspection.get_field_type(column_info.type_code, column_info),
                'pk': column_info.name == primary_key,
            }
            columns.append(column)

        table = {
            'name': table_name,
            'columns': columns,
        }
        tables.append(table)
    cursor.close()
    return tables