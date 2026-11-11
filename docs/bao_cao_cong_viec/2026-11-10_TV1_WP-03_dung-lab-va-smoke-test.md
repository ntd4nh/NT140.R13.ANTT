# WP-03 – Dựng lab thật và smoke test (TV1)

**Ngày:** 2026-11-10 · **Người làm:** TV1 · **Trạng thái:** Xong

Lab đã chạy thật trên máy TV1. Honeypot Cowrie ghi đúng SSH và Telnet từ cả hai nguồn, và không ra được Internet. Từ giờ TV2 có log thật để chốt schema, TV3 có lab để review và kiểm tra cách ly.

## Đã làm gì
- Dựng hai VM Ubuntu Server 24.04.5 trên VMware Workstation 25H2, mạng VMnet1 `192.168.239.0/24`:
  - VM-H (honeypot) `.20`, chạy Cowrie 3.1.6 bằng user `cowrie`, SSH giả cổng 2222, Telnet giả cổng 2223.
  - VM-A (nguồn 1) `.10`.
  - Máy Windows là nguồn 2 (`.1`).
- Cấu hình Cowrie: bật Telnet; tạo `userdb.txt` tạm chỉ nhận `labuser` / `LabOnly-2026`; tắt `[ssh] forwarding`. Ngoài ba thay đổi đó, mọi thứ để mặc định.
- Cách ly:
  - Hai VM không còn card NAT.
  - ufw trên VM-H chặn mọi chiều ra; chỉ máy Windows vào được cổng quản trị 22.
  - Tắt Shared Folders, kéo-thả và copy-paste; bỏ Sound Card và USB.
- Smoke test: từ mỗi nguồn chạy SSH và Telnet, mỗi lần đăng nhập sai một lần, đúng một lần, rồi gõ `whoami`, `exit`.
- Tự kiểm tra cách ly: ping, curl, `wget` trong shell giả, và thử vào cổng 22 từ VM-A.

## Kết quả
- Sản phẩm:
  - `evidence/smoke_test/`: log thật, `SHA256SUMS`, README.
  - `evidence/kiem_tra_cach_ly_TV1.md`
  - `Implement/lab/cowrie/`: `cowrie.cfg`, cùng README liệt kê các thay đổi và danh sách yếu tố mồi.
  - Đã cập nhật `Implement/lab/README_chay_lab.md` (thêm Bước 7.4, điền bảng Bước 16, ghi khác biệt khi dựng thật) và `docs/02_so_do_lab.md` mục 8.
  - Thêm `.gitattributes` để Git giữ nguyên từng byte trong `evidence/` và `data/raw/`.
- Đã kiểm tra bằng cách:
  - Đếm sự kiện bằng `jq`: 8 phiên (SSH và Telnet từ cả `.10` lẫn `.1`), 4 lần đăng nhập sai, 4 lần đúng, 8 lệnh.
  - Hash file chép về khớp với file trên VM-H.
  - Mọi phép thử ra Internet đều thất bại.

## Còn thiếu / vướng mắc
- `userdb.txt` vẫn là bản tạm; chờ danh sách credential của TV4 (BG-01).
- Telnet Client của Windows chưa bật. Smoke test dùng Python thay thế; chạy KB-05 bằng tay thì cần bật Telnet Client hoặc dùng PuTTY.
- Cowrie không tự chạy khi bật lại VM-H. Mỗi lần mở lab phải `cowrie start` (Phụ lục 1).

## Liên quan tới người khác
- Bàn giao: **BG-02** (log smoke test → TV2), **BG-03** (lab, README, cấu hình → TV3), **BG-08** (yếu tố mồi → TV3).
- Cần review: **TV3**, gồm sơ đồ lab, README, cấu hình, log.

## Các thành viên khác cần biết
- **TV2:** đọc `evidence/smoke_test/README.md` trước. Các phiên gõ giống nhau dùng chung một file TTY, nên phải ghép phiên với file TTY bằng trường `ttylog` trong sự kiện `cowrie.log.closed`.
- **TV3:** có 5 điểm lộ đã gặp khi chạy thử, ghi trong `Implement/lab/cowrie/README.md`. Ví dụ: banner SSH 9.2p1 nhưng `ssh -V` trong shell giả trả 7.9p1, và tên máy mặc định `svr04`.
- **TV4:** gửi credential (BG-01). Kịch bản chỉ nhắm `192.168.239.20` cổng 2222/2223.
