from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from svg_engine import generate_svg

app = Flask(__name__)

app.secret_key = "glyphforge-secret-key"

# temporary in-memory users
users = {}


# ─────────────────────────────────────────────
# HOME
# ─────────────────────────────────────────────
@app.route("/", methods=["GET"])
def home():

    # protect route
    if not session.get("user"):
        return redirect(url_for("login"))

    return render_template(
        "index.html",
        logged_in=session.get("user")
    )


# ─────────────────────────────────────────────
# LIVE SVG GENERATOR ROUTE
# ─────────────────────────────────────────────
@app.route("/generate", methods=["POST"])
def generate():

    text = request.form.get("text", "")
    font = request.form.get("font", "georgia")

    svg_output = generate_svg(text, font)

    return jsonify({
        "svg": svg_output
    })


# ─────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────
@app.route("/login", methods=["GET", "POST"])
def login():

    if session.get("user"):
        return redirect(url_for("home"))

    error = None

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = users.get(username)

        if not user:
            error = "User not found"

        elif user["password"] != password:
            error = "Incorrect password"

        else:
            session["user"] = username
            return redirect(url_for("home"))

    return render_template("login.html", error=error)


# ─────────────────────────────────────────────
# SIGNUP
# ─────────────────────────────────────────────
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if session.get("user"):
        return redirect(url_for("home"))

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


# ─────────────────────────────────────────────
# LOGOUT
# ─────────────────────────────────────────────
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect(url_for("login"))


# ─────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)