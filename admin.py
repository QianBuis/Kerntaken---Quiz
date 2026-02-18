from flask import Blueprint, render_template, request, redirect, session
from quiz import create_quiz, get_categories
from quiz import add_question_with_answers, get_active_quizzes

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/create-quiz", methods=["GET", "POST"])
def create_quiz_route():
    if "username" not in session:
        return redirect("/login")

    if session.get("role") != "admin":
        return redirect("/dashboard")

    if request.method == "POST":
        title = request.form["title"].strip()
        category_id = int(request.form["category_id"])

        create_quiz(title, category_id)
        return redirect("/dashboard")

    categories = get_categories()
    return render_template("admin_create_quiz.html", categories=categories)

@admin_bp.route("/admin/add-question/<int:quiz_id>", methods=["GET", "POST"])
def add_question(quiz_id):
    if "username" not in session:
        return redirect("/login")

    if session.get("role") != "admin":
        return redirect("/dashboard")

    if request.method == "POST":
        question_text = request.form["question_text"]

        answers = [
            request.form["answer1"],
            request.form["answer2"],
            request.form["answer3"],
            request.form["answer4"]
        ]

        correct_index = int(request.form["correct"])

        add_question_with_answers(quiz_id, question_text, answers, correct_index)

        return redirect("/dashboard")

    return render_template("admin_add_question.html", quiz_id=quiz_id)