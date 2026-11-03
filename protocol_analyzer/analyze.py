"""Summarize captured packet metadata and optionally request an LLM explanation."""
import argparse
import json
from collections import Counter
from pathlib import Path
from dotenv import load_dotenv
from .llm_analyzer import explain_with_llm

def load_records(path):
    records = []
    if not path.exists():
        return records
    with path.open(encoding="utf-8") as file:
        for line in file:
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default="data/captured_packets.jsonl")
    args = parser.parse_args()
    load_dotenv()
    records = load_records(Path(args.file))
    if not records:
        print("No records found. Start capture, generate lab traffic, then stop capture.")
        return

    print(f"\nTotal captured TCP packet records: {len(records)}")
    print("Destination ports:", dict(Counter(str(r.get("dst_port")) for r in records)))
    http = [r for r in records if r.get("http_method") or r.get("http_status_line")]
    print(f"HTTP-indicator records: {len(http)}")

    print("\nFirst 20 packet summaries:")
    for record in records[:20]:
        print(
            f'{record.get("src_ip")}:{record.get("src_port")} -> '
            f'{record.get("dst_ip")}:{record.get("dst_port")} | '
            f'flags={record.get("tcp_flags")} | bytes={record.get("payload_bytes")} | '
            f'HTTP={record.get("http_method") or record.get("http_status_line") or "-"}'
        )

    print("\nLLM explanation:")
    print(explain_with_llm(records))

if __name__ == "__main__":
    main()
