import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///budget.db")

# List of default categories
default_categories = ["Utilities", "Rent", "Food", "Market", "Entertainment", "Health", "Fuel", "Gifts", "Insurance", "Taxes"]

# List of months
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December", "Whole Year"]


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """ Overview of expenses """

    # Query for every year that has entries
    years = db.execute("SELECT strftime('%Y', timestamp) AS year FROM expenses WHERE user_id = ? GROUP BY year ORDER BY year DESC",
                       session.get("user_id"))

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        requested_year = request.form.get("year")

        # Convert month from its name to the appropriate number
        requested_month = request.form.get("month")
        if not requested_month in months:
            return apology("month does not exist")
        for i in range(len(months)):
            if months[i] == requested_month:
                requested_month = i + 1

        # Convert month to string so it can be used in a database query
        if requested_month < 10:
            requested_month = "0" + str(requested_month)
        else:
            requested_month = str(requested_month)

        # Decide the display according to the user's selection (whole year or individual month)
        if requested_month == "13":
            # Query for each category and the amount of money spent during the whole year
            rows = db.execute("SELECT category, SUM(amount) AS total FROM expenses WHERE user_id = ? AND strftime('%Y', timestamp) = ? GROUP BY category",
                              session.get("user_id"), str(requested_year))

            # Query for total money spent during the whole year
            total = db.execute("SELECT SUM(amount) AS grand_total FROM expenses WHERE user_id = ? AND strftime('%Y', timestamp) = ?",
                               session.get("user_id"), str(requested_year))
        else:
            # Query for each category and the amount of money spent during the selected month by the current user
            rows = db.execute("SELECT category, SUM(amount) AS total FROM expenses WHERE user_id = ? AND strftime('%Y', timestamp) = ? AND strftime('%m', timestamp) = ? GROUP BY category",
                              session.get("user_id"), str(requested_year), requested_month)

            # Query for total money spent during the selected month by the current user
            total = db.execute("SELECT SUM(amount) AS grand_total FROM expenses WHERE user_id = ? AND strftime('%Y', timestamp) = ? AND strftime('%m', timestamp) = ?",
                               session.get("user_id"), str(requested_year), requested_month)

        return render_template("index.html", years=years, months=months, year=requested_year, month=months[int(requested_month)-1], expenses=rows, grand_total=total[0]["grand_total"])

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        current_year = date.today().year
        current_month = date.today().month

        # Convert month to string so it can be used in a database query
        if current_month < 10:
            current_month = "0" + str(current_month)
        else:
            current_month = str(current_month)

        # Query for each category and the amount of money spent during the last month by the current user
        rows = db.execute("SELECT category, SUM(amount) AS total FROM expenses WHERE user_id = ? AND strftime('%Y', timestamp) = ? AND strftime('%m', timestamp) = ? GROUP BY category",
                          session.get("user_id"), str(current_year), current_month)

        # Query for total money spent during the last month by the current user
        total = db.execute("SELECT SUM(amount) AS grand_total FROM expenses WHERE user_id = ? AND strftime('%Y', timestamp) = ? AND strftime('%m', timestamp) = ?",
                           session.get("user_id"), str(current_year), current_month)

        return render_template("index.html", years=years, months=months, year=current_year, month=months[int(current_month)-1], expenses=rows, grand_total=total[0]["grand_total"])


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Log user in """

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Flash a message
        flash("You were successfully logged in!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """ Log user out """

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register user """

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username is not taken
        username = request.form.get("username")
        user_list = db.execute("SELECT username FROM users WHERE username = ?",
                               username)
        if user_list:
            return apology("username already exists")

        # Insert new user into the database
        password = request.form.get("password")
        id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                        username, generate_password_hash(password))

        # Set the categories of the new user to the default categories
        for i in range(len(default_categories)):
            db.execute("INSERT INTO categories (user_id, category) VALUES (?, ?)",
                       id, default_categories[i])

        # Log new user in
        session["user_id"] = id

        # Flash a message
        flash("You were successfully registered!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """ Change password """

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure old password is correct
        old_password = request.form.get("oldpassword")
        rows = db.execute("SELECT * FROM users WHERE id = ?",
                          session.get("user_id"))
        if not check_password_hash(rows[0]["hash"], old_password):
            return apology("old password is not correct")

        # Update password entry at the database
        new_password = request.form.get("newpassword")
        db.execute("UPDATE users SET hash = ? WHERE id = ?",
                        generate_password_hash(new_password), session.get("user_id"))

        # Forget any user_id
        session.clear()

        # Flash a message
        flash("Password was successfully changed!")

        # Redirect user to login form
        return render_template("login.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change_password.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """ Add a new expense """

    # Query for all categories of the current user
    categories = db.execute("SELECT category FROM categories WHERE user_id = ?",
                                session.get("user_id"))
    for i in range(len(categories)):
            categories[i] = categories[i]["category"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Check for invalid user input in category
        category = request.form.get("category")
        if not category in categories:
            return apology("category does not exist")

        # Convert amount to float with two decimal places
        amount = int(float(request.form.get("amount")) * 100)
        amount = float(amount / 100)

        description = request.form.get("description")
        timestamp = request.form.get("date")

        # Insert new expense into the database
        db.execute("INSERT INTO expenses (user_id, category, amount, description, timestamp) VALUES (?, ?, ?, ?, ?)",
                   session.get("user_id"), category, amount, description, timestamp)

        # Flash a message
        flash(f"You added {usd(amount)} for {category}!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        today = date.today()
        return render_template("add.html", categories=categories, today=today)


@app.route("/categories", methods=["GET", "POST"])
@login_required
def categories():
    """ Add a new category """

    # Query for all categories of the current user
    categories = db.execute("SELECT category FROM categories WHERE user_id = ?",
                                session.get("user_id"))
    for i in range(len(categories)):
            categories[i] = categories[i]["category"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Check if new category already exists
        category = request.form.get("newcategory")
        if category in categories:
            return apology("category already exists")

        # Insert new category into the database
        db.execute("INSERT INTO categories (user_id, category) VALUES (?, ?)",
                   session.get("user_id"), category)

        # Flash a message
        flash(f"You added a new category: {category}!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("categories.html", categories=categories)


@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    """ Show history of expenses """

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Remove expense from the database
        id = request.form.get("id")
        db.execute("DELETE FROM expenses WHERE id = ?", id)

        # Query for all expenses of the current user
        rows = db.execute("SELECT * FROM expenses WHERE user_id = ? ORDER BY timestamp DESC",
                          session.get("user_id"))

        # Flash a message
        flash(f"Expense was successfully removed!")

        return render_template("history.html", expenses=rows)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        rows = db.execute("SELECT * FROM expenses WHERE user_id = ? ORDER BY timestamp DESC",
                          session.get("user_id"))

        return render_template("history.html", expenses=rows)

