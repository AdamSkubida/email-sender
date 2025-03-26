import os
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

FROM_EMAIL = os.getenv("EMAIL_ADRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")


# Funkcja do nawiązywania połączenia z bazą danych
def connect_db():
    conn = sqlite3.connect('companies_data.db')
    return conn

# Funkcja do wysyłania e-maila
def send_email(to_email, to_name):
    subject = "Cześć, mam pytanie o Twoje studio detailingowe..."

    # Odczytujemy treść wiadomości z pliku
    with open("mail.txt", "r", encoding="utf-8") as file:
        body = file.read()

    # Zastępujemy {imie} w treści wiadomości na imię odbiorcy
    body = body.format(imie=to_name)

    # Tworzymy wiadomość e-mail
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        # Konfiguracja serwera SMTP (dla Gmaila)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Używamy szyfrowania
        server.login(FROM_EMAIL, PASSWORD)
        server.sendmail(FROM_EMAIL, to_email, msg.as_string())
        server.quit()
        print(f'Email wysłany do {to_name} ({to_email})')
    except Exception as e:
        print(f'Błąd podczas wysyłania e-maila: {e}')

# Funkcja do zaktualizowania bazy danych po wysłaniu e-maila
def update_sent_status(email):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE kontakty SET wyslano = 1 WHERE email = ?", (email,))
    conn.commit()
    conn.close()

# Funkcja do wysyłania wiadomości do osób, którym jeszcze nie wysłano
def send_emails():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT imie, email FROM kontakty WHERE wyslano = 0")  # Wybieramy osoby, którym jeszcze nie wysłaliśmy e-maila
    rows = cursor.fetchall()

    for row in rows:
        imie, email = row
        send_email(email, imie)  # Wysyłamy e-mail
        update_sent_status(email)  # Zmieniamy status w bazie danych na wysłano

    conn.close()

# Uruchomienie wysyłania e-maili
if __name__ == "__main__":
    send_emails()
