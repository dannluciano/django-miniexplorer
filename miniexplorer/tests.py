from django.test import TestCase

from .models import Query


class QueryTest(TestCase):
    fixture = ["queries.json"]

    def test_query(self):
        self.assertTrue(True)

    def test_execute_valid_query(self):
        TITLE = "SELECT 2 + 2"
        SQL = "SELECT 2 + 2 as Quatro"

        query = Query(title=TITLE, sql=SQL)
        result = query.execute()

        self.assertNumQueries(1)
        self.assertIsInstance(result, list)

    def test_execute_invalid_query(self):
        TITLE = "SELECT"
        SQL = "SELECT"

        query = Query(title=TITLE, sql=SQL)
        result = query.execute()

        self.assertNumQueries(1)
        self.assertIsInstance(result, list)
