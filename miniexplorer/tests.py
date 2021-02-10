from django.test import TestCase

from .models import Query
from .utils import clean_mutable_commands


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

    def test_execute_injected_query(self):
        TITLE = "SELECT INJECT"
        SQL = "INSERT INTO Students VALUES ('Robert'); DROP TABLE Students; --', 'Derper')"

        query = Query(title=TITLE, sql=SQL)
        query.save()
        result = query.execute()

        self.assertNumQueries(1)
        self.assertIsInstance(result, list)
        self.assertEqual(query.sql, "INTO Students VALUES ('Robert'); TABLE Students; --', 'Derper')")


class UtilTest(TestCase):

    def test_clean_mutable_commands_simple_select(self):
        sql = "select * from auth_user;"

        expected = "SELECT * FROM auth_user;"
        computed = clean_mutable_commands(sql)

        self.assertEqual(computed, expected)

    def test_clean_mutable_commands_simple_select_with_upper_case(self):
        sql = "SELECT * from auth_user;"

        expected = "SELECT * FROM auth_user;"
        computed = clean_mutable_commands(sql)

        self.assertEqual(computed, expected)
    
    def test_clean_mutable_commands_simple_alter(self):
        sql = "alter table auth_user DROP COLUMN password;"

        expected = "TABLE auth_user DROP COLUMN password;"
        computed = clean_mutable_commands(sql)

        self.assertEqual(computed, expected)

    def test_clean_mutable_commands_simple_rename(self):
        sql = "ALTER TABLE old_tablename RENAME TO new_tablename"

        expected = "TABLE old_tablename  TO new_tablename"
        computed = clean_mutable_commands(sql)

        self.assertEqual(computed, expected)

        sql = "RENAME TABLE old_tablename TO new_tablename"

        expected = "TABLE old_tablename TO new_tablename"
        computed = clean_mutable_commands(sql)

        self.assertEqual(computed, expected)

    def test_clean_mutable_commands_simple_update(self):
        sql = "UPDATE table_name set column1 = value1, column2 = value2 WHERE id = 1;"

        expected = "TABLE_NAME SET column1 = value1, column2 = value2 WHERE id = 1;"
        computed = clean_mutable_commands(sql)

        self.assertEqual(computed, expected)

        sql = "RENAME TABLE old_tablename TO new_tablename"

        expected = "TABLE old_tablename TO new_tablename"
        computed = clean_mutable_commands(sql)

        self.assertEqual(computed, expected)

    def test_clean_mutable_commands_simple_replace(self):
        sql = "select REPLACE('SQL Tutorial', 'T', 'M');"

        expected = "SELECT ('SQL Tutorial', 'T', 'M');"
        computed = clean_mutable_commands(sql)

        self.assertEqual(computed, expected)

    def test_clean_mutable_commands_simple_create_table(self):
        sql = "CREATE TABLE Persons (PersonID int,LastName varchar(255));"

        expected = "TABLE Persons (PersonID int,LastName varchar(255));"
        computed = clean_mutable_commands(sql)

        self.assertEqual(computed, expected)

    def test_clean_mutable_commands_simple_grant(self):
        sql = "GRANT EXECUTE ON TestProc TO TesterRole WITH GRANT OPTION;"

        expected = "EXECUTE ON TestProc TO TesterRole WITH  OPTION;"
        computed = clean_mutable_commands(sql)

        self.assertEqual(computed, expected)

    def test_clean_mutable_commands_simple_owner(self):
        sql = "OWNER foo blah"

        expected = "foo blah"
        computed = clean_mutable_commands(sql)

        self.assertEqual(computed, expected)

    def test_clean_mutable_commands_simple_delete(self):
        sql = "delete from auth_user;"

        expected = "FROM auth_user;"
        computed = clean_mutable_commands(sql)

        self.assertEqual(computed, expected)

    def test_clean_mutable_commands_simple_truncate(self):
        sql = "truncate auth_user;"

        expected = "auth_user;"
        computed = clean_mutable_commands(sql)

        self.assertEqual(computed, expected)

    def test_clean_mutable_commands_simple_drop(self):
        sql = "drop table auth_user;"

        expected = "TABLE auth_user;"
        computed = clean_mutable_commands(sql)

        self.assertEqual(computed, expected)

    def test_clean_mutable_commands_multiples_drops(self):
        sql = "drop table auth_user; drop table auth_user;"

        expected = "TABLE auth_user; TABLE auth_user;"
        computed = clean_mutable_commands(sql)

        self.assertEqual(computed, expected)

    def test_clean_mutable_commands_multiples_deletes(self):
        sql = "delete from auth_user; delete from auth_user;"

        expected = "FROM auth_user; FROM auth_user;"
        computed = clean_mutable_commands(sql)

        self.assertEqual(computed, expected)

    def test_clean_mutable_commands_insert_inject(self):
        sql = "INSERT INTO Students VALUES ('Robert'); DROP TABLE Students; --', 'Derper')"

        expected = "INTO Students VALUES ('Robert'); TABLE Students; --', 'Derper')"
        computed = clean_mutable_commands(sql)

        self.assertEqual(computed, expected)

    def test_clean_mutable_commands_select_inject(self):
        sql = "SELECT * FROM auth_user WHERE id = 4;TRUNCATE auth_user"

        expected = "SELECT * FROM auth_user WHERE id = 4; auth_user"
        computed = clean_mutable_commands(sql)

        self.assertEqual(computed, expected)

