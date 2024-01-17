from __future__ import annotations
from app.extensions import db
from sqlalchemy import Column, Integer, String, DateTime, Text
import datetime

class TodoSecurity(db.Model):
  __tablename__ = 'todo_security_table'
  id = Column(Integer, primary_key=True, autoincrement=True)
  action = Column(String(25), nullable=False)
  todo_id = Column(Integer, nullable=False)
  todo_title = Column(String(150), nullable=True)
  todo_description = Column(Text, nullable=True)
  todo_duedate = Column(DateTime, nullable=True)
  todo_status = Column(Integer, nullable=True)
  todo_user_id = Column(Integer, nullable=True)
  action_by = Column(String(25), nullable=False)
  audited_at = Column(DateTime, nullable=False, default=datetime.datetime.now(tz=datetime.timezone.utc))

  def __repr__(self) -> str:
    return f'<Todo audit "{self.id}">'
  
  @property
  def serialized(self):
    """Return object data in serializable format"""
    return {
      'id': self.id,
      'action': self.action,
      'todo_id': self.todo_id,
      'todo_title': self.todo_title,
      'todo_description': self.todo_description,
      'todo_duedate': self.todo_duedate,
      'todo_status': self.todo_status,
      'todo_user_id': self.todo_user_id,
      'action_by': self.action_by,
      'audited_at': self.audited_at,
    }
