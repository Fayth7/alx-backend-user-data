#!/usr/bin/env python3
"""Class User for ORM"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


COLUMN_LENGTH = 250


class User(Base):
    """Representation of a user."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(COLUMN_LENGTH), nullable=False)
    hashed_password = Column(String(COLUMN_LENGTH), nullable=False)
    session_id = Column(String(COLUMN_LENGTH))
    reset_token = Column(String(COLUMN_LENGTH))
