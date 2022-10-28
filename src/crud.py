import datetime
import sqlite3

from queries import queries


# try using class to contain methods but can remove if issues
class SQLTasks:
    def __init__(self):
        self.queries = queries.SQLQueries()

    @staticmethod
    def create_table(conn):
        with conn as c:
            cur = c.cursor()
            cur.executescript(
                """
            PRAGMA foreign_keys = ON;
            CREATE TABLE IF NOT EXISTS tasks_sql
            (id INTEGER PRIMARY KEY ASC,
            name TEXT NOT NULL,
            priority TEXT NOT NULL,
            body TEXT NOT NULL,
            category TEXT NOT NULL,
            complete TEXT NOT NULL,
            raiseddate DATE,
            duedate DATE);
            
            CREATE TABLE IF NOT EXISTS subtasks_sql
            (id INTEGER PRIMARY KEY ASC,
            subtask TEXT NOT NULL,
            completion_time INTEGER NOT NULL,
            complete TEXT NOT NULL,
            parent_task_id INTEGER NOT NULL,
            FOREIGN KEY (parent_task_id) REFERENCES tasks_sql (id)
            );
            CREATE INDEX IF NOT EXISTS taskindex ON subtasks_sql(parent_task_id);
            """
            )
            c.commit()

    @staticmethod
    def create_todo(conn, todo_dict):
        with conn as c:
            clean_body = str(todo_dict["body"]).strip()
            raised_date = datetime.datetime.strptime(todo_dict["raiseddate"], "%d/%m/%Y")
            due_date = datetime.datetime.strptime(todo_dict["duedate"], "%Y-%m-%d")
            cur = c.cursor()
            sql_insert = """
            INSERT INTO tasks_sql(name, priority, body, category, complete, raiseddate, duedate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cur.execute(
                sql_insert,
                (
                    todo_dict["name"],
                    todo_dict["priority"],
                    clean_body,
                    todo_dict["category"],
                    todo_dict["complete"],
                    raised_date,
                    due_date,
                ),
            )
            c.commit()
            return cur.lastrowid

    @staticmethod
    def create_subtask(conn, subtask_dict):
        with conn as c:
            clean_subtask = str(subtask_dict["subtask"]).strip()
            cur = c.cursor()
            sql_insert = """
            INSERT INTO subtasks_sql(subtask, completion_time, complete, parent_task_id)
            VALUES (?, ?, ?, ?)
            """
            cur.execute(
                sql_insert,
                (
                    clean_subtask,
                    subtask_dict["completiontime"],
                    subtask_dict["complete"],
                    subtask_dict["task_id"],
                ),
            )
            c.commit()
            return cur.lastrowid

    @staticmethod
    def update_todo():
        pass

    @staticmethod
    def get_todo_list(conn):
        with conn as c:
            c.row_factory = sqlite3.Row
            cur = c.cursor()
            cur.execute("select * from tasks_sql")
            rows = cur.fetchall()
            return rows

    @staticmethod
    def get_children(conn, task_id):
        with conn as c:
            c.row_factory = sqlite3.Row
            cur = c.cursor()
            sql_insert = """
            SELECT id, subtask, completion_time, complete FROM subtasks_sql
            WHERE parent_task_id = ?
            """
            cur.execute(sql_insert, (task_id,))
            rows = cur.fetchall()
            return rows

    @staticmethod
    def complete_todo(conn, todo_id):
        with conn as c:
            cur = c.cursor()
            sql_insert = """
            UPDATE tasks_sql
            SET complete = 1
            WHERE id = ?
            """
            cur.execute(sql_insert, (todo_id,))
            c.commit()
            return cur.lastrowid

    @staticmethod
    def complete_subtask(conn, subtask_id):
        with conn as c:
            cur = c.cursor()
            sql_insert = """
            UPDATE subtasks_sql
            SET complete = 1
            WHERE id = ?
            """
            cur.execute(sql_insert, (subtask_id,))
            c.commit()
            return cur.lastrowid

    @staticmethod
    def delete_todo(conn, todo_id):
        with conn as c:
            cur = c.cursor()
            sql_insert = """
            DELETE FROM tasks_sql
            WHERE id = ?
            """
            cur.execute(sql_insert, (todo_id,))
            c.commit()
            sql_insert_children = """
            DELETE FROM subtasks_sql
            WHERE parent_task_id = ?
            """
            cur.execute(sql_insert_children, (todo_id,))
            c.commit()
            return cur.lastrowid

    @staticmethod
    def delete_subtask(conn, subtask_id):
        with conn as c:
            cur = c.cursor()
            sql_insert = """
            DELETE FROM subtasks_sql
            WHERE id = ?
            """
            cur.execute(sql_insert, (subtask_id,))
            c.commit()
            return cur.lastrowid

    def query_priority(self, conn, priority):
        with conn as c:
            c.row_factory = sqlite3.Row
            cur = c.cursor()
            cur.execute(self.queries.get_priority(), (priority,))
            rows = cur.fetchall()
            return rows

    def get_overdue_week(self, conn):
        with conn as c:
            c.row_factory = sqlite3.Row
            cur = c.cursor()
            cur.execute(self.queries.on_list_over_week())
            rows = cur.fetchall()
            return rows

    def get_due_in_week(self, conn):
        with conn as c:
            c.row_factory = sqlite3.Row
            cur = c.cursor()
            cur.execute(self.queries.due_in_week())
            rows = cur.fetchall()
            return rows

    def get_category(self, conn, category):
        with conn as c:
            c.row_factory = sqlite3.Row
            cur = c.cursor()
            cur.execute(self.queries.get_category(), (category,))
            rows = cur.fetchall()
            return rows

    def get_status(self, conn, status):
        with conn as c:
            c.row_factory = sqlite3.Row
            cur = c.cursor()
            cur.execute(self.queries.get_status(), (status,))
            rows = cur.fetchall()
            return rows

    def get_times(self, conn):
        with conn as c:
            c.row_factory = sqlite3.Row
            cur = c.cursor()
            cur.execute(self.queries.get_time_to_complete())
            rows = cur.fetchone()
            return rows

    def get_todo_num(self, conn):
        with conn as c:
            c.row_factory = sqlite3.Row
            cur = c.cursor()
            cur.execute(self.queries.get_num_todos())
            rows = cur.fetchone()
            return rows
