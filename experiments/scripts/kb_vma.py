#!/usr/bin/env python3
"""Chạy KB-01..KB-03, KB-06..KB-09 từ VM-A vào honeypot, và đối chứng KB-03 trên VM-A thật.

Người viết: TV4 (có AI hỗ trợ), 2026-11-11; thêm KB-06..KB-09 ngày 2026-11-22.
TRẠNG THÁI: CHƯA CHẠY THỬ TRÊN LAB. Phải chạy phiên chuẩn bị (``--run CHUAN-BI``)
và đọc log Cowrie trước khi dùng cho một RUN thật.

Chỉ dùng thư viện chuẩn (pty, select, socket), chạy trên Linux (VM-A, Python 3).
Chỉ kết nối tới 192.168.239.20 cổng 2222 (SSH) và 2223 (Telnet, KB-09).
Mọi mật khẩu, username lạ, khóa SSH và dòng cron trong file là dữ liệu giả của lab.

Phần Telnet của KB-09 có lớp xử lý byte IAC riêng, lặp lại logic của kb_host.py;
cố ý để kb_vma.py tự chứa, vì khi chạy RUN chỉ chép mỗi kb_vma.py sang VM-A.

Cách chạy trên VM-A (user labadmin), mỗi kịch bản một lệnh:

    python3 kb_vma.py --run RUN-01 --kb KB-01 --out ~/tv4/RUN-01
    python3 kb_vma.py --run RUN-01 --kb KB-02 --out ~/tv4/RUN-01
    python3 kb_vma.py --run RUN-01 --kb KB-06 --out ~/tv4/RUN-01   # rải mật khẩu (SSH)
    python3 kb_vma.py --run RUN-01 --kb KB-07 --out ~/tv4/RUN-01   # bot gửi lệnh kèm (SSH)
    python3 kb_vma.py --run RUN-01 --kb KB-03 --out ~/tv4/RUN-01
    python3 kb_vma.py --run RUN-01 --kb KB-08 --out ~/tv4/RUN-01   # duy trì truy cập/xóa dấu vết (SSH)
    python3 kb_vma.py --run RUN-01 --kb KB-09 --out ~/tv4/RUN-01   # botnet IoT (Telnet)
    python3 kb_vma.py --run RUN-01 --kb KB-03-THAT --out ~/tv4/RUN-01   # đối chứng, không ghi nhật ký

Đầu ra trong thư mục --out:
    nhat_ky_VM-A.csv        dòng nhật ký H.2 (11 cột); giờ lấy đúng lúc gửi
    <KB>_VM-A.txt            transcript thô (stdout + stderr qua pty; KB-09: byte đã bỏ IAC)
    KB-09_VM-A.raw           byte Telnet nhận được nguyên văn (KB-09)
    KB-03_VM-A_that.txt      transcript đối chứng (pty); KB-03_VM-A_that.typescript do lệnh script ghi
"""

from __future__ import annotations

