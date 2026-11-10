# Log smoke test (WP-03, bàn giao BG-02)

**Người chạy:** TV1 · **Ngày:** 2026-11-10 · **Kết quả:** ĐẠT

Log thật lấy từ Cowrie trên VM-H, chưa sửa gì. Không sửa các file trong thư mục này; muốn xử lý thì chép ra chỗ khác.

## Môi trường

| Mục | Giá trị |
| --- | --- |
| Honeypot | Cowrie **3.1.6**, cài bằng `pip install cowrie` trong venv `~/cowrie-env`, chạy bằng user `cowrie` (không phải root) |
| Hệ điều hành VM-H | Ubuntu Server 24.04.5 LTS, Python 3.12.3, VMware Workstation 25H2 |
| Cấu hình | Mặc định của `cowrie init`, chỉ đổi `[telnet] enabled = true`; `etc/userdb.txt` = `labuser:x:LabOnly-2026` (tài khoản giả, bản tạm chờ BG-01) |
| Mạng | VMnet1 host-only `192.168.239.0/24`, không có Internet |
| Honeypot | `192.168.239.20`, SSH giả cổng 2222, Telnet giả cổng 2223 |
| Nguồn 1 | VM-A `192.168.239.10` (Ubuntu 24.04.5): OpenSSH 9.6p1 + `sshpass`; Telnet bằng Python `telnetlib` |
| Nguồn 2 | Máy Windows `192.168.239.1`: OpenSSH 10.5p1 (Git Bash); Telnet bằng Python 3.12 `telnetlib` |
| Đồng hồ | Cả ba máy dùng UTC; VMware đồng bộ giờ VM theo host. Lệch giữa ba máy dưới 1 giây khi đo bằng `date -u` liên tiếp |

## Đã làm gì (giờ UTC, ghi phía client)

| Giờ | Nguồn | Thao tác |
| --- | --- | --- |
| 14:47:23 | VM-A | Kiểm tra cổng: mở TCP tới 2222 và 2223 rồi đóng ngay, không đăng nhập. Tạo 2 phiên chỉ có `session.connect` / `session.closed` |
| 14:47:44 | VM-A | SSH: mật khẩu sai |
| 14:47:47 | VM-A | SSH: mật khẩu đúng → `whoami` → `exit` |
| 14:47:49 | VM-A | Telnet: mật khẩu sai → mật khẩu đúng → `whoami` → `exit` |
| 14:48:03 | Windows | SSH: mật khẩu sai |
| 14:48:06 | Windows | SSH: mật khẩu đúng → `whoami` → `exit` |
| 14:48:13 | Windows | Telnet: mật khẩu sai → mật khẩu đúng → `whoami` → `exit` |

Các thao tác chạy bằng script phía client (không gõ tay), nên khoảng cách giữa các lệnh rất ngắn.

## Kết quả kiểm tra trên log

- 8 phiên `cowrie.session.connect`: VM-A có 3 SSH và 2 Telnet (đã gồm 2 phiên kiểm tra cổng); Windows có 2 SSH và 1 Telnet.
- `cowrie.login.failed` 4 lần, `cowrie.login.success` 4 lần, đúng username/password đã gõ.
- `cowrie.command.input` 8 lần (`whoami`, `exit` ở mỗi phiên đăng nhập thành công).
- 8 `cowrie.session.closed`, có `duration_ms`.
- 58 dòng, mỗi dòng là một JSON đọc được (`jq -e .`).

## Lưu ý cho người xử lý dữ liệu (TV2)

- **Mỗi phiên có một `session` riêng**; dùng trường này để ghép các sự kiện.
- `protocol` (`ssh`/`telnet`) có ở `session.connect`.
- Thư mục `tty/` chỉ có **1 file**, dù có 4 phiên đăng nhập thành công: Cowrie đặt tên file TTY theo hash nội dung, nên các phiên gõ giống hệt nhau dùng chung một file. Muốn biết phiên nào trỏ tới file nào thì xem trường `ttylog` trong sự kiện `cowrie.log.closed`.
- Sự kiện chỉ có ở SSH: `cowrie.client.version`, `cowrie.client.kex`, `cowrie.client.size`, `cowrie.session.params`. Chỉ có ở Telnet: `cowrie.telnet.option`.
- `cowrie.log` là log dạng chữ, dùng để đọc lỗi; phân tích dùng `cowrie.json`.

## Kiểm tra tính nguyên vẹn

```bash
cd evidence/smoke_test
sha256sum -c SHA256SUMS
```

Hash của `cowrie.json` và `cowrie.log` khớp với file gốc trên VM-H lúc chép về. File `.gitattributes` của repo giữ nguyên từng byte trong `evidence/`, để clone về trên Windows hash vẫn khớp.
