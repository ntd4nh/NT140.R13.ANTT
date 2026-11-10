# Cấu hình Cowrie đang chạy trên VM-H

**Người làm:** TV1 · **Cowrie:** 3.1.6 (pip, venv `~/cowrie-env`, user `cowrie`) · **Bàn giao:** BG-03, BG-08

`cowrie.cfg` trong thư mục này là bản chép nguyên từ `/home/cowrie/etc/cowrie.cfg` trên VM-H. Đó là file do `cowrie init` sinh ra, chỉ sửa 2 dòng:

| Dòng | Mục | Mặc định | Đang dùng | Lý do |
| --- | --- | --- | --- | --- |
| 813 | `[ssh] forwarding` | `true` | `false` | Không cho kẻ tấn công nhờ honeypot mở kết nối tới máy khác. Khi thử, Cowrie trả lỗi `unknown channel: b'direct-tcpip'` |
| 873 | `[telnet] enabled` | `false` | `true` | Đề tài cần hai dịch vụ SSH và Telnet |

**Làm sạch:** file không chứa bí mật nào. `backend_pass = root` là giá trị mẫu của chế độ proxy (không dùng); `[openai] API_KEY = xxxxx` là chỗ trống mẫu. Không đưa lên repo: `etc/userdb.txt` (xem bên dưới), khóa SSH của honeypot trong `var/lib/cowrie/ssh_host_*`.

**Dùng lại khi dựng lab:** sau `cowrie init`, chép file này đè lên `~/etc/cowrie.cfg`; hoặc làm theo Bước 7 của [README_chay_lab.md](../README_chay_lab.md) rồi tắt `forwarding`.

## Danh sách yếu tố mồi (cho TV3, BG-08)

"Mồi" là những gì honeypot cho kẻ tấn công thấy để tin rằng đây là máy thật. Cột "Đã kiểm" là những gì TV1 đã nhìn thấy khi chạy thử; các dòng còn lại lấy từ `cowrie.cfg`.

| Yếu tố | Giá trị | Mặc định / Đã đổi | Đã kiểm | Nơi chỉnh |
| --- | --- | --- | --- | --- |
| Shell giả lập | `backend = shell`: Cowrie tự giả lập lệnh, không có hệ điều hành thật phía sau | Mặc định | Có: `whoami` trả `labuser` | `[honeypot] backend` |
| Tên máy | `svr04`; dấu nhắc `labuser@svr04:~$` | Mặc định | Có | `[honeypot] hostname` |
| Banner SSH công bố | `SSH-2.0-OpenSSH_9.2p1 Debian-2+deb12u3` | Mặc định | Có: `ssh -v` từ Windows thấy `remote software version OpenSSH_9.2p1 Debian-2+deb12u3` | `[ssh] version` |
| Phiên bản do `ssh -V` trả trong shell giả | `OpenSSH_7.9p1, OpenSSL 1.1.1a 20 Nov 2018` | Mặc định | Có | `[shell] ssh_version` |
| Nhân hệ điều hành (`uname -a`) | `Linux svr04 6.1.0-21-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.90-1 (2024-05-03) x86_64 GNU/Linux` | Mặc định | Có | `[shell] kernel_version`, `kernel_build_string`, `hardware_platform`, `operating_system` |
| Lời chào sau khi đăng nhập | Lời chào của Debian GNU/Linux | Mặc định | Có | Hệ thống file giả (`/etc/motd`) |
| Hệ thống file giả | `fs.pickle` đi kèm gói Cowrie | Mặc định | Có: `ls /` ra cây thư mục Linux chuẩn | `[shell] filesystem` |
| Nội dung file giả (`cat /etc/passwd`...) | Thư mục `honeyfs` đi kèm gói | Mặc định | Có: `/etc/passwd` có `root`, `daemon`, `bin`... | `[honeypot] contents_path` |
| Tài khoản giả (`userdb`) | Chỉ chấp nhận `labuser` / `LabOnly-2026`; mọi cặp khác bị từ chối | **Đã đổi** (bản tạm, chờ BG-01 của TV4) | Có: cặp sai bị từ chối, cặp đúng vào được | `etc/userdb.txt` |
| Lời nhắc đăng nhập Telnet | `login:` rồi `Password:`; sai thì báo `Login incorrect` | Mặc định | Có | Mã nguồn Cowrie |
| Lệnh tải file | `wget`, `curl` được giả lập; ở lab này luôn thất bại vì không có đường ra | Mặc định | Có | Không chỉnh |
| SFTP | Bật | Mặc định | Chưa | `[ssh] sftp_enabled` |
| Thời gian chờ | Ngắt phiên rảnh sau 180 giây; ngắt bước đăng nhập sau 120 giây | Mặc định | Chưa | `[honeypot] idle_timeout`, `authentication_timeout` |

### Điểm lộ TV1 đã gặp khi chạy thử (đầu vào cho WP-13)

1. **Hai phiên bản OpenSSH không khớp nhau:** banner công bố bản 9.2p1, còn lệnh `ssh -V` trong shell giả trả bản 7.9p1. Cả hai đều là giá trị mặc định, và TV1 đã thấy tận mắt cả hai.
2. **Hệ điều hành lộ khác nhau:** VM-H thật là Ubuntu 24.04, nhưng shell giả nói là Debian. Kẻ tấn công từ bên ngoài không thấy được điều này, nhưng nên ghi rõ trong báo cáo.
3. **`wget` in "connected." rồi treo**, trong khi máy thật sẽ báo lỗi ngay.
4. **`curl -m 5 ...` báo `option -m not recognized`.** Tùy chọn này phổ biến, máy thật đều hỗ trợ.
5. **Tên máy `svr04` là giá trị mặc định nổi tiếng của Cowrie.** Công cụ dò honeypot thường kiểm tra tên này.

Nhóm có thể đổi các giá trị mặc định trên để honeypot giống thật hơn (hướng nâng cao trong kế hoạch). Mỗi lần đổi phải ghi lại vào bảng này và chụp snapshot mới.
