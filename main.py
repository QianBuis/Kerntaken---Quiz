from auth import register, login

def main():
    while True:
        print("\n=== QUIZ APP ===")
        print("1. Registreren")
        print("2. Login")
        print("3. Stoppen")

        keuze = input("Keuze: ")

        if keuze == "1":
            register()
        elif keuze == "2":
            login()
        elif keuze == "3":
            break
        else:
            print("Ongeldige keuze.")

if __name__ == "__main__":
    main()
