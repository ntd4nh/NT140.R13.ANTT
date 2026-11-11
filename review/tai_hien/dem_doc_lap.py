"""Phép đếm độc lập của TV3 (WP-09): đếm thẳng từ cowrie.json, không dùng mã của analysis/.

Chạy:
    python -I review/tai_hien/dem_doc_lap.py <thư mục lượt chạy> [<thư mục đầu ra của analysis>]

Chỉ dùng thư viện chuẩn và chỉ đọc file. Nếu có thư mục đầu ra, so từng phiên trong
sessions.csv và từng dòng trong events.csv với số đếm độc lập; in "KHỚP" hoặc danh sách lệch.
"""

import collections
import csv
import json
import sys
from pathlib import Path


def doc_log(run_dir: Path) -> list[dict]:
    # File xoay vòng (cowrie.json.<hậu tố>) trước, cowrie.json hiện tại sau.
    files = sorted(p for p in run_dir.glob("cowrie.json*") if p.name != "cowrie.json")
    if (run_dir / "cowrie.json").is_file():
        files.append(run_dir / "cowrie.json")
    rows = []
    for f in files:
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                print(f"JSON hỏng: {f.name}:{i}")
                continue
            r["_ref"] = f"{f.name}:{i}"
            rows.append(r)
    return rows


def dem_phien(rows: list[dict]) -> dict[str, dict]:
    sess: dict[str, dict] = collections.OrderedDict()
    for r in rows:
        s = sess.setdefault(r.get("session", ""), {
            "src_ip": r.get("src_ip", ""), "protocol": r.get("protocol", ""),
            "n_events": 0, "n_login_failed": 0, "n_login_success": 0,
            "commands": [], "duration_ms": "",
        })
        s["n_events"] += 1
        e = r.get("eventid")
        if e == "cowrie.login.failed":
            s["n_login_failed"] += 1
        elif e == "cowrie.login.success":
            s["n_login_success"] += 1
        elif e == "cowrie.command.input":
            s["commands"].append(r.get("input", ""))
        elif e == "cowrie.session.closed":
            s["duration_ms"] = r.get("duration_ms", "")
    return sess


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows mặc định cp1252
    run_dir = Path(sys.argv[1])
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    rows = doc_log(run_dir)
    sess = dem_phien(rows)
    dem = collections.Counter(r.get("eventid") for r in rows)

    print(f"Sự kiện (dòng JSON hợp lệ): {len(rows)}")
    print(f"Phiên (session khác nhau): {len(sess)}")
    print(f"Lần đăng nhập: thất bại {dem['cowrie.login.failed']}, thành công {dem['cowrie.login.success']}")
    print(f"Lệnh (command.input): {dem['cowrie.command.input']}, lệnh không hỗ trợ (command.failed): {dem['cowrie.command.failed']}")
    for k, v in sorted(dem.items()):
        print(f"  {k}: {v}")
    if out_dir is None:
        return 0

    lech = []
    events = list(csv.DictReader((out_dir / "events.csv").open(encoding="utf-8")))
    by_ref = {e["raw_ref"]: e for e in events}
    for r in rows:
        e = by_ref.get(r["_ref"])
        if e is None:
            lech.append(f"events.csv thiếu {r['_ref']} ({r.get('eventid')})")
        elif e["event_type"] != r.get("eventid") or e["session_id"] != r.get("session", ""):
            lech.append(f"events.csv sai nội dung tại {r['_ref']}")
    sessions = {s["session_id"]: s for s in csv.DictReader((out_dir / "sessions.csv").open(encoding="utf-8"))}
    for sid, s in sess.items():
        o = sessions.get(sid)
        if o is None:
            lech.append(f"sessions.csv thiếu phiên {sid}")
            continue
        for k in ("src_ip", "protocol", "n_events", "n_login_failed", "n_login_success", "duration_ms"):
            if str(o[k]) != str(s[k]):
                lech.append(f"{sid}.{k}: analysis={o[k]} đếm độc lập={s[k]}")
        if json.loads(o["commands"]) != s["commands"]:
            lech.append(f"{sid}.commands: analysis={o['commands']} đếm độc lập={s['commands']}")
    print(f"events.csv: {len(events)} dòng; sessions.csv: {len(sessions)} phiên")
    print("KHỚP" if not lech else "LỆCH:\n  " + "\n  ".join(lech))
    return 0 if not lech else 1


if __name__ == "__main__":
    sys.exit(main())
