import unittest
from protocol_analyzer.analyze import load_records
from pathlib import Path
import tempfile

class TestRecordLoader(unittest.TestCase):
    def test_missing_file_returns_empty_list(self):
        self.assertEqual(load_records(Path("this_file_does_not_exist.jsonl")), [])

    def test_reads_valid_json_lines_and_skips_invalid_lines(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "packets.jsonl"
            path.write_text('{"protocol":"TCP"}\nnot-json\n{"dst_port":8000}\n', encoding="utf-8")
            records = load_records(path)
            self.assertEqual(len(records), 2)
            self.assertEqual(records[0]["protocol"], "TCP")
            self.assertEqual(records[1]["dst_port"], 8000)

if __name__ == "__main__":
    unittest.main()
