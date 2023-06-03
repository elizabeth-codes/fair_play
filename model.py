from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """a user"""
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(40))
    name = db.Column(db.String(50))

    def__repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"



class Household(db.Model):
    """a household"""
    __tablename__ = "households"

    household_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    household_name = db.Column(db.String(50))
    #users: users are coming in from class User; do I recreate them here? confused.

    def__repr__(self):
        return f"<Household_ID={self.household_id} Household_name={self.household_name}>"


class Task_Type(db.Model):
    """a task in the universe; not necessarily assigned to a user, not necessarily done in a household"""
    __tablename__ = "task_type"

    task_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    task_name = db.Column(db.String(100))
    task_description = db.Column(db.String(5000))

    def__repr__(self):
        return f"<task_name={self.task_name} task_id={self.task_id}>"


class Assigned_Task(db.Model):
    """a task that is done in a household, assigned to a user"""
    __tablename__ = "assigned_task"

    task_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    #task_name = db.Column(db.String(100))
    #task_description = db.Column(db.String(5000))
    was_completed_on_time = db.Column(db.Boolean)
    assigned_to = db.Column(user)
    #                 self.user^???

    def__repr__(self):
        return f"<task_name={self.task_name} task_id={self.task_id}>"




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