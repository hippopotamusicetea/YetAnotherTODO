import sqlite3
from flask import g
import os

folder = os.path.dirname(__file__)
db_path = os.path.join(folder, "sql_todo.db")


def get_db():
    db = getattr(g, "_sql", None)
    if db is None:
        db = g._sql = sqlite3.connect(db_path)
    return db
