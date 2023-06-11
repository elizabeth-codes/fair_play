"""CRUD operations."""

from model import db, User, Household, Task_Type, Assigned_Task, connect_to_db


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user


def get_users():
    """Return all users."""

    return User.query.all()


def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""
    return User.query.filter(User.email == email).first()


if __name__ == "__main__":
    from server import app

    connect_to_db(app)