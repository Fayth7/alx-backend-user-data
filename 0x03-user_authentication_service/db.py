#!/usr/bin/env python3
""" Database for ORM """

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar
from user import Base, User


class DB:
    """DB Class for Object Relational Mapping"""

    def __init__(self, database_url="sqlite:///my_database.db"):
        """Constructor Method"""
        self._engine = create_engine(database_url, echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Session Getter Method"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds user to the database
        Return: User Object
        """
        user = User(email=email, hashed_password=hashed_password)
        with self._session as session:
            session.add(user)
            session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        """Finds user by keyword args
        Return: First row found in the users table as filtered by kwargs
        """
        if not kwargs:
            raise InvalidRequestError("No filter criteria provided")

        column_names = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in column_names:
                raise InvalidRequestError(f"Invalid filter key: {key}")

        with self._session as session:
            user = session.query(User).filter_by(**kwargs).first()

        if user is None:
            raise NoResultFound("No user found with the specified criteria")

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user's attributes
        Returns: None
        """
        user = self.find_user_by(id=user_id)

        column_names = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in column_names:
                raise ValueError(f"Invalid attribute key: {key}")

        for key, value in kwargs.items():
            setattr(user, key, value)

        with self._session as session:
            session.commit()
