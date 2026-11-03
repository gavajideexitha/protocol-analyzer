"""Extract limited TCP/IP metadata and safe HTTP request indicators."""
from datetime import datetime, timezone

def parse_packet(packet):
    """Return a JSON-serializable summary; never store the full packet payload."""
    try:
        from scapy.layers.inet import IP, TCP
        from scapy.layers.inet6 import IPv6
    except ImportError as exc:
        raise RuntimeError("Scapy is required. Install requirements.txt") from exc

    if TCP not in packet:
        return None

    if IP in packet:
        src_ip, dst_ip = packet[IP].src, packet[IP].dst
    elif IPv6 in packet:
        src_ip, dst_ip = packet[IPv6].src, packet[IPv6].dst
    else:
        src_ip, dst_ip = "unknown", "unknown"

    tcp = packet[TCP]
    summary = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "src_port": int(tcp.sport),
        "dst_port": int(tcp.dport),
        "protocol": "TCP",
        "tcp_flags": str(tcp.flags),
        "payload_bytes": len(bytes(tcp.payload)),
        "http_method": None,
        "http_path": None,
        "http_host": None,
        "http_status_line": None,
    }

    # Inspect only the first line and Host header for plain HTTP lab traffic.
    payload = bytes(tcp.payload)
    first_line = payload.split(b"\r\n", 1)[0][:300]
    try:
        first_text = first_line.decode("ascii", errors="ignore")
    except Exception:
        first_text = ""

    parts = first_text.split()
    if len(parts) >= 3 and parts[0] in {"GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"}:
        summary["http_method"] = parts[0]
        summary["http_path"] = parts[1][:200]
        try:
            headers = payload.decode("iso-8859-1", errors="ignore").split("\r\n")
            for header in headers[1:30]:
                if header.lower().startswith("host:"):
                    summary["http_host"] = header.split(":", 1)[1].strip()[:200]
                    break
        except Exception:
            pass
    elif first_text.startswith("HTTP/"):
        summary["http_status_line"] = first_text[:200]

    return summary
