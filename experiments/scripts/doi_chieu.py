#!/usr/bin/env python3
"""Lập bảng đối chiếu bước nhật ký H.2 ↔ sự kiện Cowrie cho một lượt chạy (WP-06).

Người viết: TV4 (có AI hỗ trợ), 2026-11-11.
Đã thử trên log smoke test với nhật ký thử dựng trong thư mục tạm; CHƯA chạy trên RUN thật.

Đọc thẳng log gốc (``cowrie.json*``), không dùng mã trong analysis/, chỉ đọc file.
Nhãn thao_tac theo experiments/quy_uoc_nhat_ky.md (BAT_DAU, MO_KET_NOI, GUI_USERNAME,
GUI_MAT_KHAU, GO_LENH, HUY_DAU_NHAC, CLIENT_TU_NGAT, KET_THUC).

    python -I experiments/scripts/doi_chieu.py --run-dir data/raw/RUN-01 \
        --logbook experiments/nhat_ky_thu_nghiem.csv --out experiments/doi_chieu_RUN-01.csv \
        --transcript-dir experiments/transcript/RUN-01

Cách ghép:
- Mỗi bộ (scenario_id, ip_nguon, cổng) có một cửa sổ [dòng sớm nhất − |δ|, dòng muộn nhất + |δ|],
  δ lấy từ clock_offset_s trong run_note.txt (hoặc --delta-seconds). Phiên ứng viên: cùng src_ip,
  cùng dst_port, thời gian giao cửa sổ. Phiên nằm trong cửa sổ của hai kịch bản bị ghi mo_ho.
- Mỗi MO_KET_NOI lấy phiên ứng viên kế tiếp theo giờ bắt đầu; các bước sau dùng phiên đó.
- Một bước có thể ứng với nhiều sự kiện: mỗi sự kiện một dòng.
- Sự kiện phân tích không ứng với bước nào, và phiên ngoài mọi cửa sổ, được ghi khong_khop.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

COT_RA = [
    "run_id", "scenario_id", "step_no", "thao_tac", "ip_nguon", "dich_vu_cong", "time_utc_client",
    "session_id", "eventid", "event_time_utc", "lech_giay", "raw_ref", "trang_thai", "giai_thich",
    "transcript_ref",
]
PHU = {"cowrie.telnet.option", "cowrie.client.size", "cowrie.client.var", "cowrie.session.params"}
LOGIN = {"cowrie.login.failed", "cowrie.login.success"}
NHAN = re.compile(r"^([A-Z_]+)(?::\s*(.*))?$")


def gio(chuoi: str) -> datetime:
    t = datetime.fromisoformat(chuoi.strip().replace("Z", "+00:00"))
    return t if t.tzinfo else t.replace(tzinfo=timezone.utc)  # không ghi múi giờ thì coi là UTC


def doc_log(run_dir: Path) -> list[dict]:
    files = sorted(p for p in run_dir.glob("cowrie.json*") if p.is_file() and p.name != "cowrie.json")
    if (run_dir / "cowrie.json").is_file():
        files.append(run_dir / "cowrie.json")
    if not files:
        raise SystemExit(f"{run_dir}: không có cowrie.json*")
    ev = []
    for thu_tu, f in enumerate(files):
        for so, dong in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if not dong.strip():
                continue
            try:
                e = json.loads(dong)
            except json.JSONDecodeError:
                print(f"CẢNH BÁO: JSON hỏng {f.name}:{so}")
                continue
            e["_ref"], e["_t"], e["_k"] = f"{f.name}:{so}", gio(e["timestamp"]), (thu_tu, so)
            ev.append(e)
    return ev


def doc_delta(run_dir: Path, ghi_de: float | None) -> float:
    if ghi_de is not None:
        return ghi_de
    note = run_dir / "run_note.txt"
    m = re.search(r"clock_offset_s\s*=\s*([+-]?\d+(?:\.\d*)?)", note.read_text(encoding="utf-8")) if note.is_file() else None
    if not m:
        raise SystemExit("Thiếu clock_offset_s trong run_note.txt; dùng --delta-seconds nếu cần")
    return float(m.group(1))


def cong(dich_vu: str) -> int:
    m = re.search(r"(\d+)\s*$", dich_vu or "")
    return int(m.group(1)) if m else -1


def main() -> int:
    for luong in (sys.stdout, sys.stderr):
        luong.reconfigure(encoding="utf-8")  # console Windows mặc định cp1252
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run-dir", required=True, type=Path)
    ap.add_argument("--logbook", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--transcript-dir", type=Path)
    ap.add_argument("--delta-seconds", type=float)
    args = ap.parse_args()
    if "raw" in args.out.resolve().parts:
        ap.error("không ghi đầu ra vào data/raw/")
    run_id = args.run_dir.resolve().name
    tol = abs(doc_delta(args.run_dir, args.delta_seconds))

    # Phiên trong log.
    phien: dict[str, dict] = {}
    for e in sorted(doc_log(args.run_dir), key=lambda e: (e["_t"], e["_k"])):
        p = phien.setdefault(e.get("session", ""), {"id": e.get("session", ""), "ip": e.get("src_ip", ""),
                                                     "port": e.get("dst_port"), "ev": []})
        p["ev"].append(e)
    for p in phien.values():
        p["start"], p["end"] = p["ev"][0]["_t"], p["ev"][-1]["_t"]

    # Nhật ký, theo bộ (kịch bản, ip, cổng).
    with args.logbook.open(encoding="utf-8-sig", newline="") as f:
        dong_nk = [r for r in csv.DictReader(f) if r["run_id"] == run_id]
    nhom: dict[tuple, list[dict]] = defaultdict(list)
    for r in dong_nk:
        r["_t"] = gio(r["time_utc_client"])
        nhom[(r["scenario_id"], r["ip_nguon"], cong(r["dich_vu_cong"]))].append(r)
    cua_so = {k: (min(r["_t"] for r in v) - timedelta(seconds=tol), max(r["_t"] for r in v) + timedelta(seconds=tol))
              for k, v in nhom.items()}

    def trong(p: dict, k: tuple) -> bool:
        a, b = cua_so[k]
        return p["ip"] == k[1] and p["port"] == k[2] and p["start"] <= b and p["end"] >= a

    ra: list[dict] = []
    dung: set[str] = set()
    da_gan: set[str] = set()

    def them(r: dict | None, k: tuple, sid: str, e: dict | None, tt: str, gt: str) -> None:
        tr = ""
        if r is not None and args.transcript_dir:
            ung_vien = args.transcript_dir / f"{k[0]}_{r['may_nguon']}.txt"
            tr = ung_vien.as_posix() if ung_vien.exists() else ""
        ra.append({
            "run_id": run_id, "scenario_id": k[0], "step_no": r["step_no"] if r else "",
            "thao_tac": r["thao_tac"] if r else "", "ip_nguon": k[1],
            "dich_vu_cong": r["dich_vu_cong"] if r else "", "time_utc_client": r["time_utc_client"] if r else "",
            "session_id": sid, "eventid": e["eventid"] if e else "",
            "event_time_utc": e["timestamp"] if e else "",
            "lech_giay": f"{(e['_t'] - r['_t']).total_seconds():+.3f}" if (e and r) else "",
            "raw_ref": e["_ref"] if e else "", "trang_thai": tt, "giai_thich": gt, "transcript_ref": tr,
        })
        if e is not None and tt in ("khop", "khong_co_su_kien_rieng"):
            dung.add(e["_ref"])

    def ke_tiep(p: dict | None, loai: set[str]) -> dict | None:
        if p is None:
            return None
        return next((e for e in p["ev"] if e["eventid"] in loai and e["_ref"] not in dung), None)

    for k in sorted(nhom, key=lambda k: min(r["_t"] for r in nhom[k])):
        rows = sorted(nhom[k], key=lambda r: (int(r["step_no"]), r["_t"]))
        ung = sorted((p for p in phien.values() if trong(p, k)), key=lambda p: p["start"])
        hang_doi = list(ung)
        cur: dict | None = None
        for r in rows:
            m = NHAN.match(r["thao_tac"].strip())
            nhan, ct = (m.group(1), (m.group(2) or "").strip()) if m else ("", "")
            sid = cur["id"] if cur else ""
            if nhan in ("BAT_DAU", "KET_THUC"):
                them(r, k, "", None, "khong_co_su_kien_rieng", "dòng mốc của nhật ký")
            elif nhan == "MO_KET_NOI":
                if not hang_doi:
                    them(r, k, "", None, "khong_khop", "không còn phiên nào cùng nguồn, cùng cổng trong cửa sổ")
                    cur = None
                    continue
                cur = hang_doi.pop(0)
                da_gan.add(cur["id"])
                khac = [kk[0] for kk in cua_so if kk != k and trong(cur, kk)]
                tt = "mo_ho" if khac else "khop"
                gt = f"phiên cũng nằm trong cửa sổ {khac}" if khac else "phiên kế tiếp trong cửa sổ"
                for loai in ("cowrie.session.connect", "cowrie.client.version", "cowrie.client.kex"):
                    e = ke_tiep(cur, {loai})
                    if e:
                        them(r, k, cur["id"], e, tt, gt)
            elif nhan == "GUI_USERNAME":
                e = ke_tiep(cur, LOGIN)
                gt = (f"gửi username không sinh sự kiện riêng; username={e.get('username')!r} nằm trong {e['eventid']} kế tiếp"
                      if e else "gửi username không sinh sự kiện riêng; không thấy sự kiện đăng nhập kế tiếp")
                them(r, k, sid, None, "khong_co_su_kien_rieng" if e else "khong_khop", gt)
                if e:
                    ra[-1]["raw_ref"], ra[-1]["eventid"] = e["_ref"], e["eventid"]
            elif nhan == "GUI_MAT_KHAU":
                e = ke_tiep(cur, LOGIN)
                if e is None:
                    them(r, k, sid, None, "khong_khop", "không có sự kiện đăng nhập tương ứng")
                elif e.get("password") == ct:
                    them(r, k, sid, e, "khop", f"username={e.get('username')}, password khớp chuỗi đã gửi")
                else:
                    them(r, k, sid, e, "khong_khop", "password trong log khác chuỗi đã gửi")
            elif nhan == "GO_LENH":
                e = ke_tiep(cur, {"cowrie.command.input"})
                if e is None:
                    them(r, k, sid, None, "khong_khop", "không có command.input tương ứng")
                    continue
                them(r, k, sid, e, "khop" if e.get("input") == ct else "khong_khop",
                     "input khớp lệnh đã gõ" if e.get("input") == ct else f"input trong log là {e.get('input')!r}")
                f = ke_tiep(cur, {"cowrie.command.failed"})
                if f and f.get("input") == ct:
                    them(r, k, sid, f, "khop", "shell giả báo lệnh không được hỗ trợ")
                if ct == "exit":
                    for loai in ("cowrie.log.closed", "cowrie.session.closed"):
                        e2 = ke_tiep(cur, {loai})
                        if e2:
                            them(r, k, sid, e2, "khop", "đóng phiên sau exit")
            elif nhan == "HUY_DAU_NHAC":
                so_login = sum(e["eventid"] in LOGIN for e in cur["ev"]) if cur else -1
                e = ke_tiep(cur, {"cowrie.session.closed"})
                if cur and so_login == 0:
                    them(r, k, sid, e, "khong_co_su_kien_rieng",
                         "hủy không sinh sự kiện riêng; phiên không có cowrie.login.*; đối chiếu bằng session.closed")
                else:
                    them(r, k, sid, e, "khong_khop", f"phiên có {so_login} sự kiện đăng nhập")
            elif nhan == "CLIENT_TU_NGAT":
                e = ke_tiep(cur, {"cowrie.session.closed"})
                them(r, k, sid, e, "khop" if e else "khong_khop",
                     "phiên đóng sau khi client thoát" if e else "không thấy session.closed")
            else:
                them(r, k, sid, None, "mo_ho", f"không nhận ra nhãn thao_tac {r['thao_tac']!r}")
        # Sự kiện phân tích còn lại trong các phiên đã gán cho bộ này.
        for p in ung:
            if p["id"] not in da_gan:
                continue
            for e in p["ev"]:
                if e["_ref"] not in dung and e["eventid"] not in PHU:
                    them(None, k, p["id"], e, "khong_khop", "sự kiện không ứng với bước nào trong nhật ký")

    for p in sorted(phien.values(), key=lambda p: p["start"]):
        if p["id"] not in da_gan:
            e = p["ev"][0]
            them(None, ("", p["ip"], p["port"]), p["id"], e, "khong_khop",
                 "phiên không được bước MO_KET_NOI nào nhận (ngoài cửa sổ, hoặc thừa)")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COT_RA, lineterminator="\n")
        w.writeheader()
        w.writerows(ra)
    dem = defaultdict(int)
    for x in ra:
        dem[x["trang_thai"]] += 1
    phu = sum(e["eventid"] in PHU for p in phien.values() for e in p["ev"])
    print(f"run_id={run_id}; |δ|={tol}s; phiên trong log={len(phien)}; dòng nhật ký={len(dong_nk)}")
    print("Dòng đối chiếu theo trạng thái: " + ", ".join(f"{k}={v}" for k, v in sorted(dem.items())))
    print(f"Sự kiện phụ không đưa vào bảng (telnet.option, client.size/var, session.params): {phu}")
    print(f"Đã ghi {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
