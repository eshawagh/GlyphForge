from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    jsonify,
    make_response
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

import shelve

from datetime import datetime

from svg_engine import generate_svg


app = Flask(__name__)

app.secret_key = "glyphforge_secret_key"


# =====================================================
# USER DATABASE
# =====================================================

def create_user(username, password):

    with shelve.open("users_db") as db:

        if username in db:
            return False

        db[username] = {
            "password": generate_password_hash(password),
            "glyphs": []
        }

    return True


def validate_user(username, password):

    with shelve.open("users_db") as db:

        if username not in db:
            return False

        stored_hash = db[username]["password"]

        return check_password_hash(
            stored_hash,
            password
        )


# =====================================================
# SAVE GLYPHS
# =====================================================

def save_glyph(username, text, font):

    svg = generate_svg(text, font)

    glyph_data = {
        "text": text,
        "font": font,
        "svg": svg,
        "created": datetime.now().strftime("%d %b %Y %H:%M")
    }

    with shelve.open("users_db", writeback=True) as db:

        db[username]["glyphs"].append(glyph_data)


def get_user_glyphs(username):

    with shelve.open("users_db") as db:

        if username in db:
            return db[username]["glyphs"]

    return []


# =====================================================
# HOME
# =====================================================

@app.route("/")
def home():

    if "user" not in session:
        return redirect("/login")

    glyphs = get_user_glyphs(session["user"])

    return render_template(
        "index.html",
        glyphs=glyphs
    )


# =====================================================
# SIGNUP
# =====================================================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    error = None

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            error = "All fields required."

        else:

            success = create_user(
                username,
                password
            )

            if success:

                session["user"] = username

                return redirect("/")

            else:
                error = "Username already exists."

    return render_template(
        "signup.html",
        error=error
    )


# =====================================================
# LOGIN
# =====================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        valid = validate_user(
            username,
            password
        )

        if valid:

            session["user"] = username

            return redirect("/")

        else:
            error = "Invalid credentials."

    return render_template(
        "login.html",
        error=error
    )


# =====================================================
# LOGOUT
# =====================================================

@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/login")


# =====================================================
# GENERATE SVG
# =====================================================

@app.route("/generate", methods=["POST"])
def generate():

    if "user" not in session:

        return jsonify({
            "error": "Unauthorized"
        }), 401

    text = request.form.get("text", "")
    font = request.form.get("font", "Georgia")

    svg = generate_svg(
        text,
        font
    )

    save_glyph(
        session["user"],
        text,
        font
    )

    return jsonify({
        "svg": svg
    })


# =====================================================
# DOWNLOAD SVG
# =====================================================

@app.route("/download", methods=["POST"])
def download():

    text = request.form.get(
        "text",
        "GlyphForge"
    )

    font = request.form.get(
        "font",
        "Georgia"
    )

    svg = generate_svg(
        text,
        font
    )

    response = make_response(svg)

    response.headers["Content-Type"] = "image/svg+xml"

    response.headers["Content-Disposition"] = (
        "attachment; filename=glyphforge.svg"
    )

    return response


# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":
    app.run(debug=True)