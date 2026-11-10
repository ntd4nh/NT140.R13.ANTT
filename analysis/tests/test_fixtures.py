import json
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_DIR = Path(__file__).parent / "fixtures" / "minh_hoa_RUN-TEST"


def test_cowrie_fixture_counts_and_raw_directory():
    log_files = sorted(FIXTURE_DIR.glob("cowrie.json*"))
    assert len(log_files) == 2

    valid_lines = []
    malformed_lines = 0
    blank_lines = 0
    for log_file in log_files:
        for line in log_file.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                blank_lines += 1
                continue
            try:
                json.loads(line)
            except json.JSONDecodeError:
                malformed_lines += 1
            else:
                valid_lines.append(line)

    duplicate_excess = sum(count - 1 for count in Counter(valid_lines).values())
    assert len(valid_lines) == 48
    assert malformed_lines == 1
    assert blank_lines == 1
    assert duplicate_excess == 1

    raw_dir = PROJECT_ROOT / "data" / "raw"
    raw_files = [
        path for path in raw_dir.rglob("*")
        if path.is_file() and path.name != ".gitkeep"
    ]
    assert raw_files == []
