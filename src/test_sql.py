import sqlite3

import pytest
from sql import init_sql, add_todo, create_table


@pytest.fixture
def setup_db():
    db = "database/test.db"
    conn = sqlite3.connect(db)
    return conn


def test_init_sql():
    db = "database/test.db"
    conn = init_sql(db)
    assert conn is not None


def test_add_todo(setup_db):
    create_table(setup_db)
    todo = "field 1", "field 2", "field 3", "field 4"
    last_row = add_todo(setup_db, todo)
    assert last_row is not None
