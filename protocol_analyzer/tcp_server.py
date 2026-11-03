"""TCP socket server for the local two-process demonstration."""
import json
import socket

HOST = "127.0.0.1"
PORT = 9000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"TCP server listening on {HOST}:{PORT}")
        try:
            while True:
                conn, address = server.accept()
                with conn:
                    print(f"Connected by {address}")
                    buffer = b""
                    while True:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        buffer += chunk
                        while b"\n" in buffer:
                            line, buffer = buffer.split(b"\n", 1)
                            try:
                                message = json.loads(line.decode("utf-8"))
                            except (UnicodeDecodeError, json.JSONDecodeError):
                                message = {"raw": line.decode("utf-8", errors="replace")}
                            print("Received:", message)
                            response = {"status": "received", "message_type": message.get("type", "unknown")}
                            conn.sendall((json.dumps(response) + "\n").encode("utf-8"))
        except KeyboardInterrupt:
            print("\nStopping TCP server.")

if __name__ == "__main__":
    main()
