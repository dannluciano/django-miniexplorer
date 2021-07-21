import json
from django.db import connections

def get_database_schema():
    tables = []
    connection = connections.all()[0]

    with connection.cursor() as cursor:
        tables_info = connection.introspection.get_table_list(cursor)
        for table_info in tables_info:
            table_name = table_info.name
            columns = []
            
            table_description = connection.introspection.get_table_description(cursor, table_name)
            for column_info in table_description:
                column = {
                    'name': column_info.name,
                    'type': column_info.type_code,
                    'pk': column_info.pk,
                }
                columns.append(column)
                
            table = {
                'name': table_name,
                'columns': columns,
            }
            tables.append(table)
        return json.dumps(tables)

get_database_schema()