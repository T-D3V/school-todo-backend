from __future__ import annotations
from app.extensions import db
from sqlalchemy import Column, Integer, String
from typing import List
from sqlalchemy.orm import relationship, Mapped
from app.models import user

class Role(db.Model):
  __tablename__ = "role_table"
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(25), nullable=False)
  users: Mapped[List["user.User"]] = relationship(back_populates="roles")

  def __repr__(self) -> str:
    return f'<Role "{self.name}">'