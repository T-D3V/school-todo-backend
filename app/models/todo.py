from __future__ import annotations
from app.extensions import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, relationship
from typing import List
from app.models import user
import datetime


class Todo(db.Model):
  __tablename__ = 'todo_table'
  id = Column(Integer, primary_key=True, autoincrement=True)
  title = Column(String(150), nullable=False)
  description = Column(Text, nullable=False)
  duedate = Column(DateTime, nullable=False, default=datetime.datetime.now(tz=datetime.timezone.utc))
  status = Column(Integer, nullable=False)
  user_id = Column(ForeignKey('user_table.id'))
  users: Mapped[List['user.User']] = relationship(back_populates='todos')

  @property
  def serialized(self):
    """Return object data in serializable format"""
    return {
      'id': self.id,
      'title': self.title,
      'description': self.description,
      'duedate': self.duedate,
      'status': self.status,
      'user_id': self.user_id,
    }

  def __repr__(self) -> str:
    return f'<Todo "{self.title}">'
