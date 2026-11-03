"""TCP socket client; sends newline-delimited JSON messages."""
import json
import socket
import time

HOST = "127.0.0.1"
PORT = 9000

def main():
    messages = [
        {"type": "greeting", "text": "Hello from the client"},
        {"type": "network_test", "sequence": 2},
        {"type": "goodbye", "text": "End of socket test"},
    ]
    with socket.create_connection((HOST, PORT), timeout=5) as client:
        reader = client.makefile("rb")
        for message in messages:
            client.sendall((json.dumps(message) + "\n").encode("utf-8"))
            response = reader.readline()
            print("Server response:", response.decode("utf-8").strip())
            time.sleep(0.2)
        reader.close()

if __name__ == "__main__":
    main()