import argparse
import csv
import os
import pty
import re
import select
import signal
import socket
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HONEYPOT = "192.168.239.20"
CONG_SSH = 2222
CONG_TELNET = 2223
MAY_NGUON = "VM-A"
IP_NGUON = "192.168.239.10"
NGUOI = "TV4 (AI hỗ trợ)"
COT = [
    "run_id", "scenario_id", "step_no", "time_utc_client", "may_nguon", "ip_nguon",
    "dich_vu_cong", "thao_tac", "ket_qua_phia_client", "nguoi_thuc_hien", "ghi_chu",
]
USER = "labuser"
# Mật khẩu giả của lab (docs/03_kich_ban_thu_nghiem.md, mục 0.2).
MK_DUNG = "LabOnly-2026"
MK_KB02_KN1 = ["LabWrong-01", "LabWrong-02", "LabWrong-03"]
MK_KB02_KN2 = ["LabWrong-04", "LabWrong-05", MK_DUNG]
GHI_CHU_MK = "mật khẩu giả của lab"
LENH_KB03 = [
    "whoami", "id", "uname -a", "pwd", "ls -la", "cat /etc/passwd",
    "ps aux", "ifconfig", "ssh -V", "nt140_cmd_khong_ton_tai", "exit",
]
# KB-06 rải mật khẩu: một mật khẩu giả cho nhiều username giả (mỗi username một kết nối).
MK_KB06 = "LabSpray-2026"
USERS_KB06 = ["admin", "root", "user", "oracle"]
# KB-07 bot: một chuỗi lệnh gửi kèm exec, không mở shell tương tác.
LENH_KB07 = "whoami; uname -a; hostname; id"
# KB-08 duy trì truy cập/xóa dấu vết. MỌI khóa SSH, dòng cron, đường dẫn là chuỗi GIẢ của lab.
LENH_KB08 = [
    "mkdir -p .ssh",
    "echo 'ssh-ed25519 AAAA-LAB-FAKE-KEY-KHONG-PHAI-KHOA-THAT lab-attacker@nt140' >> .ssh/authorized_keys",
    "cat .ssh/authorized_keys",
    "echo '*/5 * * * * /tmp/.lab_fake_beacon.sh # lab-gia' | crontab -",
    "crontab -l",
    "history -c",
    "rm -f .bash_history",
    "exit",
]
# KB-09 botnet IoT qua Telnet từ VM-A: cặp "mặc định" giả, lần cuối là cặp hợp lệ của lab
# (đóng vai cặp mặc định đoán trúng; giữ userdb.txt đúng một dòng).
PAIRS_KB09 = [("root", "LabIoT-admin"), ("admin", "LabIoT-1234"), (USER, MK_DUNG)]
LENH_KB09 = ["cat /proc/cpuinfo", "uname -a", "exit"]
NGHI_KB09 = 0.2  # bot IoT gần như không nghỉ giữa các lệnh (khác KB-03 gõ tay)
# Byte điều khiển Telnet (IAC) cho KB-09.
IAC, DONT, DO, WONT, WILL, SB, SE = 255, 254, 253, 252, 251, 250, 240
SSH_CO_BAN = [
    "ssh", "-p", str(CONG_SSH),
    "-o", "PubkeyAuthentication=no",
    "-o", "PreferredAuthentications=password",
    "-o", "StrictHostKeyChecking=no",
    "-o", "UserKnownHostsFile=/dev/null",
]
DICH = f"{USER}@{HONEYPOT}"
MAU_MK = re.compile(rb"[Pp]assword: *$")
MAU_LOGIN = re.compile(rb"login: *$")  # dấu nhắc Telnet (KB-09)
MAU_SHELL = re.compile(rb"[$#] $")
ANSI = re.compile(rb"\x1b\[[0-9;?]*[A-Za-z]")
BANNER = re.compile(rb"remote software version ([^\r\n]+)")


def gio_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def tom_tat(du_lieu: bytes, gioi_han: int = 150) -> str:
    """Dòng cuối có chữ của đoạn output, bỏ mã điều khiển màu."""
    chu = ANSI.sub(b"", du_lieu).decode("utf-8", errors="replace")
    dong = [d.strip() for d in chu.replace("\r", "\n").split("\n") if d.strip()]
    return dong[-1][:gioi_han] if dong else ""


def truoc_dau_nhac(buf: bytes, moc: int, m: re.Match[bytes]) -> bytes:
    """Phần output từ moc tới trước dòng chứa dấu nhắc vừa khớp."""
    doan = buf[moc:m.start()]
    cat = max(doan.rfind(b"\n"), doan.rfind(b"\r"))
    return doan[:cat] if cat >= 0 else b""


