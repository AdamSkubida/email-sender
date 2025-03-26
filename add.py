import sqlite3

def dodaj_kontakt(imie, email, firma):
    # Połączenie z bazą danych
    conn = sqlite3.connect("C:\\sqlite\\companies_data.db")
    cursor = conn.cursor()

    # Sprawdzamy, czy email już istnieje w bazie
    cursor.execute("SELECT * FROM kontakty WHERE email = ?", (email,))
    wynik = cursor.fetchone()

    if wynik:  # Jeśli wynik istnieje, tzn. email już w bazie
        print(f"Kontakt z tym emailem ({email}) już istnieje w bazie.")
    else:
        # Dodanie nowego kontaktu do bazy
        cursor.execute("INSERT INTO kontakty (imie, email, firma) VALUES (?, ?, ?)", (imie, email, firma))
        conn.commit()
        print(f"Kontakt {imie} <{email}> został dodany do bazy.")

    # Zamknięcie połączenia z bazą danych
    conn.close()

# Przykładowe dodanie kontaktów
# Możesz je zmieniać lub dodać interaktywnie
dodaj_kontakt("ABC", "firma@example.com", "firma")
