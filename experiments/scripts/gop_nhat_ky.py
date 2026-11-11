#!/usr/bin/env python3
"""Gộp nhật ký từng máy (nhat_ky_VM-A.csv, nhat_ky_Host.csv) vào experiments/nhat_ky_thu_nghiem.csv.

Người viết: TV4 (có AI hỗ trợ), 2026-11-11.

Chỉ THÊM dòng, không sửa hay xóa dòng đã có. Dừng nếu header sai, nếu có dòng mang
run_id khác, hoặc nếu file đích đã có dòng của run_id này (tránh gộp hai lần).

    python experiments/scripts/gop_nhat_ky.py --run RUN-01 <nhat_ky_VM-A.csv> <nhat_ky_Host.csv>
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

COT = [
    "run_id", "scenario_id", "step_no", "time_utc_client", "may_nguon", "ip_nguon",
    "dich_vu_cong", "thao_tac", "ket_qua_phia_client", "nguoi_thuc_hien", "ghi_chu",
]


def doc(path: Path) -> list[list[str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        dong = list(csv.reader(f))
    if not dong or dong[0] != COT:
        raise SystemExit(f"{path}: header không đúng 11 cột H.2")
    return dong[1:]


def main() -> int:
    for luong in (sys.stdout, sys.stderr):
        luong.reconfigure(encoding="utf-8")  # console Windows mặc định cp1252
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run", required=True)
    ap.add_argument("--dich", type=Path, default=Path("experiments/nhat_ky_thu_nghiem.csv"))
    ap.add_argument("nguon", nargs="+", type=Path)
    args = ap.parse_args()

    moi: list[list[str]] = []
    for p in args.nguon:
        for d in doc(p):
            if d[0] != args.run:
                raise SystemExit(f"{p}: có dòng run_id={d[0]!r}, khác {args.run}")
            moi.append(d)
    moi.sort(key=lambda d: (d[3], d[4], int(d[2])))
    if args.dich.exists():
        cu = doc(args.dich)
        if any(d[0] == args.run for d in cu):
            raise SystemExit(f"{args.dich} đã có dòng của {args.run}; không gộp lần hai")
    with args.dich.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        if f.tell() == 0:
            w.writerow(COT)
        w.writerows(moi)
    print(f"Đã thêm {len(moi)} dòng của {args.run} vào {args.dich}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
