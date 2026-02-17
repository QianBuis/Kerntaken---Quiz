from database import get_connection

def save_score(user_id, quiz_id, score, time_taken=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO scores (user_id, quiz_id, score, time_taken) VALUES (%s, %s, %s, %s)",
        (user_id, quiz_id, score, time_taken)
    )

    conn.commit()
    cursor.close()
    conn.close()
