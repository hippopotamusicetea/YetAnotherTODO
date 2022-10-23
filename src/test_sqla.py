import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base
from sqla import init_db, add_todo


@pytest.fixture
def get_session():
    engine = create_engine("sqlite:///database/sqla_test.db")
    Base.metadata.bind = engine
    session = sessionmaker(bind=engine)
    Base.metadata.create_all()
    s = session()
    return s


def test_init_db():
    s = init_db()
    assert s is not None


def test_add_todo(get_session):
    n, p, b, c = "name", "priority", "body", False
    add_todo(get_session, n, p, b, c)
