from flask import Flask, render_template, request, redirect, url_for, session
from svg_engine import generate_svg

app = Flask(__name__)

app.secret_key = "super-secret-key"

# temporary fake database
users = {}


# HOME PAGE
@app.route("/", methods=["GET", "POST"])
def home():

    svg_output = ""

    if request.method == "POST":

        text = request.form.get("text")

        svg_output = generate_svg(text)

    return render_template(
        "index.html",
        svg_output=svg_output,
        logged_in=session.get("user")
    )


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = users.get(username)

        if not user:
            error = "User not found"

        elif user["password"] != password:
            error = "Wrong password"

        else:
            session["user"] = username
            return redirect(url_for("home"))

    return render_template("login.html", error=error)


# SIGNUP
@app.route("/signup", methods=["GET", "POST"])
def signup():

    error = None

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if username in users:
            error = "Username already exists"

        elif password != confirm:
            error = "Passwords do not match"

        else:
            users[username] = {
                "email": email,
                "password": password
            }

            session["user"] = username

            return redirect(url_for("home"))

    return render_template("signup.html", error=error)


# LOGOUT
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)