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

