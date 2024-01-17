from __future__ import annotations
from app.extensions import db
from sqlalchemy import Column, Integer, String, DateTime
import datetime

class UserSecurity(db.Model):
  __tablename__ = 'user_security_table'
  id = Column(Integer, primary_key=True, autoincrement=True)
  action = Column(String(25), nullable=False)
  user_id = Column(Integer, nullable=False)
  user_username = Column(String(25), nullable=True)
  user_role_id = Column(Integer, nullable=True)
  action_by = Column(String(25), nullable=False)
  audited_at = Column(DateTime, nullable=False, default=datetime.datetime.now(tz=datetime.timezone.utc))

  def __repr__(self) -> str:
    return f'<User audit "{self.id}">'
  
  @property
  def serialized(self):
    """Return object data in serializable format"""
    return {
      'id': self.id,
      'action': self.action,
      'user_id': self.user_id,
      'user_username': self.user_username,
      'user_role_id': self.user_role_id,
      'action_by': self.action_by,
      'audited_at': self.audited_at,
    }
