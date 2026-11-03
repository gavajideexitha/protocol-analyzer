"""Capture only the project's local demonstration ports and write JSONL metadata."""
import argparse
import json
from pathlib import Path
from scapy.all import sniff
from .packet_parser import parse_packet

OUTPUT = Path("data/captured_packets.jsonl")
BPF_FILTER = "tcp and (port 9000 or port 8000)"

def main():
    parser = argparse.ArgumentParser(description="Capture local protocol-analyzer lab traffic.")
    parser.add_argument("--iface", help="Network interface name; omit to use Scapy's default.")
    args = parser.parse_args()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    print(f"Capturing TCP traffic matching: {BPF_FILTER}")
    print(f"Writing packet metadata to: {OUTPUT}")
    print("Start the TCP/HTTP demos in other terminals. Press Ctrl+C to stop.")
    def handle(packet):
        record = parse_packet(packet)
        if record is None:
            return
        with OUTPUT.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record) + "\n")
        print(
            f'{record["src_ip"]}:{record["src_port"]} -> '
            f'{record["dst_ip"]}:{record["dst_port"]} '
            f'flags={record["tcp_flags"]} bytes={record["payload_bytes"]}'
        )
    try:
        sniff(iface=args.iface, filter=BPF_FILTER, prn=handle, store=False)
    except KeyboardInterrupt:
        print("\nCapture stopped.")
    except Exception as exc:
        print(f"Capture error: {exc}")
        print("Check capture permissions, Npcap/libpcap, and the interface name.")

if __name__ == "__main__":
    main()
