"""Server for fair play app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db, User, Task_Type
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
#db.SQLAlchemy(app)


@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")


@app.route("/login_page")
def log_in():
    """Log In."""

    return render_template("login_page.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")
    print(email)
    print(password)
    user = crud.get_user_by_email(email)
    print(f"Selected User: {user}")
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        return redirect("/login_page")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        session["user_id"] = user.user_id
        flash(f"Welcome back, {user.email}!")

        return redirect(f"/mypage/{user.user_id}")


@app.route("/about")
def about():
    """View about page."""

    return render_template("about.html")


@app.route("/calendar")
def show_calendar():
    """Show a calendar including tasks that are due."""

    return render_template("calendar.html")


@app.route("/create_account", methods=['POST'])
def create_account():
    """Create an account."""
    email = request.form.get("email")
    password = request.form.get("password")

    # Check if a user already exists with that email
    user = User.query.filter_by(email=email).first()

    if user:
        flash("A user already exists with that email.")
    else:
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created! Please log in.")
        user = User.query.filter_by(email=email).first()
        print(f"asdfasdfasdfasdf: {user}")
    return redirect("login_page")

@app.route("/account_creation_page")
def account_creation_page():
    return render_template("account_creation_page.html")


@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    password = request.form['password']

    user = User(username=username, password=password) # need to hash password for security?
    db.session.add(user)
    db.session.commit()

    return 'Submitted!'


@app.route("/mypage/<int:user_id>")
def mypage(user_id):
    """Show a user's personal page."""
    
    # Check if a user is logged in
    if "user_email" not in session:
        flash("You need to login first.")
        return redirect("/login_page")
    
    # Get the user object for the logged in user
    logged_in_user = crud.get_user_by_email(session["user_email"])
    print(f"logged in user{logged_in_user}")
    # If the logged in user's id doesn't match the user_id in the path, 
    # redirect them to their own page
    if logged_in_user.user_id != user_id:
        flash("You can't access another user's page!")
        return redirect(f"/mypage/{logged_in_user.user_id}")
    
    my_tasks = crud.get_user_tasks(user_id)
    print(f"Tasks: {my_tasks}")
    print(f"Complete status for task {my_tasks[0].was_completed_on_time}")
    print(f"Completed date for task {my_tasks[0].completed_date}")


    return render_template("mypage.html")



@app.route("/options")
def options():
    """Show details on a particular user."""

    return render_template("options.html")


@app.route("/create_task")
def create_task():
    """Render page to create a new task."""
    return render_template("create_task.html")


@app.route("/submit_task", methods=['POST'])
def submit_task():
    """Submit a new task."""

    task_name = request.form['task_name']
    task_description = request.form['task_description']

    # Get the user's ID from the session
    user_id = session.get('user_id')

    # If the user is not logged in, redirect to the login page
    if user_id is None:
        flash("Please log in to create a task.")
        return redirect("/login_page")

    new_task = crud.create_general_task(task_name, task_description)
    db.session.add(new_task)
    db.session.commit()

    flash("New task created!")
    return redirect(f"/mypage/{user_id}")

@app.route("/assign_tasks")
def assign_tasks():
    """View to assign new tasks."""

    # Get the user's ID from the session
    user_id = session.get('user_id')

    # If the user is not logged in, redirect to the login page
    if user_id is None:
        flash("Please log in to assign tasks.")
        return redirect("/login_page")

    # Fetch all task types
    all_task_types = crud.get_all_task_types()

    return render_template("assign_tasks.html", task_types=all_task_types)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)





    # email = request.form.get("email")
    # password = request.form.get("password")

    # user = crud.get_user_by_email(email)
    # if user:
    #     flash("Cannot create an account with that email. Try again.")
    # else:
    #     user = crud.create_user(email, password)
    #     db.session.add(user)
    #     db.session.commit()
    #     flash("Account created! Please log in.")
