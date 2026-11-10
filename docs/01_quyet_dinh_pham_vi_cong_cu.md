# Quyết định phạm vi và công cụ (WP-01)

**Trạng thái:** phần công cụ (TV1) đã soạn, chờ TV3 review · phần phạm vi (TV4) chưa có · phần trường dữ liệu chờ TV2 xác nhận

## 1. Phạm vi và câu hỏi nghiên cứu (TV4)

[TV4 điền: bản chốt Q1–Q3, phạm vi trong/ngoài. Bản nháp ở mục A của kế hoạch.]

## 2. Quyết định công cụ (TV1)

| | Lựa chọn | Lý do |
| --- | --- | --- |
| **Chính** | **Cowrie**, mở SSH (cổng 2222) và Telnet (cổng 2223) | Ghi được đủ các thứ đề tài cần phân tích: nguồn, dịch vụ, lệnh, diễn biến phiên. Mọi sự kiện có mã phiên nên dựng được timeline; log JSON đọc thẳng bằng Pandas |
| **Dự phòng** | **OpenCanary** | Dùng nếu Cowrie không cài được cả bằng pip lẫn Docker. Vẫn có nguồn, dịch vụ, lần thử đăng nhập; **không có lệnh** vì SSH luôn từ chối đăng nhập, không có shell |
| Không chọn | Dionaea | Mục đích chính là thu mẫu malware, khó có dữ liệu ý nghĩa trong lab cô lập; dự án gần như ngừng bảo trì (bản cuối 11/2020), khó cài trên hệ điều hành mới |
| Không chọn | Honeypot tự viết | Chỉ ghi được những gì nhóm tự code, dễ có lỗi bảo mật; chỉ dùng khi cả hai công cụ trên đều không chạy |

## 3. Trả lời các câu hỏi của WP-01 về Cowrie

**3.1. Cowrie ghi những sự kiện nào?**
Mọi sự kiện đều có `eventid`, `timestamp` (ISO 8601, UTC), `session`, `src_ip`, `sensor`, `message`. Các sự kiện nhóm dùng:

| Sự kiện | Ý nghĩa | Trường riêng |
| --- | --- | --- |
| `cowrie.session.connect` | Có kết nối mới | `src_port`, `dst_ip`, `dst_port`, `protocol` |
| `cowrie.client.version` | Phiên bản SSH client | `version` |
| `cowrie.client.kex` | Fingerprint client | `hassh` |
| `cowrie.login.failed` / `cowrie.login.success` | Thử đăng nhập | `username`, `password` |
| `cowrie.command.input` | Lệnh gõ trong shell giả | `input` |
| `cowrie.command.failed` | Lệnh shell giả không hỗ trợ | `input` |
| `cowrie.session.file_download` | Tải tệp | `url`, `shasum` (SHA-256), `outfile` |
| `cowrie.log.closed` | Đóng bản ghi TTY | `ttylog`, `duration_ms` |
| `cowrie.session.closed` | Kết thúc phiên | `duration_ms` (trường `duration` cũ đã bị bỏ) |

**3.2. Log ở đâu, định dạng gì?**
- `var/log/cowrie/cowrie.json`: mỗi dòng một sự kiện JSON. Đây là file nhóm dùng để phân tích.
- `var/log/cowrie/cowrie.log`: log chẩn đoán, dùng khi gỡ lỗi.
- `var/lib/cowrie/tty/`: bản ghi phiên, phát lại bằng lệnh `playlog`.
- `var/lib/cowrie/downloads/`: tệp bị tải về.
- Các đường dẫn tính từ thư mục làm việc khi chạy Cowrie. Log xoay vòng lúc nửa đêm; tên file JSON sau khi xoay cần xem trên máy thật.

**3.3. Cài theo cách nào?**
Tài liệu chính thức nêu 3 cách: pip, Docker, git checkout (cho người phát triển).

- **Nhóm chọn: pip trong virtualenv trên VM-H.** Đây là cách tài liệu khuyên cho người vận hành, và dễ ngắt Internet sau khi cài.
  ```bash
  python3 -m venv cowrie-env
  source cowrie-env/bin/activate
  pip install cowrie
  cowrie init      # tạo etc/cowrie.cfg
  cowrie start
  ```
- Cần **Python ≥ 3.11**. Đề xuất VM-H chạy Ubuntu 24.04 LTS hoặc Debian 12 trở lên; kiểm tra bằng `python3 --version` trước khi cài.
- **Dự phòng:** Docker image `cowrie/cowrie` (bật Telnet bằng `COWRIE_TELNET_ENABLED=yes`). Phải tải image trước khi ngắt Internet.
- Ghi phiên bản Cowrie thực tế đã cài vào README của lab.

