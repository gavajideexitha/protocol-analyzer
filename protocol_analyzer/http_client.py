"""Sends a harmless local HTTP GET request."""
from urllib.request import urlopen

def main():
    with urlopen("http://127.0.0.1:8000/lab-status", timeout=5) as response:
        print("HTTP status:", response.status)
        print("Response:", response.read().decode("utf-8"))

if __name__ == "__main__":
    main()
