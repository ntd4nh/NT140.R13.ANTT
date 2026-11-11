"""Giải mã file TTY của Cowrie thành chữ (WP-13): xem kẻ tấn công gõ gì và màn hình hiện gì.

Chạy:
    python -I review/tai_hien/doc_tty.py evidence/smoke_test/tty/<tên file>

Chỉ dùng thư viện chuẩn và chỉ đọc file. Mỗi bản ghi trong file TTY có phần đầu
"<iLiiLL" (thao tác, tty, độ dài, chiều, giây, micro giây), giống lệnh playlog của Cowrie.
"""

import struct
import sys
from pathlib import Path

HEADER = struct.Struct("<iLiiLL")
OP_WRITE = 3
CHIEU = {1: "GÕ VÀO", 2: "HIỆN RA"}


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows mặc định cp1252
    data = Path(sys.argv[1]).read_bytes()
    off = 0
    while off + HEADER.size <= len(data):
        op, _tty, length, chieu, _sec, _usec = HEADER.unpack_from(data, off)
        off += HEADER.size
        if op == OP_WRITE:
            noi_dung = data[off:off + length].decode("utf-8", errors="replace")
            print(f"{CHIEU.get(chieu, chieu)}: {noi_dung!r}")
            off += length
    return 0


if __name__ == "__main__":
    sys.exit(main())
