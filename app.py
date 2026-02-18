# app.py
from flask import Flask, render_template, request, redirect, session
from auth import register_user, login_user
from quiz import get_active_quizzes

app = Flask(__name__)
app.secret_key = "supersecretkey123"

@app.route("/")
def home():
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        ok = register_user(username, password)
        if not ok:
            return render_template("register.html", error="❌ Deze gebruikersnaam bestaat al. Kies een andere.")

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        data = login_user(username, password)

        if data:
            session["username"] = username
            session["user_id"] = data["user_id"]
            session["role"] = data["role"]  # 'player' of 'admin'
            return redirect("/dashboard")

        return render_template("login.html", error="❌ Onjuiste gebruikersnaam of wachtwoord.")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/login")

    quizzes = get_active_quizzes()

    return render_template(
        "dashboard.html",
        username=session["username"],
        role=session.get("role"),
        quizzes=quizzes
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    print(">>> Flask start...")
    app.run(host="127.0.0.1", port=5000, debug=True)
