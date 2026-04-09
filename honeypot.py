import socket
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("honeypot.log"),
        logging.StreamHandler()
    ]
)

IP_ADDRESS = '0.0.0.0'
PORT = 80


def start_honeypot():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((IP_ADDRESS, PORT))
        server.listen(5)

        logging.info(f"Honeypot started on port {PORT}")

        while True:
            client_socket, client_address = server.accept()

            logging.warning(f"INTRUSION ATTEMPT: {client_address[0]}:{client_address[1]}")

            # Zmień tę linię w swoim skrypcie:
            fake_banner = ("HTTP/1.1 200 OK\r\n"
                           "Server: Honeypot-Systemd-Verified\r\n"
                           "Content-Type: text/html\r\n\r\n"
                           "<html>"
                           "<body>"
                           "<h1>Security Monitor</h1>"
                           "<p>Automatic Deployment Successful.</p>"
                           "</body>"
                           "</html>")
            client_socket.send(fake_banner.encode('utf-8'))
            client_socket.close()

    except PermissionError:
        logging.error("Insufficient privileges. Use 'sudo'.")
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        server.close()


if __name__ == "__main__":
    start_honeypot()