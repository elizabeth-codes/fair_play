from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """a user"""
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(40))
    name = db.Column(db.String(50))
    household_id = db.Column(db.Integer, db.ForeignKey("households.household_id"))

    household = db.relationship("Household", back_populates = "users")
    assigned_tasks = db.relationship("Assigned_Task", back_populates = "users")

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"



class Household(db.Model):
    """a household"""
    __tablename__ = "households"

    household_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    household_name = db.Column(db.String(50))
    #users: users are coming in from class User; do I recreate them here? confused.
    #user = db.Column(db.String, db.ForeignKey("users.user_id"))

    users = db.relationship("User", back_populates = "household")
    
    

    def __repr__(self):
        return f"<Household_ID={self.household_id} Household_name={self.household_name}>"


class Task_Type(db.Model):
    """a task in the universe; not necessarily assigned to a user, not necessarily done in a household"""
    __tablename__ = "task_type"

    task_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    task_name = db.Column(db.String(100))
    task_description = db.Column(db.String(5000))
    # assigned_task_id = db.Column(db.Integer, db.ForeignKey("assigned_task.assigned_task_id"))
    assigned_tasks = db.relationship("Assigned_Task", back_populates = "task_type")

    def __repr__(self):
        return f"<task_name={self.task_name} task_id={self.task_id}>"


class Assigned_Task(db.Model):
    """a task that is done in a household, assigned to a user"""
    __tablename__ = "assigned_task"

    assigned_task_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    was_completed_on_time = db.Column(db.Boolean)
    active_status = db.Column(db.Boolean, default = True)
    #frequency = db.
    completed_date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)
    assigned_to = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    task_id = db.Column(db.Integer, db.ForeignKey("task_type.task_id"))

    users = db.relationship("User", back_populates = "assigned_tasks")
    task_type = db.relationship("Task_Type", back_populates = "assigned_tasks")

    def __repr__(self):
        return f"<assigned_task_id={self.assigned_task_id}>"




def connect_to_db(flask_app, db_uri="postgresql:///fair_play", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    connect_to_db(app)