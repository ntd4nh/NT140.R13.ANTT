#!/usr/bin/env python3
"""Chạy KB-05 (Telnet) và KB-01 lặp lại (SSH) từ máy host Windows vào honeypot.

Người viết: TV4 (có AI hỗ trợ), 2026-11-11.
TRẠNG THÁI: CHƯA CHẠY THỬ TRÊN LAB. Phải chạy phiên chuẩn bị (``--run CHUAN-BI``)
và đọc log Cowrie trước khi dùng cho một RUN thật.

Chỉ dùng thư viện chuẩn. Chỉ kết nối tới 192.168.239.20 cổng 2222/2223.
Mọi mật khẩu trong file là mật khẩu giả của lab.

- KB-05: Telnet bằng socket, tự xử lý byte IAC giống mặc định của telnetlib
  (từ chối mọi tùy chọn: DO/DONT → WONT, WILL/WONT → DONT), không cần telnetlib.
- KB-01: chạy ssh của Git for Windows với SSH_ASKPASS + SSH_ASKPASS_REQUIRE=force.
  Chương trình askpass KHÔNG trả mật khẩu: nó ghi dấu nhắc ra file rồi ngủ; script
  thấy file thì dừng ssh. Không để askpass thoát, vì askpass thoát lỗi có thể làm
  ssh gửi mật khẩu rỗng (docs/03_kich_ban_thu_nghiem.md, KB-01, rủi ro đã biết).

Cách chạy trong PowerShell hoặc Git Bash trên máy host chạy lab:

    python experiments/scripts/kb_host.py --run RUN-01 --kb KB-05 --out experiments/RUN-01/host
    python experiments/scripts/kb_host.py --run RUN-01 --kb KB-01 --out experiments/RUN-01/host

Đầu ra trong --out: nhat_ky_Host.csv (dòng nhật ký H.2), KB-05_Host.txt (byte nhận được,
đã bỏ byte điều khiển Telnet), KB-05_Host.raw (byte nhận được nguyên văn),
KB-01_Host.txt (stdout + stderr của ssh -v), KB-01_Host.askpass.txt (dấu nhắc ssh đưa cho askpass).
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HONEYPOT = "192.168.239.20"
MAY_NGUON = "Host"
IP_NGUON = "192.168.239.1"
NGUOI = "TV4 (AI hỗ trợ)"
COT = [
    "run_id", "scenario_id", "step_no", "time_utc_client", "may_nguon", "ip_nguon",
    "dich_vu_cong", "thao_tac", "ket_qua_phia_client", "nguoi_thuc_hien", "ghi_chu",
]
USER = "labuser"
# Mật khẩu giả của lab (docs/03_kich_ban_thu_nghiem.md, mục 0.2).
MK_KB05 = ["TelnetWrong-01", "TelnetWrong-02", "LabOnly-2026"]
GHI_CHU_MK = "mật khẩu giả của lab"
LENH_KB05 = ["whoami", "uname -a", "exit"]
SSH_MAC_DINH = "C:/Program Files/Git/usr/bin/ssh.exe"

IAC, DONT, DO, WONT, WILL, SB, SE = 255, 254, 253, 252, 251, 250, 240
MAU_LOGIN = re.compile(rb"login: *$")
MAU_MK = re.compile(rb"[Pp]assword: *$")
MAU_SHELL = re.compile(rb"[$#] $")
ANSI = re.compile(rb"\x1b\[[0-9;?]*[A-Za-z]")
BANNER = re.compile(rb"remote software version ([^\r\n]+)")


def gio_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def tom_tat(du_lieu: bytes, gioi_han: int = 150) -> str:
    chu = ANSI.sub(b"", du_lieu).decode("utf-8", errors="replace")
    dong = [d.strip() for d in chu.replace("\r", "\n").split("\n") if d.strip()]
    return dong[-1][:gioi_han] if dong else ""


def truoc_dau_nhac(buf: bytes, moc: int, m: re.Match[bytes]) -> bytes:
    doan = buf[moc:m.start()]
    cat = max(doan.rfind(b"\n"), doan.rfind(b"\r"))
    return doan[:cat] if cat >= 0 else b""


class NhatKy:
    def __init__(self, path: Path, run_id: str, kb: str, dich_vu: str) -> None:
        self.path, self.run_id, self.kb, self.dich_vu = path, run_id, kb, dich_vu

    def dong(self, step: int, gio: str, thao_tac: str, ket_qua: str = "", ghi_chu: str = "") -> None:
        moi = not self.path.exists() or self.path.stat().st_size == 0
        with self.path.open("a", encoding="utf-8", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            if moi:
                w.writerow(COT)
            w.writerow([self.run_id, self.kb, step, gio, MAY_NGUON, IP_NGUON,
                        self.dich_vu, thao_tac, ket_qua, NGUOI, ghi_chu])
        print(f"[{gio}] {self.kb} bước {step}: {thao_tac} -> {ket_qua}")


def bo_iac(data: bytes, trang_thai: dict) -> tuple[bytes, bytes]:
    """Tách byte điều khiển Telnet. Trả (dữ liệu chữ, byte cần gửi lại cho server)."""
    ra, tra_loi = bytearray(), bytearray()
    for b in data:
        tt = trang_thai["tt"]
        if tt == "du_lieu":
            if b == IAC:
                trang_thai["tt"] = "iac"
            else:
                ra.append(b)
        elif tt == "iac":
            if b == IAC:  # IAC IAC là byte 255 thật
                ra.append(b)
                trang_thai["tt"] = "du_lieu"
            elif b in (DO, DONT, WILL, WONT):
                trang_thai["lenh"] = b
                trang_thai["tt"] = "tuy_chon"
            elif b == SB:
                trang_thai["tt"] = "sb"
            else:
                trang_thai["tt"] = "du_lieu"
        elif tt == "tuy_chon":
            lenh = trang_thai["lenh"]
            tra_loi += bytes([IAC, WONT if lenh in (DO, DONT) else DONT, b])
            trang_thai["tt"] = "du_lieu"
        elif tt == "sb":
            if b == IAC:
                trang_thai["tt"] = "sb_iac"
        elif tt == "sb_iac":
            trang_thai["tt"] = "du_lieu" if b == SE else "sb"
    return bytes(ra), bytes(tra_loi)


class Telnet:
    def __init__(self, cong: int, txt: Path, raw: Path, eol: bytes) -> None:
        self.s = socket.create_connection((HONEYPOT, cong), timeout=10)
        self.s.settimeout(0.3)
        self.ftxt, self.fraw = txt.open("ab"), raw.open("ab")
        self.buf, self.pos, self.het, self.eol = b"", 0, False, eol
        self.tt = {"tt": "du_lieu", "lenh": None}

    def _doc(self) -> None:
        try:
            data = self.s.recv(4096)
        except socket.timeout:
            return
        except OSError:
            data = b""
        if not data:
            self.het = True
            return
        self.fraw.write(data)
        self.fraw.flush()
        chu, tra_loi = bo_iac(data, self.tt)
        if tra_loi:
            self.s.sendall(tra_loi)
        self.buf += chu
        self.ftxt.write(chu)
        self.ftxt.flush()

    def cho(self, mau: re.Pattern[bytes], han_s: float = 30.0, yen_s: float = 0.4) -> re.Match[bytes]:
        het_han = time.monotonic() + han_s
        while True:
            m = mau.search(self.buf, self.pos)
            if m and m.end() == len(self.buf):
                truoc = len(self.buf)
                time.sleep(yen_s)
                self._doc()
                if len(self.buf) == truoc:
                    self.pos = m.end()
                    return m
                continue
            if self.het:
                raise RuntimeError(f"server đã đóng khi chờ {mau.pattern!r}")
            if time.monotonic() > het_han:
                raise TimeoutError(f"quá {han_s}s khi chờ {mau.pattern!r}")
            self._doc()

    def cho_het(self, han_s: float = 30.0) -> None:
        het_han = time.monotonic() + han_s
        while not self.het:
            if time.monotonic() > het_han:
                raise TimeoutError(f"quá {han_s}s khi chờ server đóng")
            self._doc()

    def gui_dong(self, chu: str) -> None:
        self.s.sendall(chu.encode().replace(bytes([IAC]), bytes([IAC, IAC])) + self.eol)

    def dong(self) -> None:
        self.s.close()
        self.ftxt.close()
        self.fraw.close()


def buoc_telnet(nk: NhatKy, tn: Telnet, step: int, thao_tac: str, gui: str,
                mau: re.Pattern[bytes] | None, ghi_chu: str = "") -> None:
    moc = tn.pos
    gio = gio_utc()
    tn.gui_dong(gui)
    try:
        if mau is None:
            tn.cho_het()
            kq = tom_tat(tn.buf[moc:])
        else:
            m = tn.cho(mau)
            if mau is MAU_SHELL and thao_tac.startswith("GUI_MAT_KHAU"):
                kq = "thấy dấu nhắc shell: " + tom_tat(tn.buf[moc:m.end()])
            elif mau is MAU_MK:
                kq = "thấy Password:"
            else:
                kq = tom_tat(truoc_dau_nhac(tn.buf, moc, m))
    except Exception as loi:
        nk.dong(step, gio, thao_tac, f"LỖI SCRIPT: {loi}", ghi_chu)
        raise
    nk.dong(step, gio, thao_tac, kq, ghi_chu)


def kb05(run_id: str, out: Path, nghi: float, eol: bytes) -> None:
    nk = NhatKy(out / "nhat_ky_Host.csv", run_id, "KB-05", "telnet/2223")
    nk.dong(0, gio_utc(), "BAT_DAU")
    gio = gio_utc()
    try:
        tn = Telnet(2223, out / "KB-05_Host.txt", out / "KB-05_Host.raw", eol)
        tn.cho(MAU_LOGIN)
    except Exception as loi:
        nk.dong(1, gio, f"MO_KET_NOI: telnet {HONEYPOT} 2223", f"LỖI SCRIPT: {loi}")
        raise
    nk.dong(1, gio, f"MO_KET_NOI: telnet {HONEYPOT} 2223", "thấy login:")
    step = 2
    for i, mk in enumerate(MK_KB05):
        buoc_telnet(nk, tn, step, f"GUI_USERNAME: {USER}", USER, MAU_MK)
        sau = MAU_SHELL if i == len(MK_KB05) - 1 else MAU_LOGIN
        buoc_telnet(nk, tn, step + 1, f"GUI_MAT_KHAU: {mk}", mk, sau, GHI_CHU_MK)
        step += 2
    for lenh in LENH_KB05:
        time.sleep(nghi)
        buoc_telnet(nk, tn, step, f"GO_LENH: {lenh}", lenh, None if lenh == "exit" else MAU_SHELL)
        step += 1
    tn.dong()
    nk.dong(step, gio_utc(), "KET_THUC", "server đã đóng kết nối")


ASKPASS_SH = """#!/bin/sh
# Askpass cua TV4 cho KB-01: KHONG tra mat khau.
# Ghi dau nhac ra file roi ngu; script chinh se dung ssh. Khong thoat som,
# vi askpass thoat loi co the lam ssh gui mat khau rong.
printf '%s\\n' "$1" > "$TV4_ASKPASS_DAU"
sleep 600
"""


def dung_cay_tien_trinh(p: subprocess.Popen) -> None:
    if os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"], capture_output=True)
    else:
        p.kill()


def kb01(run_id: str, out: Path, ssh: str) -> None:
    nk = NhatKy(out / "nhat_ky_Host.csv", run_id, "KB-01", "ssh/2222")
    askpass = out / "askpass_cho.sh"
    askpass.write_text(ASKPASS_SH, encoding="ascii", newline="\n")
    dau = out / "KB-01_Host.askpass.txt"
    if dau.exists():
        raise SystemExit(f"{dau} đã có; dùng thư mục --out khác.")
    env = dict(os.environ, SSH_ASKPASS=askpass.resolve().as_posix(), SSH_ASKPASS_REQUIRE="force",
               DISPLAY="tv4:0", TV4_ASKPASS_DAU=dau.resolve().as_posix())
    argv = [ssh, "-v", "-p", "2222", "-o", "PubkeyAuthentication=no",
            "-o", "PreferredAuthentications=password", "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null", f"{USER}@{HONEYPOT}"]
    tr = out / "KB-01_Host.txt"
    nk.dong(0, gio_utc(), "BAT_DAU")
    gio = gio_utc()
    with tr.open("ab") as f:
        p = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=f, stderr=subprocess.STDOUT, env=env)
        het_han = time.monotonic() + 30
        while not (dau.exists() and dau.stat().st_size > 0):
            if p.poll() is not None or time.monotonic() > het_han:
                dung_cay_tien_trinh(p)
                nk.dong(1, gio, "MO_KET_NOI: " + " ".join(argv[1:]),
                        f"LỖI SCRIPT: không thấy askpass được gọi (mã ssh {p.poll()})")
                raise SystemExit("KB-01 Host lỗi: xem transcript")
            time.sleep(0.1)
        banner = BANNER.search(tr.read_bytes())
        kq = "askpass được gọi (dấu nhắc mật khẩu): " + dau.read_text(errors="replace").strip()
        if banner:
            kq = f"banner: {banner.group(1).decode(errors='replace')}; " + kq
        nk.dong(1, gio, "MO_KET_NOI: " + " ".join(argv[1:]), kq)
        time.sleep(1.5)  # để phiên không quá ngắn (experiments/quy_uoc_nhat_ky.md, mục 5)
        gio = gio_utc()
        dung_cay_tien_trinh(p)
        p.wait(timeout=10)
    nk.dong(2, gio, "HUY_DAU_NHAC: dừng ssh khi đang chờ askpass", f"ssh bị dừng, mã {p.returncode}")
    nk.dong(3, gio_utc(), "KET_THUC")


def main() -> int:
    for luong in (sys.stdout, sys.stderr):
        luong.reconfigure(encoding="utf-8")  # console Windows mặc định cp1252
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run", required=True, help="RUN-xx, hoặc CHUAN-BI cho phiên chuẩn bị")
    ap.add_argument("--kb", required=True, choices=["KB-05", "KB-01"])
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--nghi", type=float, default=1.0, help="giây nghỉ giữa hai lệnh ở KB-05")
    ap.add_argument("--eol", choices=["crlf", "lf"], default="crlf", help="ký tự Enter gửi qua Telnet")
    ap.add_argument("--ssh", default=SSH_MAC_DINH, help="đường dẫn ssh của Git for Windows")
    args = ap.parse_args()
    if not re.fullmatch(r"RUN-\d{2}|CHUAN-BI[A-Za-z0-9_-]*", args.run):
        ap.error("--run phải dạng RUN-xx hoặc CHUAN-BI…")
    args.out.mkdir(parents=True, exist_ok=True)
    ten = {"KB-05": "KB-05_Host.txt", "KB-01": "KB-01_Host.txt"}[args.kb]
    if (args.out / ten).exists():
        ap.error(f"{args.out / ten} đã có; không ghi đè transcript. Dùng thư mục --out khác.")
    if args.kb == "KB-05":
        kb05(args.run, args.out, args.nghi, b"\r\n" if args.eol == "crlf" else b"\n")
    else:
        kb01(args.run, args.out, args.ssh)
    return 0


if __name__ == "__main__":
    sys.exit(main())
