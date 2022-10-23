import datetime
import sqlite3

from queries import queries


# try using class to contain methods but can remove if issues
class SQLTasks:
    def __init__(self, db):
        self.queries = None
        self.db = db

    def connect(self):
        conn = sqlite3.connect(self.db)
        return conn

    def load_queries(self):
        self.queries = queries.SQLQueries()

    def create_table(self):
        with self.connect() as c:
            cur = c.cursor()
            cur.execute(
                """
            CREATE TABLE IF NOT EXISTS tasks_sql
            (id INTEGER PRIMARY KEY ASC,
            name TEXT NOT NULL,
            priority TEXT NOT NULL,
            body TEXT NOT NULL,
            complete TEXT NOT NULL,
            raiseddate timestamp,
            duedate timestamp)
            """
            )
            c.commit()

    def create_todo(self, todo_dict):
        with self.connect() as c:
            print(f"creating: {todo_dict}")
            duedate = datetime.datetime.strptime(
                todo_dict["duedate"], "%Y-%M-%d"
            ).strftime("%d/%M/%Y")
            clean_body = str(todo_dict["body"]).strip()
            cur = c.cursor()
            sql_insert = """
            INSERT INTO tasks_sql(name, priority, body, complete, raiseddate, duedate)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            cur.execute(
                sql_insert,
                (
                    todo_dict["name"],
                    todo_dict["priority"],
                    clean_body,
                    todo_dict["complete"],
                    todo_dict["raiseddate"],
                    duedate,
                ),
            )
            c.commit()
            return cur.lastrowid

    def update_todo(self):
        pass

    def get_todo_list(self):
        with self.connect() as c:
            c.row_factory = sqlite3.Row
            cur = c.cursor()
            cur.execute("select * from tasks_sql")
            rows = cur.fetchall()
            return rows

    def complete_todo(self, todo_id):
        with self.connect() as c:
            cur = c.cursor()
            sql_insert = """
            UPDATE tasks_sql
            SET complete = 1
            WHERE id = ?
            """
            cur.execute(sql_insert, (todo_id,))
            c.commit()
            return cur.lastrowid

    def delete_todo(self, todo_id):
        with self.connect() as c:
            cur = c.cursor()
            sql_insert = """
            DELETE FROM tasks_sql
            WHERE id = ?
            """
            cur.execute(sql_insert, (todo_id,))
            c.commit()
            return cur.lastrowid

    def query_priority(self, priority):
        with self.connect() as c:
            c.row_factory = sqlite3.Row
            cur = c.cursor()
            cur.execute(self.queries.get_priority(), (priority,))
            rows = cur.fetchall()
            return rows
