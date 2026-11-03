"""Tiny local HTTP server used only to generate inspectable HTTP test traffic."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({"service": "protocol-analyzer-lab", "result": "ok"}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print("HTTP:", fmt % args)

def main():
    server = HTTPServer(("127.0.0.1", 8000), Handler)
    print("HTTP demo server listening on http://127.0.0.1:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping HTTP server.")
    finally:
        server.server_close()

if __name__ == "__main__":
    main()