class NhatKy:
    def __init__(self, path: Path, run_id: str, kb: str, bat: bool = True,
                 dich_vu: str | None = None) -> None:
        self.path, self.run_id, self.kb, self.bat = path, run_id, kb, bat
        self.dich_vu = dich_vu or f"ssh/{CONG_SSH}"

    def dong(self, step: int, gio: str, thao_tac: str, ket_qua: str = "", ghi_chu: str = "") -> None:
        if not self.bat:
            return
        moi = not self.path.exists() or self.path.stat().st_size == 0
        with self.path.open("a", encoding="utf-8", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            if moi:
                w.writerow(COT)
            w.writerow([self.run_id, self.kb, step, gio, MAY_NGUON, IP_NGUON,
                        self.dich_vu, thao_tac, ket_qua, NGUOI, ghi_chu])
        print(f"[{gio}] {self.kb} bước {step}: {thao_tac} -> {ket_qua}")


class Phien:
    """Một tiến trình chạy trong pty; ghi mọi byte nhận được vào transcript."""

    def __init__(self, argv: list[str], transcript: Path, env: dict[str, str] | None = None) -> None:
        self.argv = argv
        self.pid, self.fd = pty.fork()
        if self.pid == 0:  # tiến trình con
            try:
                if env:
                    os.environ.update(env)
                os.execvp(argv[0], argv)
            finally:
                os._exit(127)
        self.buf = b""
        self.pos = 0
        self.het = False
        self.tf = transcript.open("ab")

    def _doc(self, cho: float) -> None:
        r, _, _ = select.select([self.fd], [], [], cho)
        if not r:
            return
        try:
            data = os.read(self.fd, 4096)
        except OSError:
            data = b""
        if not data:
            self.het = True
            return
        self.buf += data
        self.tf.write(data)
        self.tf.flush()

    def cho(self, mau: re.Pattern[bytes], han_s: float = 30.0, yen_s: float = 0.4) -> re.Match[bytes]:
        """Chờ mẫu xuất hiện ở cuối output và output đứng yên yen_s giây."""
        het_han = time.monotonic() + han_s
        while True:
            m = mau.search(self.buf, self.pos)
            if m and m.end() == len(self.buf):
                truoc = len(self.buf)
                self._doc(yen_s)
                if len(self.buf) == truoc:
                    self.pos = m.end()
                    return m
                continue
            if self.het:
                raise RuntimeError(f"tiến trình đã đóng khi chờ {mau.pattern!r}")
            con = het_han - time.monotonic()
            if con <= 0:
                raise TimeoutError(f"quá {han_s}s khi chờ {mau.pattern!r}")
            self._doc(min(con, 0.5))

    def cho_het(self, han_s: float = 30.0) -> None:
        het_han = time.monotonic() + han_s
        while not self.het:
            con = het_han - time.monotonic()
            if con <= 0:
                raise TimeoutError(f"quá {han_s}s khi chờ tiến trình đóng")
            self._doc(min(con, 0.5))

    def gui(self, chu: str | bytes) -> None:
        os.write(self.fd, chu.encode() if isinstance(chu, str) else chu)

    def gui_dong(self, chu: str) -> None:
        self.gui(chu + "\r")  # phím Enter của terminal

    def dong_lai(self, han_s: float = 10.0) -> int:
        """Đợi tiến trình con thoát (dừng hẳn nếu quá hạn) và trả mã thoát."""
        het_han = time.monotonic() + han_s
        while True:
            pid, status = os.waitpid(self.pid, os.WNOHANG)
            if pid:
                break
            if time.monotonic() > het_han:
                os.kill(self.pid, signal.SIGTERM)
                time.sleep(1)
                pid, status = os.waitpid(self.pid, os.WNOHANG)
                if not pid:
                    os.kill(self.pid, signal.SIGKILL)
                    _, status = os.waitpid(self.pid, 0)
                break
            self._doc(0.2)
        self.tf.close()
        try:
            os.close(self.fd)
        except OSError:
            pass
        return os.waitstatus_to_exitcode(status)


def buoc(nk: NhatKy, ph: Phien, step: int, thao_tac: str, gui: str, mau: re.Pattern[bytes] | None,
         ghi_chu: str = "", nhan_ket_qua=None) -> re.Match[bytes] | None:
    """Gửi một dòng, chờ phản hồi (mẫu, hoặc tiến trình đóng nếu mau=None), rồi ghi nhật ký."""
    moc = ph.pos
    gio = gio_utc()
    ph.gui_dong(gui)
    try:
        if mau is None:
            ph.cho_het()
            m = None
            kq = tom_tat(ph.buf[moc:])
        else:
            m = ph.cho(mau)
            kq = nhan_ket_qua(ph, moc, m) if nhan_ket_qua else tom_tat(truoc_dau_nhac(ph.buf, moc, m))
    except Exception as loi:
        nk.dong(step, gio, thao_tac, f"LỖI SCRIPT: {loi}", ghi_chu)
        raise
    nk.dong(step, gio, thao_tac, kq, ghi_chu)
    return m


def kq_shell(ph: Phien, moc: int, m: re.Match[bytes]) -> str:
    return "thấy dấu nhắc shell: " + tom_tat(ph.buf[moc:m.end()])


def mo_ket_noi(nk: NhatKy, step: int, argv: list[str], tr: Path, mau: re.Pattern[bytes]) -> Phien:
    gio = gio_utc()
    ph = Phien(argv, tr)
    try:
        ph.cho(mau)
    except Exception as loi:
        nk.dong(step, gio, "MO_KET_NOI: " + " ".join(argv), f"LỖI SCRIPT: {loi}")
        raise
    banner = BANNER.search(ph.buf)
    kq = "thấy dấu nhắc mật khẩu"
    if banner:
        kq = f"banner: {banner.group(1).decode(errors='replace')}; " + kq
    nk.dong(step, gio, "MO_KET_NOI: " + " ".join(argv), kq)
    return ph


def kb01(nk: NhatKy, out: Path) -> None:
    tr = out / "KB-01_VM-A.txt"
    argv = ["ssh", "-v"] + SSH_CO_BAN[1:] + [DICH]
    nk.dong(0, gio_utc(), "BAT_DAU")
    ph = mo_ket_noi(nk, 1, argv, tr, MAU_MK)
    time.sleep(1.5)  # để phiên không quá ngắn (experiments/quy_uoc_nhat_ky.md, mục 5)
    gio = gio_utc()
    ph.gui(b"\x03")  # Ctrl+C ở dấu nhắc mật khẩu; không gửi mật khẩu, không Enter
    try:
        ph.cho_het(10)
    except TimeoutError:
        pass
    ma = ph.dong_lai()
    nk.dong(2, gio, "HUY_DAU_NHAC: Ctrl+C", f"ssh thoát, mã {ma}")
    nk.dong(3, gio_utc(), "KET_THUC")


def kb02(nk: NhatKy, out: Path) -> None:
    tr = out / "KB-02_VM-A.txt"
    argv = SSH_CO_BAN + ["-o", "NumberOfPasswordPrompts=3", DICH]
    nk.dong(0, gio_utc(), "BAT_DAU")
    # Kết nối 1: ba mật khẩu sai, client tự ngắt.
    ph = mo_ket_noi(nk, 1, argv, tr, MAU_MK)
    for i, mk in enumerate(MK_KB02_KN1):
        buoc(nk, ph, 2 + i, f"GUI_MAT_KHAU: {mk}", mk, MAU_MK if i < 2 else None, GHI_CHU_MK)
    ma = ph.dong_lai()
    nk.dong(5, gio_utc(), "CLIENT_TU_NGAT: sau 3 lần sai", f"ssh thoát, mã {ma}")
    time.sleep(2)
    # Kết nối 2: hai mật khẩu sai, một mật khẩu đúng, rồi exit.
    ph = mo_ket_noi(nk, 6, argv, tr, MAU_MK)
    buoc(nk, ph, 7, f"GUI_MAT_KHAU: {MK_KB02_KN2[0]}", MK_KB02_KN2[0], MAU_MK, GHI_CHU_MK)
    buoc(nk, ph, 8, f"GUI_MAT_KHAU: {MK_KB02_KN2[1]}", MK_KB02_KN2[1], MAU_MK, GHI_CHU_MK)
    buoc(nk, ph, 9, f"GUI_MAT_KHAU: {MK_KB02_KN2[2]}", MK_KB02_KN2[2], MAU_SHELL, GHI_CHU_MK, kq_shell)
    time.sleep(1)
    buoc(nk, ph, 10, "GO_LENH: exit", "exit", None)
    ma = ph.dong_lai()
    nk.dong(11, gio_utc(), "KET_THUC", f"ssh thoát, mã {ma}")


def kb03(nk: NhatKy, out: Path, nghi: float) -> None:
    tr = out / "KB-03_VM-A.txt"
    argv = SSH_CO_BAN + [DICH]
    nk.dong(0, gio_utc(), "BAT_DAU")
    ph = mo_ket_noi(nk, 1, argv, tr, MAU_MK)
    buoc(nk, ph, 2, f"GUI_MAT_KHAU: {MK_DUNG}", MK_DUNG, MAU_SHELL, GHI_CHU_MK, kq_shell)
    for i, lenh in enumerate(LENH_KB03):
        time.sleep(nghi)
        buoc(nk, ph, 3 + i, f"GO_LENH: {lenh}", lenh, None if lenh == "exit" else MAU_SHELL)
    ma = ph.dong_lai()
    nk.dong(3 + len(LENH_KB03), gio_utc(), "KET_THUC", f"ssh thoát, mã {ma}")


def kb06(nk: NhatKy, out: Path) -> None:
    """Rải mật khẩu: mỗi username giả một kết nối, cùng một mật khẩu giả, mỗi kết nối một lần thử."""
    tr = out / "KB-06_VM-A.txt"
    nk.dong(0, gio_utc(), "BAT_DAU")
    step = 1
    for i, user in enumerate(USERS_KB06):
        # NumberOfPasswordPrompts=1: mỗi kết nối chỉ gửi một mật khẩu rồi client tự ngắt.
        argv = SSH_CO_BAN + ["-o", "NumberOfPasswordPrompts=1", f"{user}@{HONEYPOT}"]
        ph = mo_ket_noi(nk, step, argv, tr, MAU_MK)
        step += 1
        gio = gio_utc()
        ph.gui_dong(MK_KB06)  # một mật khẩu giả cho mọi username; username giả phải bị từ chối
        try:
            ph.cho_het(10)
        except TimeoutError:
            pass
        ma = ph.dong_lai()
        nk.dong(step, gio, f"GUI_MAT_KHAU: {MK_KB06}",
                f"username={user}; bị từ chối, ssh thoát mã {ma}",
                GHI_CHU_MK + f"; username giả {user}")
        step += 1
        nk.dong(step, gio_utc(), f"CLIENT_TU_NGAT: sau 1 lần sai (user {user})", f"ssh thoát, mã {ma}")
        step += 1
        if i < len(USERS_KB06) - 1:
            time.sleep(2)  # giãn các kết nối trong cùng kịch bản cho dễ đọc
    nk.dong(step, gio_utc(), "KET_THUC")


def kb07(nk: NhatKy, out: Path) -> None:
    """Bot tự động: gửi chuỗi lệnh kèm exec (không mở shell), trả mật khẩu qua pty, rồi ssh tự thoát."""
    tr = out / "KB-07_VM-A.txt"
    # Chuỗi lệnh là MỘT đối số exec; không dùng -t nên không cấp pty phía server (đúng kiểu bot).
    argv = SSH_CO_BAN + [DICH, LENH_KB07]
    nk.dong(0, gio_utc(), "BAT_DAU")
    ph = mo_ket_noi(nk, 1, argv, tr, MAU_MK)
    gio = gio_utc()
    ph.gui_dong(MK_DUNG)  # trả mật khẩu; sau xác thực, chuỗi lệnh chạy qua exec rồi ssh thoát
    try:
        ph.cho_het(30)
    except TimeoutError:
        pass
    ma = ph.dong_lai()
    nk.dong(2, gio, f"GUI_MAT_KHAU: {MK_DUNG}", f"exec xong, ssh thoát mã {ma}", GHI_CHU_MK)
    nk.dong(3, gio, f"GO_LENH: {LENH_KB07}", "gửi kèm exec khi kết nối, không mở shell",
            "mong đợi một command.input chứa cả chuỗi [XM]")
    nk.dong(4, gio_utc(), "CLIENT_TU_NGAT: bot thoát sau exec", f"ssh thoát, mã {ma}")
    nk.dong(5, gio_utc(), "KET_THUC")


def kb08(nk: NhatKy, out: Path, nghi: float) -> None:
    """Duy trì truy cập/xóa dấu vết trong MỘT phiên shell: thêm khóa SSH giả, dòng cron giả, xóa history."""
    tr = out / "KB-08_VM-A.txt"
    argv = SSH_CO_BAN + [DICH]
    nk.dong(0, gio_utc(), "BAT_DAU")
    ph = mo_ket_noi(nk, 1, argv, tr, MAU_MK)
    buoc(nk, ph, 2, f"GUI_MAT_KHAU: {MK_DUNG}", MK_DUNG, MAU_SHELL, GHI_CHU_MK, kq_shell)
    for i, lenh in enumerate(LENH_KB08):
        time.sleep(nghi)
        buoc(nk, ph, 3 + i, f"GO_LENH: {lenh}", lenh, None if lenh == "exit" else MAU_SHELL)
    ma = ph.dong_lai()
    nk.dong(3 + len(LENH_KB08), gio_utc(), "KET_THUC", f"ssh thoát, mã {ma}")


def kb03_that(out: Path, nghi: float) -> None:
    """Đối chứng: cùng danh sách lệnh trên VM-A thật, trong script + bash --noprofile --norc."""
    tr = out / "KB-03_VM-A_that.txt"
    typescript = out / "KB-03_VM-A_that.typescript"
    argv = ["script", "-q", "-f", "-c", "bash --noprofile --norc -i", str(typescript)]
    print(f"[{gio_utc()}] KB-03-THAT bắt đầu (không ghi nhật ký H.2)")
    ph = Phien(argv, tr, env={"PS1": "vm-a-that$ "})
    ph.cho(MAU_SHELL)
    for lenh in LENH_KB03:
        time.sleep(nghi)
        moc = ph.pos
        ph.gui_dong(lenh)
        if lenh == "exit":
            ph.cho_het()
        else:
            ph.cho(MAU_SHELL)
        print(f"[{gio_utc()}] KB-03-THAT {lenh!r} -> {tom_tat(ph.buf[moc:])}")
    ma = ph.dong_lai()
    print(f"[{gio_utc()}] KB-03-THAT kết thúc, mã {ma}")


# --- Telnet cho KB-09 (socket + tự xử lý IAC; lặp lại logic kb_host.py để kb_vma.py tự chứa) ---

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
    """Telnet tối giản cho KB-09: từ chối mọi tùy chọn (DO/DONT→WONT, WILL/WONT→DONT)."""

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


def kb09(nk: NhatKy, out: Path, nghi: float, eol: bytes) -> None:
    """Botnet IoT qua Telnet từ VM-A: thử nhanh cặp mặc định giả, vào được chạy lệnh xem thiết bị."""
    nk.dong(0, gio_utc(), "BAT_DAU")
    gio = gio_utc()
    try:
        tn = Telnet(CONG_TELNET, out / "KB-09_VM-A.txt", out / "KB-09_VM-A.raw", eol)
        tn.cho(MAU_LOGIN)
    except Exception as loi:
        nk.dong(1, gio, f"MO_KET_NOI: telnet {HONEYPOT} {CONG_TELNET}", f"LỖI SCRIPT: {loi}")
        raise
    nk.dong(1, gio, f"MO_KET_NOI: telnet {HONEYPOT} {CONG_TELNET}", "thấy login:")
    step = 2
    cuoi = len(PAIRS_KB09) - 1
    for i, (user, mk) in enumerate(PAIRS_KB09):
        buoc_telnet(nk, tn, step, f"GUI_USERNAME: {user}", user, MAU_MK)
        sau = MAU_SHELL if i == cuoi else MAU_LOGIN
        gc = GHI_CHU_MK + (f"; cặp mặc định giả (user {user})" if i < cuoi
                           else "; cặp hợp lệ đóng vai mặc định đoán trúng")
        buoc_telnet(nk, tn, step + 1, f"GUI_MAT_KHAU: {mk}", mk, sau, gc)
        step += 2
    for lenh in LENH_KB09:
        time.sleep(nghi)
        buoc_telnet(nk, tn, step, f"GO_LENH: {lenh}", lenh, None if lenh == "exit" else MAU_SHELL)
        step += 1
    tn.dong()
    nk.dong(step, gio_utc(), "KET_THUC", "server đã đóng kết nối")


def main() -> int:
    for luong in (sys.stdout, sys.stderr):
        luong.reconfigure(encoding="utf-8")  # console Windows mặc định cp1252
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run", required=True, help="RUN-xx, hoặc CHUAN-BI cho phiên chuẩn bị")
    ap.add_argument("--kb", required=True,
                    choices=["KB-01", "KB-02", "KB-03", "KB-06", "KB-07", "KB-08", "KB-09", "KB-03-THAT"])
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--nghi", type=float, default=1.0, help="giây nghỉ giữa hai lệnh ở KB-03, KB-08")
    ap.add_argument("--eol", choices=["crlf", "lf"], default="crlf", help="ký tự Enter gửi qua Telnet (KB-09)")
    args = ap.parse_args()
    if not re.fullmatch(r"RUN-\d{2}|CHUAN-BI[A-Za-z0-9_-]*", args.run):
        ap.error("--run phải dạng RUN-xx hoặc CHUAN-BI…")
    out = args.out.expanduser()
    out.mkdir(parents=True, exist_ok=True)
    ten_tr = {"KB-01": "KB-01_VM-A.txt", "KB-02": "KB-02_VM-A.txt", "KB-03": "KB-03_VM-A.txt",
              "KB-06": "KB-06_VM-A.txt", "KB-07": "KB-07_VM-A.txt", "KB-08": "KB-08_VM-A.txt",
              "KB-09": "KB-09_VM-A.txt", "KB-03-THAT": "KB-03_VM-A_that.txt"}[args.kb]
    if (out / ten_tr).exists():
        ap.error(f"{out / ten_tr} đã có; không ghi đè transcript. Dùng thư mục --out khác.")
    dich_vu = f"telnet/{CONG_TELNET}" if args.kb == "KB-09" else None
    nk = NhatKy(out / "nhat_ky_VM-A.csv", args.run, args.kb, dich_vu=dich_vu)
    if args.kb == "KB-01":
        kb01(nk, out)
    elif args.kb == "KB-02":
        kb02(nk, out)
    elif args.kb == "KB-03":
        kb03(nk, out, args.nghi)
    elif args.kb == "KB-06":
        kb06(nk, out)
    elif args.kb == "KB-07":
        kb07(nk, out)
    elif args.kb == "KB-08":
        kb08(nk, out, args.nghi)
    elif args.kb == "KB-09":
        kb09(nk, out, NGHI_KB09, b"\r\n" if args.eol == "crlf" else b"\n")
    else:
        kb03_that(out, args.nghi)
    return 0


if __name__ == "__main__":
    sys.exit(main())
