from __future__ import annotations
from app.extensions import db
from sqlalchemy import Column, Integer, String, ForeignKey
from typing import List
from sqlalchemy.orm import relationship, Mapped
from app.models import role, todo

class User(db.Model):
  __tablename__ = "user_table"
  id = Column(Integer, primary_key=True, autoincrement=True)
  username = Column(String(25), nullable=False, unique=True)
  password = Column(String(512), nullable=False)
  todos: Mapped[List["todo.Todo"]] = relationship(back_populates="users")
  role_id = Column(ForeignKey('role_table.id'))
  roles: Mapped[List["role.Role"]] = relationship(back_populates="users")

  def __repr__(self) -> str:
    return f'<User "{self.username}">'