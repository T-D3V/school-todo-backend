from __future__ import annotations
from app.extensions import db
from sqlalchemy import Column, Integer, String, DateTime
import datetime

class RoleSecurity(db.Model):
  __tablename__ = 'role_security_table'
  id = Column(Integer, primary_key=True, autoincrement=True)
  action = Column(String(25), nullable=False)
  role_id = Column(Integer, nullable=False)
  role_name = Column(String(25), nullable=True)
  action_by = Column(String(25), nullable=False)
  audited_at = Column(DateTime, nullable=False, default=datetime.datetime.now(tz=datetime.timezone.utc))

  def __repr__(self) -> str:
    return f'<Role audit "{self.id}">'
  
  @property
  def serialized(self):
    """Return object data in serializable format"""
    return {
      'id': self.id,
      'action': self.action,
      'role_id': self.role_id,
      'role_name': self.role_name,
      'action_by': self.action_by,
      'audited_at': self.audited_at,
    }
