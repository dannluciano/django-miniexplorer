from collections import namedtuple

from django.db import connection

def raw_sql(query):
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            desc = cursor.description
            nt_result = namedtuple('Result', [col[0] for col in desc])
            return [nt_result(*row) for row in cursor.fetchall()]
        except Exception as e:
            nt_error = namedtuple('Error', 'msg')
            return [nt_error(e), ]