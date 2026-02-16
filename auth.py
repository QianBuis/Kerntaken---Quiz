import bcrypt
from database import get_connection

def register():
    username = input("Kies gebruikersnaam: ")
    password = input("Kies wachtwoord: ")

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (username, hashed_password.decode())
    )

    conn.commit()
    cursor.close()
    conn.close()

    print("Account aangemaakt!")


def login():
    username = input("Gebruikersnaam: ")
    password = input("Wachtwoord: ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        stored_password = result[0]

        if bcrypt.checkpw(password.encode(), stored_password.encode()):
            print("Login succesvol!")
            return True
        else:
            print("Fout wachtwoord.")
            return False
    else:
        print("Gebruiker niet gevonden.")
        return False
