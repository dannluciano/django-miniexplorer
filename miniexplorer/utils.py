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