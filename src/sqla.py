"""
SQLAlchemy DB
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import ToDoTask, Base


def init_db():
    engine = create_engine("sqlite:///database/todo.db")
    Base.metadata.bind = engine
    session = sessionmaker(bind=engine)
    Base.metadata.create_all()
    s = session()
    return s


def add_todo(session, n, p, b, c):
    t = ToDoTask(name=n, priority=p, body=b, complete=c)
    session.add(t)
    session.commit()


def get_todo_list(session):
    todo_list = session.query(ToDoTask).all()
    return todo_list


engine = create_engine("sqlite:///database/todo.db")
Base.metadata.bind = engine
session = sessionmaker(bind=engine)
Base.metadata.create_all()
s = session()

if __name__ == "__main__":
    s = init_db()
    t_l = get_todo_list(s)
    print(t_l)
    for x in t_l:
        print(x.name)
        print(x.priority)
        print(x.body)
        print(x.complete)
