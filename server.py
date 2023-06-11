"""Server for fair play app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db, User
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

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

    return redirect("/")


@app.route("/about")
def about():
    """View about page."""

    return render_template("about.html")


@app.route("/calendar")
def show_calendar():
    """Show a calendar including tasks that are due."""

    return render_template("calendar.html")


@app.route("/create_account")
def create_account():
    """Create an account."""

    if request.method == "POST":
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

    return render_template("create_account.html")


@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    password = request.form['password']

    user = User(username=username, password=password) # need to hash password for security?
    db.session.add(user)
    db.session.commit()

    return 'Submitted!'


@app.route("/mypage")
def mypage():
    """Show a user's personal page."""

    return redirect("/mypage.html")


@app.route("/options")
def options():
    """Show details on a particular user."""

    return render_template("options.html")


# @app.route("/login", methods=["POST"])
# def process_login():
#     """Process user login."""

#     email = request.form.get("email")
#     password = request.form.get("password")

#     user = crud.get_user_by_email(email)
#     if not user or user.password != password:
#         flash("The email or password you entered was incorrect.")
#     else:
#         # Log in user by storing the user's email in session
#         session["user_email"] = user.email
#         flash(f"Welcome back, {user.email}!")

#     return redirect("/")

# @app.route("/update_rating", methods=["POST"])
# def update_rating():
#     rating_id = request.json["rating_id"]
#     updated_score = request.json["updated_score"]
#     crud.update_rating(rating_id, updated_score)
#     db.session.commit()

#     return "Success"

# @app.route("/movies/<movie_id>/ratings", methods=["POST"])
# def create_rating(movie_id):
#     """Create a new rating for the movie."""

#     logged_in_email = session.get("user_email")
#     rating_score = request.form.get("rating")

#     if logged_in_email is None:
#         flash("You must log in to rate a movie.")
#     elif not rating_score:
#         flash("Error: you didn't select a score for your rating.")
#     else:
#         user = crud.get_user_by_email(logged_in_email)
#         movie = crud.get_movie_by_id(movie_id)

#         rating = crud.create_rating(user, movie, int(rating_score))
#         db.session.add(rating)
#         db.session.commit()

#         flash(f"You rated this movie {rating_score} out of 5.")

#     return redirect(f"/movies/{movie_id}")


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
