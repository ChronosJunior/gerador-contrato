from src.email import connect_smtp_server
import os
from dotenv import load_dotenv 

def test_connect_smtp_server():
    load_dotenv()
    config = {
        "smtp_server": os.getenv("SMTP_SERVER"),
        "port": int(os.getenv("SMTP_PORT")),
        "sender_email": os.getenv("SENDER_EMAIL"),
        "sender_pass": os.getenv("SENDER_PASS")
    }
    print(config)
    server = connect_smtp_server(**config)
    
    status, message = server.noop()
    
    try:
        assert status == 250
    finally:
        server.quit() 