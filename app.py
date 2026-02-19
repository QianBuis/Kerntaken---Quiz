from flask import Flask, render_template, request, redirect, session
from auth import register_user, login_user
from admin import admin_bp
from quiz import get_all_quizzes  # voeg bovenaan toe bij je imports
from quiz import (
    
    get_active_quizzes,
    get_categories,
    get_quizzes_by_category,
    get_question_with_answers,
    is_answer_correct
)

app = Flask(__name__)
app.register_blueprint(admin_bp)
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
            return render_template(
                "register.html",
                error="❌ Deze gebruikersnaam bestaat al. Kies een andere."
            )

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

    admin_quizzes = None
    if session.get("role") == "admin":
        admin_quizzes = get_all_quizzes()

    return render_template(
        "dashboard.html",
        username=session["username"],
        role=session.get("role"),
        quizzes=quizzes,
        admin_quizzes=admin_quizzes
    )
# =========================
# CATEGORIE → QUIZ KIEZEN
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


# =========================
# QUIZ FLOW
# =========================

@app.route("/quiz/<int:quiz_id>/start")
def quiz_start(quiz_id):
    if "username" not in session:
        return redirect("/login")

    session["quiz_id"] = quiz_id
    session["q_index"] = 0
    session["correct"] = 0
    session["chosen_answers"] = {}
    session.pop("last_feedback", None)

    return redirect(f"/quiz/{quiz_id}/question")


@app.route("/quiz/<int:quiz_id>/question", methods=["GET", "POST"])
def quiz_question(quiz_id):
    if "username" not in session:
        return redirect("/login")

    if session.get("quiz_id") != quiz_id:
        return redirect(f"/quiz/{quiz_id}/start")

    q_index = session.get("q_index", 0)

    if request.method == "POST":
        # Volgende vraag
        if "next" in request.form:
            session["q_index"] = q_index + 1
            session.pop("last_feedback", None)
            return redirect(f"/quiz/{quiz_id}/question")

        # Antwoord kiezen + feedback
        answer_id = request.form.get("answer_id")
        if not answer_id:
            return redirect(f"/quiz/{quiz_id}/question")

        answer_id = int(answer_id)

        chosen = session.get("chosen_answers", {})
        chosen[str(q_index)] = answer_id
        session["chosen_answers"] = chosen

        correct = is_answer_correct(answer_id)
        if correct:
            session["correct"] = session.get("correct", 0) + 1
            session["last_feedback"] = "✅ Correct!"
        else:
            session["last_feedback"] = "❌ Fout!"

        return redirect(f"/quiz/{quiz_id}/question")

    question = get_question_with_answers(quiz_id, q_index)

    if not question:
        session.pop("last_feedback", None)
        return redirect(f"/quiz/{quiz_id}/result")

    feedback = session.get("last_feedback")
    chosen = session.get("chosen_answers", {})
    chosen_answer_id = chosen.get(str(q_index))

    return render_template(
        "question.html",
        quiz_id=quiz_id,
        question=question,
        q_index=q_index,
        feedback=feedback,
        chosen_answer_id=chosen_answer_id
    )


@app.route("/quiz/<int:quiz_id>/result")
def quiz_result(quiz_id):
    if "username" not in session:
        return redirect("/login")

    if session.get("quiz_id") != quiz_id:
        return redirect("/dashboard")

    score = session.get("correct", 0)
    return render_template("result.html", quiz_id=quiz_id, score=score)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    print(">>> Flask start...")
    app.run(host="127.0.0.1", port=5000, debug=True)

#hi test 2