from flask import Blueprint, render_template, request, redirect, session
from quiz import create_quiz, get_categories
from quiz import add_question_with_answers, get_active_quizzes
from quiz import get_questions_by_quiz, delete_question
from quiz import get_question_with_all_answers, update_question_with_answers
from quiz import get_all_quizzes, set_quiz_active

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

@admin_bp.route("/admin/questions/<int:quiz_id>")
def admin_questions(quiz_id):
    if "username" not in session:
        return redirect("/login")
    if session.get("role") != "admin":
        return redirect("/dashboard")

    questions = get_questions_by_quiz(quiz_id)
    return render_template("admin_questions.html", quiz_id=quiz_id, questions=questions)


@admin_bp.route("/admin/delete-question/<int:question_id>", methods=["POST"])
def admin_delete_question(question_id):
    if "username" not in session:
        return redirect("/login")
    if session.get("role") != "admin":
        return redirect("/dashboard")

    delete_question(question_id)
    return redirect(request.referrer or "/dashboard")

@admin_bp.route("/admin/edit-question/<int:question_id>", methods=["GET", "POST"])
def edit_question(question_id):
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

        update_question_with_answers(
            question_id, question_text, answers, correct_index
        )

        return redirect("/dashboard")

    question, answers = get_question_with_all_answers(question_id)

    correct_index = 0
    for i, a in enumerate(answers):
        if a["is_correct"] == 1:
            correct_index = i

    return render_template(
        "admin_edit_question.html",
        question=question,
        answers=answers,
        correct_index=correct_index
    )

@admin_bp.route("/admin/toggle-quiz/<int:quiz_id>", methods=["POST"])
def toggle_quiz(quiz_id):
    if "username" not in session:
        return redirect("/login")

    if session.get("role") != "admin":
        return redirect("/dashboard")

    is_active = request.form.get("is_active") == "1"
    set_quiz_active(quiz_id, is_active)

    return redirect("/dashboard")
