from src.email import connect_smtp_server, send_email
import os
from dotenv import load_dotenv 
import pytest

@pytest.fixture
def smtp_server():
    load_dotenv()
    config = {
        "smtp_server": os.getenv("SMTP_SERVER"),
        "port": int(os.getenv("SMTP_PORT")),
        "sender_email": os.getenv("SENDER_EMAIL"),
        "sender_pass": os.getenv("SENDER_PASS")
    }
    server = connect_smtp_server(**config)
    yield server

def test_connection_is_active(smtp_server):
    status, _ = smtp_server.noop()
    assert status == 250
    
def test_send_email_integration(smtp_server):
    sender = os.getenv("SENDER_EMAIL")
    assert send_email([sender], "Subject: Teste\n\nCorpo do email", smtp_server)