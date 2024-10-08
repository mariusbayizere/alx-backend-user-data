#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """DB class for handling database operations
    """

    def __init__(self) -> None:
        """Initialize a new DB instance and setup database schema
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)  # Clear the DB
        Base.metadata.create_all(self._engine)  # Create tables
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object to handle database transactions
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database

        Args:
            email (str): The email of the user
            hashed_password (str): The hashed password of the user

        Returns:
            User: The created User object
        """
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(new_user)
        session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments

        Args:
            kwargs: Arbitrary keyword arguments for filtering

        Returns:
            User: The first user found that matches the filters

        Raises:
            NoResultFound: If no user is found
            InvalidRequestError: If invalid query arguments are passed
        """
        session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except NoResultFound:
            raise NoResultFound("No user found with the provided filters.")
        except Exception as e:
            raise InvalidRequestError(f"Invalid request: {e}")

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user’s attributes

        Args:
            user_id (int): The ID of the user to update
            kwargs: Arbitrary keyword arguments of attributes to update

        Returns:
            None

        Raises:
            ValueError: If any argument does not correspond to a user attribute
        """
        session = self._session

        # Find the user by ID
        user = self.find_user_by(id=user_id)

        # Update the user's attributes
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"{key} is not a valid attribute of User")
            setattr(user, key, value)

        # Commit the changes to the database
        session.commit()
