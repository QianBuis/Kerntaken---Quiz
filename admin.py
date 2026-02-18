from flask import Blueprint, render_template, request, redirect, session
from quiz import create_quiz, get_categories

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
