from flask import Flask, render_template, request, redirect, session
from auth import register_user, login_user

app = Flask(__name__)
app.secret_key = "supersecretkey123"


# ========================
# HOME
# ========================
@app.route("/")
def home():
    return redirect("/login")


# ========================
# REGISTER
# ========================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        ok = register_user(username, password)
        if not ok:
            return render_template("register.html", error="Gebruikersnaam bestaat al.")

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
            session["role"] = data["role"]
            return redirect("/dashboard")

        return render_template("login.html", error="Onjuiste gegevens.")

    return render_template("login.html")

# ========================
# DASHBOARD
# ========================
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        username=session["username"],
        role=session.get("role")
    )


# ========================
# LOGOUT
# ========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ========================
# START APP (MOET ONDERAAN)
# ========================
if __name__ == "__main__":
    print(">>> Flask start...")
    app.run(host="127.0.0.1", port=5000, debug=True)
