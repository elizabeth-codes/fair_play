"""CRUD operations."""

from model import db, User, Household, Task_Type, Assigned_Task, connect_to_db


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user


def create_assigned_task(was_on_time, active_status, assigned_to, completed_date, task_id):
    """Create a task for the assigned task table"""

    assigned_task = Assigned_Task(
        #assigned_task_id=assigned_task_id, 
        completed_date=completed_date,
        users=User.query.filter(User.user_id == assigned_to).first(), 
        was_completed_on_time=was_on_time, 
        active_status=active_status, 
        assigned_to=assigned_to, 
        task_id=task_id)
    
    return assigned_task


def create_general_task(task_name, task_description):
    """Create a task for the general tasks table."""
    general_task = Task_Type( 
        task_name=task_name,
        task_description=task_description, 
    )
    return general_task

def get_users():
    """Return all users."""

    return User.query.all()


def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""
    return User.query.filter(User.email == email).first()

def get_user_tasks(user_id):
    """Return tasks that the user has done and has yet to do. """
    return Assigned_Task.query.filter(Assigned_Task.assigned_to == user_id).all()

def get_all_task_types():
    """Return all rows of task_type."""

    return Task_Type.query.all()


if __name__ == "__main__":
    from server import app

    connect_to_db(app)