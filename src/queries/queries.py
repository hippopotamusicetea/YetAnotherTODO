class SQLQueries:
    @staticmethod
    def get_priority():
        query = """
        SELECT *
        FROM tasks_sql
        WHERE priority = ?;
        """
        return query
