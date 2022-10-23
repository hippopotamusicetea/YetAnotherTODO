from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class ToDoTask(Base):
    __tablename__ = "tasks_sqla"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    priority = Column(Integer)
    body = Column(String)
    complete = Column(Boolean, default=False)
    subtasks = relationship("SubTask")


class SubTask(Base):
    __tablename__ = "subtasks"
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks_sqla.id"))
    name = Column(String)
    priority = Column(Integer)
    body = Column(String)
    complete = Column(Boolean)
