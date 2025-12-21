from src.email import send_email

class mock_server():
    @staticmethod
    def sendmail(from_addr, to_addrs, msg):
        return "Email enviado com sucesso."

def test_send_email(monkeypatch):
    def mock_smtp():
        return mock_server()

    monkeypatch.setattr("src.email.connect_smtp_server", mock_smtp)
    addressee, message = "teste@gmail.com", "Contrato de fulano gerado."
    assert send_email(addressee, message)