import smtplib
import os

def connect_smtp_server():
    return

def send_email(addressee, message):
    try:
        server = connect_smtp_server()
        server.sendmail(os.getenv("SENDER_EMAIL"), addressee, message)
        return True 
    except Exception:
        return False