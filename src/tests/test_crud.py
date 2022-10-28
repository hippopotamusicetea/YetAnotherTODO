import pytest
from crud import SQLTasks
import sqlite3
import os


class TestSql:
    @pytest.fixture(scope="session")
    def connect_db(self, tmp_path_factory):
        tmp_dir = tmp_path_factory.mktemp("data")
        tmp_path = os.path.join(tmp_dir, "sql_test.db")
        conn = sqlite3.connect(tmp_path)
        yield conn
        conn.close()

    @pytest.fixture
    def get_sql_obj(self):
        sql = SQLTasks()
        return sql

    def test_load_queries(self):
        from queries import queries

        queries = queries.SQLQueries()
        assert queries, "queries should be imported, queries not imported"

    def test_create_table(self, connect_db, get_sql_obj):
        get_sql_obj.create_table(connect_db)

        with connect_db as c:
            cur = c.cursor()
            sql_q = "SELECT name FROM sqlite_master WHERE type='table' AND name='tasks_sql';"
            cur.execute(sql_q)
            t = cur.fetchone()
            assert t, "table should be created, table not created"

    # add multiple inserts to test
    def test_create_todo(self, connect_db, get_sql_obj):
        todo_dict = {
            "name": "exemption",
            "priority": "High",
            "body": "body",
            "complete": 0,
            "raiseddate": "2022-10-21",
            "duedate": "2022-10-30",
        }
        row_id = get_sql_obj.create_todo(connect_db, todo_dict)
        assert row_id, "row_id should not be none if row created, row not created"

    def test_update_todo(self):
        pass

    def test_get_todo_list(self, connect_db, get_sql_obj):
        row_id = get_sql_obj.complete_todo(connect_db, "1")
        assert row_id, "row_id should exist, no items in db"

    def test_complete_todo(self, connect_db, get_sql_obj):
        row_id = get_sql_obj.complete_todo(connect_db, "1")

        with connect_db as c:
            cur = c.cursor()
            sql_q = f"SELECT complete FROM tasks_sql WHERE id = {row_id};"
            cur.execute(sql_q)
            row = cur.fetchone()
            assert row[0] == "1", "complete should be 1, complete is not 1"

    def test_query_priority(self, connect_db, get_sql_obj):
        priority = "High"
        get_sql_obj.query_priority(connect_db, priority)

        with connect_db as c:
            cur = c.cursor()
            sql_q = f"SELECT priority FROM tasks_sql WHERE id = ?;"
            cur.execute(sql_q, ("1",))
            row = cur.fetchone()
            assert row[0] == "High", "should be High, is not High"

    def test_get_overdue_week(self, connect_db, get_sql_obj):
        rows = get_sql_obj.get_overdue_week(connect_db)
        assert rows[0]["id"] == 1, "should return id 1, did not return id 1"

    def test_get_due_week(self, connect_db, get_sql_obj):
        rows = get_sql_obj.get_due_in_week(connect_db)
        assert rows[0]["id"] == 1, "should return id 1, did not return id 1"

    def test_delete_todo(self, connect_db, get_sql_obj):
        get_sql_obj.delete_todo(connect_db, "1")

        with connect_db as c:
            cur = c.cursor()
            sql_q = f"SELECT * FROM tasks_sql WHERE id = ?;"
            cur.execute(sql_q, ("1",))
            row = cur.fetchone()
            assert not row, "no row should be found, row found"
