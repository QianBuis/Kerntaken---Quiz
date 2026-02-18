from flask import Flask, render_template, request, redirect, session
from auth import register_user, login_user
from quiz import get_active_quizzes, get_categories, get_quizzes_by_category
from quiz import get_question_with_answers

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


# =========================
# STAP 4: categorie kiezen → quiz kiezen
# =========================

@app.route("/choose-category", methods=["GET", "POST"])
def choose_category():
    if "username" not in session:
        return redirect("/login")

    if request.method == "POST":
        category_id = int(request.form["category_id"])
        return redirect(f"/quizzes/category/{category_id}")

    categories = get_categories()
    return render_template("choose_category.html", categories=categories)


@app.route("/quizzes/category/<int:category_id>")
def quizzes_by_category(category_id):
    if "username" not in session:
        return redirect("/login")

    quizzes = get_quizzes_by_category(category_id)
    return render_template("quizzes_by_category.html", quizzes=quizzes)


# Stap 3: quiz start
@app.route("/quiz/<int:quiz_id>/start")
def quiz_start(quiz_id):
    if "username" not in session:
        return redirect("/login")

    session["quiz_id"] = quiz_id
    session["q_index"] = 0
    session["correct"] = 0
    session["chosen_answers"] = {}  # handig om meteen te resetten

    return redirect(f"/quiz/{quiz_id}/question")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# =========================
# STAP 6: per vraag 1 antwoord kiezen (opslaan)
# =========================
@app.route("/quiz/<int:quiz_id>/question", methods=["GET", "POST"])
def quiz_question(quiz_id):
    if "username" not in session:
        return redirect("/login")

    if session.get("quiz_id") != quiz_id:
        return redirect(f"/quiz/{quiz_id}/start")

    q_index = session.get("q_index", 0)

    # POST: speler kiest 1 antwoord en bevestigt
    if request.method == "POST":
        answer_id = request.form.get("answer_id")
        if not answer_id:
            return redirect(f"/quiz/{quiz_id}/question")

        chosen = session.get("chosen_answers", {})
        chosen[str(q_index)] = int(answer_id)
        session["chosen_answers"] = chosen

        # nog geen volgende vraag (stap 8), alleen opslaan
        return redirect(f"/quiz/{quiz_id}/question?saved=1")

    # GET: toon vraag
    question = get_question_with_answers(quiz_id, q_index)
    if not question:
        return "Geen vragen gevonden voor deze quiz."

    saved = request.args.get("saved") == "1"
    chosen = session.get("chosen_answers", {})
    chosen_answer_id = chosen.get(str(q_index))

    return render_template(
        "question.html",
        quiz_id=quiz_id,
        question=question,
        q_index=q_index,
        saved=saved,
        chosen_answer_id=chosen_answer_id
    )


if __name__ == "__main__":
    print(">>> Flask start...")
    app.run(host="127.0.0.1", port=5000, debug=True)
