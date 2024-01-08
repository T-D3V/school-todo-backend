from __future__ import annotations
from app.extensions import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from typing import List
from sqlalchemy.orm import relationship, Mapped
from app.models import role, todo
import datetime


class User(db.Model):
  __tablename__ = 'user_table'
  id = Column(Integer, primary_key=True, autoincrement=True)
  username = Column(String(25), nullable=False, unique=True)
  password = Column(String(512), nullable=False)
  todos: Mapped[List['todo.Todo']] = relationship(back_populates='users')
  created_at = Column(DateTime, nullable=False, default=datetime.datetime.now(tz=datetime.timezone.utc))
  updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now(tz=datetime.timezone.utc))
  role_id = Column(ForeignKey('role_table.id'))
  roles: Mapped[List['role.Role']] = relationship(back_populates='users')

  def __repr__(self) -> str:
    return f'<User "{self.username}">'

  @property
  def serialized(self):
    """Return object data in serializable format"""
    return {
      'id': self.id,
      'username': self.username,
      'role_id': self.role_id,
      'created_at': self.created_at,
      'updated_at': self.updated_at,
    }
