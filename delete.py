import sqlite3

def usun_kontakt(email):
    # Połączenie z bazą danych
    conn = sqlite3.connect("C:\\sqlite\\companies_data.db")
    cursor = conn.cursor()

    # Zapytanie SQL, aby usunąć kontakt na podstawie e-maila
    cursor.execute("DELETE FROM kontakty WHERE email = ?", (email,))

    # Sprawdzamy, ile rekordów zostało usuniętych
    if cursor.rowcount > 0:
        print(f"Kontakt o adresie {email} został usunięty.")
    else:
        print(f"Nie znaleziono kontaktu o adresie {email}.")

    # Zatwierdzamy zmiany w bazie
    conn.commit()

    # Zamknięcie połączenia
    conn.close()

# Przykładowe wywołanie funkcji
usun_kontakt ("firma@example.com")