**3.4. Cần quyền gì?**
- Cổng 2222 và 2223 đều trên 1024, nên **không cần root**. Cowrie chạy bằng một user riêng.
- Cấu hình thay đổi ghi trong `etc/cowrie.cfg`. File mặc định để tham khảo là `src/cowrie/data/etc/cowrie.cfg.dist` trong repo Cowrie.
- **Phải tạo `etc/userdb.txt` riêng.** Nếu không có file này, Cowrie dùng danh sách mặc định chấp nhận gần như mọi cặp username/password (luật `*:x:*`). Danh sách credential lấy từ TV4 (bàn giao BG-01).

**3.5. Tính năng nào có thể tạo kết nối ra ngoài?**

| Tính năng | Quyết định |
| --- | --- |
| Tải tệp từ shell giả (`wget`, `curl`): Cowrie tải thật | Giữ, nhưng VM-H không có đường ra Internet. Chỉ thử ở KB-04 với web server trong lab |
| Chế độ proxy (chuyển tiếp tới máy thật) | Không dùng, giữ `backend = shell` |
| Chế độ LLM (gọi mô hình ngôn ngữ bên ngoài) | Không dùng |
| Các plugin xuất log ra dịch vụ ngoài | Chỉ bật output JSON ghi file. Kiểm tra trong `cowrie.cfg` không có plugin nào khác được bật [cần xem trên máy thật] |
| SSH port forwarding (`cowrie.direct-tcpip.request`) | Cowrie ghi lại yêu cầu. Xem lại các tùy chọn forwarding trong mục `[ssh]` của `cowrie.cfg.dist` khi cài [cần xem trên máy thật] |

Mọi tính năng trên đều nằm sau lớp cách ly ở mức VM: không có NAT, firewall chặn chiều ra (kế hoạch mục D.5).

## 4. Hành vi muốn quan sát → sự kiện → trường dữ liệu

Bảng do TV1 soạn; **TV2 xác nhận** đã đủ trường cho bộ xử lý.

| Hành vi muốn quan sát | Câu hỏi | Sự kiện Cowrie | Trường dùng |
| --- | --- | --- | --- |
| Ai kết nối, vào dịch vụ nào | Q1, Q2 | `cowrie.session.connect` | `src_ip`, `src_port`, `dst_port`, `protocol`, `session` |
| Dùng client gì | Q1 | `cowrie.client.version`, `cowrie.client.kex` | `version`, `hassh` |
| Thử mật khẩu nào, kết quả ra sao | Q1, Q3 | `cowrie.login.failed`, `cowrie.login.success` | `username`, `password`, `eventid` |
| Gõ lệnh gì, theo thứ tự nào | Q2, Q3 | `cowrie.command.input` | `input`, `timestamp` |
| Lệnh nào làm lộ shell giả | Q1 (deception) | `cowrie.command.failed` | `input` |
| Tải tệp gì về | Q3 | `cowrie.session.file_download` | `url`, `shasum` |
| Phiên kéo dài bao lâu | Q2 | `cowrie.session.closed` | `duration_ms` |
| Xem lại toàn bộ phiên | Q2 | `cowrie.log.closed` | `ttylog` |

## 5. Ghi chú cho phương án dự phòng (OpenCanary)

- Cấu hình JSON tạo bằng `opencanaryd --copyconfig` tại `/etc/opencanaryd/opencanary.conf`, phải thuộc root. Mặc định chỉ bật FTP; phải tự bật SSH và Telnet.
- Log ở `/var/tmp/opencanary.log`, mỗi dòng một JSON. `local_time` thực ra là UTC; chỉ `local_time_adjusted` là giờ máy.
- Mã `logtype` cho SSH: 4000 kết nối, 4001 phiên bản, 4002 thử đăng nhập.
- Bản Docker chính thức chạy bằng host network, nên phải cách ly ở mức VM.

## 6. Đầu vào cần có cho bước tiếp theo của TV1

| Cần gì | Từ ai | Dùng cho |
| --- | --- | --- |
| Máy nào chạy lab, RAM bao nhiêu, dùng VirtualBox hay VMware | Cả nhóm | WP-02: sơ đồ lab |
| Hệ điều hành cho VM-H (Ubuntu 24.04 hoặc Debian 12+) | TV1 chốt | WP-03: cài Cowrie |
| Danh sách credential cho `userdb.txt` | TV4 (BG-01) | WP-03 |

## Nguồn

- Cowrie: https://github.com/cowrie/cowrie/blob/main/README.rst · https://docs.cowrie.org/en/latest/INSTALL.html · https://docs.cowrie.org/en/latest/OUTPUT.html · https://docs.cowrie.org/en/latest/docker/README.html · https://github.com/cowrie/cowrie/blob/main/src/cowrie/data/etc/cowrie.cfg.dist · https://github.com/cowrie/cowrie/blob/main/src/cowrie/data/etc/userdb.example · https://docs.cowrie.org/en/latest/CHANGELOG.html
- OpenCanary: https://github.com/thinkst/opencanary · https://opencanary.readthedocs.io/en/latest/ · https://github.com/thinkst/opencanary/blob/master/opencanary/logger.py
- Dionaea: https://github.com/DinoTools/dionaea · https://dionaea.readthedocs.io/en/latest/changelog.html
