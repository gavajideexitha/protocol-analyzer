# Protocol Analyzer (Python + TCP Sockets + Scapy + LangChain)

A local, educational protocol analyzer. It demonstrates:
- communication between two separate Python processes using TCP sockets;
- packet capture of the project's own TCP and HTTP test traffic using Scapy;
- extraction of packet metadata and basic HTTP request details;
- optional LLM explanations through LangChain and an OpenAI-compatible API.

## Safety and scope
Run this only on your own computer and against the included local test services. The capture filter is restricted to TCP ports 9000 and 8000. Do not capture networks or traffic you do not own or have permission to inspect. HTTPS/TLS payloads are encrypted; this project does not decrypt them. The HTTP demo uses harmless local test data and does not send passwords or tokens.

## 1. Requirements
- Python 3.10 or newer
- Windows, macOS, or Linux
- Administrator/root permission may be required for packet capture.
- On Windows, install Npcap (enable loopback capture if you want to capture localhost traffic).
- On Linux, install libpcap if Scapy reports that a capture backend is missing.

## 2. Create and activate a virtual environment

### Windows PowerShell
```powershell
py -3 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Configure optional LLM access
Copy `.env.example` to `.env`, then add your API key and model name. Keep `.env` private and never commit it to Git.

```text
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
```

The core project works without an API key. The LLM feature is optional and requires internet access and a valid provider key.

## 4. Run the TCP socket demonstration
Open two terminals in this project directory. Activate the virtual environment in both.

Terminal 1:
```bash
python -m protocol_analyzer.tcp_server
```

Terminal 2:
```bash
python -m protocol_analyzer.tcp_client
```

The client sends three JSON messages to the server. The server prints each message and returns an acknowledgement. Stop the server with Ctrl+C.

## 5. Run the HTTP demonstration
Terminal 1:
```bash
python -m protocol_analyzer.http_server
```

Terminal 2:
```bash
python -m protocol_analyzer.http_client
```

The client sends a harmless HTTP GET request to `127.0.0.1:8000`.

## 6. Capture the lab traffic
Start the capture in a terminal with the permissions required by your operating system:

```bash
python -m protocol_analyzer.capture
```

While capture is running, repeat steps 4 and 5 in other terminals. Press Ctrl+C in the capture terminal to stop. Captured packet metadata is appended to `data/captured_packets.jsonl`.

If your OS does not capture loopback traffic by default, choose the correct loopback interface:
```bash
python -m protocol_analyzer.capture --iface "INTERFACE_NAME"
```
List interfaces:
```bash
python -c "from scapy.all import get_if_list; print('\\n'.join(get_if_list()))"
```
On Windows, run the terminal as Administrator and select the Npcap Loopback Adapter if necessary. On Linux, run the capture command with sudo, using the Python interpreter from your virtual environment if needed.

## 7. Analyze captured packets
```bash
python -m protocol_analyzer.analyze
```
This prints packet counts, TCP metadata, and any detected HTTP request lines. If `.env` contains a valid API key and the optional packages are installed, it also asks the LLM for a concise explanation.

To analyze a different file:
```bash
python -m protocol_analyzer.analyze --file data/captured_packets.jsonl
```

## 8. Run tests
```bash
python -m unittest discover -s tests -v
```

## 9. Project structure
```text
protocol_analyzer_project/
├── protocol_analyzer/
│   ├── __init__.py
│   ├── tcp_server.py
│   ├── tcp_client.py
│   ├── http_server.py
│   ├── http_client.py
│   ├── capture.py
│   ├── packet_parser.py
│   ├── analyze.py
│   └── llm_analyzer.py
├── tests/
│   └── test_packet_parser.py
├── data/
│   └── .gitkeep
├── .env.example
├── .gitignore
└── requirements.txt
```

## 10. What to explain in your project review
1. TCP is connection-oriented and provides reliable, ordered byte-stream delivery.
2. A socket is an endpoint identified by an IP address and port.
3. The server binds, listens, accepts a connection, receives data, and responds.
4. Scapy observes packets at the network interface; it is separate from the application socket code.
5. HTTP is an application-layer protocol that commonly runs over TCP. This demo uses plain HTTP on localhost so the request line and headers can be inspected.
6. The parser extracts metadata and only a limited HTTP request line/Host header. It does not collect full payloads.
7. LangChain sends a compact, redacted summary to an LLM. The LLM provides explanations, not authoritative security verdicts.

## Troubleshooting
- `ModuleNotFoundError`: activate the virtual environment and run `pip install -r requirements.txt`.
- `PermissionError` / capture fails: run with the required privileges and check Npcap/libpcap installation.
- No packets appear: confirm capture is running before the clients, use the correct loopback interface, and check that ports 9000/8000 are not changed.
- Port already in use: stop the earlier server process or change the port consistently in the server, client, and capture filter.
- LLM skipped: this is normal without a configured API key; packet parsing and reporting still work.
