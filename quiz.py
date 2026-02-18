from database import get_connection

def get_active_quizzes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT q.id, q.title, c.name AS category
        FROM quizzes q
        LEFT JOIN categories c ON q.category_id = c.id
        WHERE q.is_active = 1
        ORDER BY q.created_at DESC
    """)
    quizzes = cursor.fetchall()

    cursor.close()
    conn.close()
    return quizzes

def get_categories():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, name FROM categories ORDER BY name")
    categories = cursor.fetchall()

    cursor.close()
    conn.close()
    return categories

def get_quizzes_by_category(category_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT q.id, q.title, c.name AS category
        FROM quizzes q
        LEFT JOIN categories c ON q.category_id = c.id
        WHERE q.is_active = 1 AND q.category_id = %s
        ORDER BY q.created_at DESC
    """, (category_id,))

    quizzes = cursor.fetchall()

    cursor.close()
    conn.close()
    return quizzes

def get_question_with_answers(quiz_id, index):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, question_text FROM questions WHERE quiz_id=%s ORDER BY id LIMIT 1 OFFSET %s",
        (quiz_id, index)
    )
    question = cursor.fetchone()

    if not question:
        cursor.close()
        conn.close()
        return None

    cursor.execute(
        "SELECT id, answer_text FROM answers WHERE question_id=%s ORDER BY id LIMIT 4",
        (question["id"],)
    )
    answers = cursor.fetchall()

    cursor.close()
    conn.close()

    question["answers"] = answers
    return question

def is_answer_correct(answer_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT is_correct FROM answers WHERE id = %s", (answer_id,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return bool(row and row[0] == 1)

def create_quiz(title, category_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO quizzes (title, category_id, is_active) VALUES (%s, %s, 1)",
        (title, category_id)
    )

    conn.commit()
    cursor.close()
    conn.close()

def add_question_with_answers(quiz_id, question_text, answers, correct_index):
    conn = get_connection()
    cursor = conn.cursor()

    # Vraag toevoegen
    cursor.execute(
        "INSERT INTO questions (quiz_id, question_text) VALUES (%s, %s)",
        (quiz_id, question_text)
    )
    question_id = cursor.lastrowid

    # Antwoorden toevoegen
    for i, answer_text in enumerate(answers):
        is_correct = 1 if i == correct_index else 0
        cursor.execute(
            "INSERT INTO answers (question_id, answer_text, is_correct) VALUES (%s, %s, %s)",
            (question_id, answer_text, is_correct)
        )

    conn.commit()
    cursor.close()
    conn.close()

def delete_question(question_id):
    conn = get_connection()
    cursor = conn.cursor()

    # eerst antwoorden weg (FK-safe)
    cursor.execute("DELETE FROM answers WHERE question_id=%s", (question_id,))
    cursor.execute("DELETE FROM questions WHERE id=%s", (question_id,))

    conn.commit()
    cursor.close()
    conn.close()

def get_questions_by_quiz(quiz_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, question_text FROM questions WHERE quiz_id=%s ORDER BY id",
        (quiz_id,)
    )
    questions = cursor.fetchall()

    cursor.close()
    conn.close()
    return questions

def get_question_with_all_answers(question_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, question_text FROM questions WHERE id=%s",
        (question_id,)
    )
    question = cursor.fetchone()

    cursor.execute(
        "SELECT id, answer_text, is_correct FROM answers WHERE question_id=%s ORDER BY id",
        (question_id,)
    )
    answers = cursor.fetchall()

    cursor.close()
    conn.close()

    return question, answers

def update_question_with_answers(question_id, question_text, answers, correct_index):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE questions SET question_text=%s WHERE id=%s",
        (question_text, question_id)
    )

    cursor.execute(
        "SELECT id FROM answers WHERE question_id=%s ORDER BY id",
        (question_id,)
    )
    answer_ids = [row[0] for row in cursor.fetchall()]

    for i, answer_id in enumerate(answer_ids):
        is_correct = 1 if i == correct_index else 0
        cursor.execute(
            "UPDATE answers SET answer_text=%s, is_correct=%s WHERE id=%s",
            (answers[i], is_correct, answer_id)
        )

    conn.commit()
    cursor.close()
    conn.close()
