import bcrypt
from database import get_connection

def register_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (username, hashed_password)
    )

    conn.commit()
    cursor.close()
    conn.close()
    return True


def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    # haal ook id op
    cursor.execute("SELECT id, password, role FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        user_id, stored_password, role = result
        if bcrypt.checkpw(password.encode(), stored_password.encode()):
            # role kan NULL zijn → fallback naar player
            return {"user_id": user_id, "role": role or "player"}

    return None
