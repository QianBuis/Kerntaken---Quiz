from flask import Flask, render_template, request, redirect, session
from auth import register_user, login_user

app = Flask(__name__)
app.secret_key = "supersecretkey123"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        data = login_user(username, password)

        if data:
            session["username"] = username
            session["user_id"] = data["user_id"]
            session["role"] = data["role"]   # 'player' of 'admin'
            return redirect("/dashboard")
        else:
            return "Login mislukt"

    return render_template("login.html")
