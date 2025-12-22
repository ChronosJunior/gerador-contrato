import smtplib
import os
from dotenv import load_dotenv 

def connect_smtp_server(smtp_server, port, sender_email, sender_pass):
    try:
        mail_server = smtplib.SMTP(smtp_server, port)
        mail_server.starttls()
        mail_server.login(sender_email, sender_pass)
    except Exception:
        raise Exception
    return mail_server

def send_email(addressee, message):
    load_dotenv()
    config = {
        "smtp_server": os.getenv("SMTP_SERVER"),
        "port": int(os.getenv("SMTP_PORT", 587)),
        "sender_email": os.getenv("SENDER_EMAIL"),
        "sender_pass": os.getenv("SENDER_PASS")
    }
    
    try:
        server = connect_smtp_server(**config)
        server.sendmail(os.getenv("SENDER_EMAIL"), addressee, message)
        server.quit()
        return True 
    except Exception:
        return False