import datetime


class SQLQueries:
    @staticmethod
    def get_priority():
        query = """
        SELECT *
        FROM tasks_sql
        WHERE priority = ?;
        """
        return query

    @staticmethod
    def on_list_over_week():
        query = """
        SELECT *
        FROM tasks_sql
        WHERE raiseddate <= DATE('now', '-6 days');
        """
        return query

    @staticmethod
    def due_in_week():
        query = """
        SELECT *
        FROM tasks_sql
        WHERE duedate BETWEEN DATE('now') AND DATE('now', '+6 days');
        """
        return query

    @staticmethod
    def get_category():
        query = """
         SELECT *
         FROM tasks_sql
         WHERE category = ?;
         """
        return query

    @staticmethod
    def get_status():
        query = """
         SELECT *
         FROM tasks_sql
         WHERE complete = ?;
         """
        return query

    @staticmethod
    def get_time_to_complete():
        query = """
         SELECT SUM(completion_time)
         FROM subtasks_sql
         WHERE complete = 0;
         """
        return query

    @staticmethod
    def get_num_todos():
        query = """
         SELECT COUNT(id)
         FROM tasks_sql
         WHERE complete = 0;
         """
        return query
