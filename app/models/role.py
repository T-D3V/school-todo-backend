from __future__ import annotations
from app.extensions import db
from sqlalchemy import Column, Integer, String, DateTime
from typing import List
from sqlalchemy.orm import relationship, Mapped
from app.models import user
import datetime

ROLES = {'admin': 1, 'user': 2}


class Role(db.Model):
  __tablename__ = 'role_table'
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(25), nullable=False)
  created_at = Column(DateTime, nullable=False, default=datetime.datetime.now(tz=datetime.timezone.utc))
  updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now(tz=datetime.timezone.utc))
  users: Mapped[List['user.User']] = relationship(back_populates='roles')

  def __repr__(self) -> str:
    return f'<Role "{self.name}">'
