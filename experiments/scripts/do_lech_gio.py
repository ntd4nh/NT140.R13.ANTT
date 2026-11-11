#!/usr/bin/env python3
"""Đo lệch giờ của VM-A và VM-H so với máy host, trước hoặc sau một lượt chạy.

Người viết: TV4 (có AI hỗ trợ), 2026-11-11. TRẠNG THÁI: CHƯA CHẠY THỬ TRÊN LAB.

Chạy trên máy host chạy lab. Cần ssh quản trị vào VM không hỏi mật khẩu
(BatchMode=yes); script không nhận và không lưu mật khẩu. Không đổi giờ máy nào.

Mỗi lần đo: t0 = giờ UTC của host; chạy ``ssh labadmin@<IP> 'date -u +%s.%N'``;
t1 = giờ UTC của host. lệch = giờ VM − (t0+t1)/2; sai số ±(t1−t0)/2.
Lấy trung vị của 5 lần. δ(VM-A − VM-H) = lệch(VM-A) − lệch(VM-H).

    python experiments/scripts/do_lech_gio.py --run RUN-01 --nhan truoc
    python experiments/scripts/do_lech_gio.py --run RUN-01 --nhan sau

Ghi thêm (không ghi đè) vào experiments/<RUN>/do_lech_gio.md. Không đặt file này trong data/raw/.
"""

from __future__ import annotations

import argparse
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

MAY = {"VM-A": "192.168.239.10", "VM-H": "192.168.239.20"}


def do_mot_may(ssh: str, ip: str, lan: int) -> list[tuple[float, float, float]]:
    mau = []
    for _ in range(lan):
        t0 = time.time()
        r = subprocess.run(
            [ssh, "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", f"labadmin@{ip}", "date -u +%s.%N"],
            capture_output=True, text=True, timeout=30,
        )
        t1 = time.time()
        if r.returncode != 0:
            raise SystemExit(f"ssh tới {ip} lỗi (mã {r.returncode}): {r.stderr.strip()}")
        mau.append((t0, float(r.stdout.strip()), t1))
        time.sleep(0.5)
    return mau


def iso(t: float) -> str:
    return datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"


def main() -> int:
    for luong in (sys.stdout, sys.stderr):
        luong.reconfigure(encoding="utf-8")  # console Windows mặc định cp1252
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run", required=True)
    ap.add_argument("--nhan", required=True, choices=["truoc", "sau", "chuan-bi"])
    ap.add_argument("--lan", type=int, default=5)
    ap.add_argument("--ssh", default="ssh")
    ap.add_argument("--out", type=Path, default=None, help="mặc định experiments/<RUN>/do_lech_gio.md")
    args = ap.parse_args()
    out = args.out or Path("experiments") / args.run / "do_lech_gio.md"
    if "raw" in out.resolve().parts:
        ap.error("không ghi file đo giờ vào data/raw/")
    out.parent.mkdir(parents=True, exist_ok=True)

    dong = [f"\n## Đo {args.nhan} – bắt đầu {iso(time.time())}\n",
            f"Đồng hồ host: `time.time()`, độ phân giải báo cáo {time.get_clock_info('time').resolution} s.\n",
            "| Máy | Lần | t0 host (UTC) | Giờ VM (UTC) | t1 host (UTC) | Lệch VM − host (s) | Sai số ± (s) |",
            "| --- | --- | --- | --- | --- | --- | --- |"]
    trung_vi = {}
    for ten, ip in MAY.items():
        mau = do_mot_may(args.ssh, ip, args.lan)
        lech = []
        for i, (t0, vm, t1) in enumerate(mau, 1):
            l, e = vm - (t0 + t1) / 2, (t1 - t0) / 2
            lech.append((l, e))
            dong.append(f"| {ten} | {i} | {iso(t0)} | {iso(vm)} | {iso(t1)} | {l:+.4f} | {e:.4f} |")
        trung_vi[ten] = (statistics.median(x for x, _ in lech), max(e for _, e in lech))
    delta = trung_vi["VM-A"][0] - trung_vi["VM-H"][0]
    dong += [
        "",
        f"- Trung vị lệch VM-A − host: {trung_vi['VM-A'][0]:+.4f} s (sai số lớn nhất ±{trung_vi['VM-A'][1]:.4f} s)",
        f"- Trung vị lệch VM-H − host: {trung_vi['VM-H'][0]:+.4f} s (sai số lớn nhất ±{trung_vi['VM-H'][1]:.4f} s)",
        f"- Lệch host − VM-H: {-trung_vi['VM-H'][0]:+.4f} s",
        f"- **δ(VM-A − VM-H) = {delta:+.4f} s** (giá trị cho `run_note.txt` nếu là lần đo trước lượt)",
        "",
    ]
    with out.open("a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(dong) + "\n")
    print("\n".join(dong))
    return 0


if __name__ == "__main__":
    sys.exit(main())
