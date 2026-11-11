# Kiểm tra cách ly – lần tự kiểm của TV1 (WP-03, Bước 14)

**Ngày:** 2026-11-10, khoảng 14:46–14:50 UTC · **Kết quả:** ĐẠT

Đây là lần tự kiểm của TV1 sau khi dựng lab. TV3 vẫn phải kiểm tra lại độc lập và lập biên bản chính thức ở `review/kiem_tra_cach_ly.md` (BG-04).

## Trạng thái lúc kiểm tra

- VM-H chỉ có một card mạng, nối vào VMnet1 host-only (`192.168.239.0/24`). Không còn card NAT.
- Bảng định tuyến của VM-H chỉ có một dòng: `192.168.239.0/24 dev ens32`. Không có default route.
- ufw đang bật: `DEFAULT_INPUT_POLICY="DROP"`, `DEFAULT_OUTPUT_POLICY="DROP"`. Có 3 luật cho phép đi vào: 22/tcp chỉ từ `192.168.239.1`, 2222/tcp và 2223/tcp từ `192.168.239.0/24`.
- VMware: Shared Folders tắt, drag and drop và copy-paste tắt, CD/DVD không tự gắn, đã gỡ Sound Card và USB.

## Lệnh và kết quả

**Trên VM-H (user `labadmin`):**

| Lệnh | Kết quả | Đạt? |
| --- | --- | --- |
| `ping -c 2 -W 2 8.8.8.8` | `ping: connect: Network is unreachable` | Đạt |
| `curl -m 5 https://example.com` | `curl: (6) Could not resolve host: example.com` | Đạt |
| `curl -m 5 http://93.184.215.14` | `curl: (7) Failed to connect ... Couldn't connect to server` | Đạt |
| Mở TCP tới `1.1.1.1:443` | `Network is unreachable` | Đạt |
| Mở TCP tới máy host `192.168.239.1:445` | Thất bại (ufw chặn chiều ra) | Đạt |

**Trong shell giả của honeypot** (đăng nhập `labuser` qua cổng 2222 từ VM-A):

| Lệnh | Shell giả hiển thị | Thực tế (log VM-H) | Đạt? |
| --- | --- | --- | --- |
| `wget http://example.com` | `failed: Temporary failure in name resolution` | Không phân giải được tên | Đạt |
| `curl http://93.184.215.14` | Không in gì | `cowrie.session.file_download.failed`; `cowrie.log` ghi `NoRouteError: Network is unreachable` | Đạt |
| `wget http://93.184.215.14/x.sh` | `Connecting to 93.184.215.14:80... connected.` rồi treo | `cowrie.session.file_download.failed`; `NoRouteError: Network is unreachable` | Đạt |

Thư mục `var/lib/cowrie/downloads/` vẫn trống sau khi thử.

**Từ VM-A tới cổng quản trị của VM-H:**

| Lệnh | Kết quả | Đạt? |
| --- | --- | --- |
| `ssh -o ConnectTimeout=5 labadmin@192.168.239.20` | `connect to host 192.168.239.20 port 22: Connection timed out` | Đạt |
| Mở TCP tới 2222 và 2223 | Mở được (đúng thiết kế) | Đạt |

## Ghi chú cho TV3

- Lệnh `wget` của shell giả **in ra "connected."** dù thực tế không kết nối được. Đây là output giả do Cowrie dựng sẵn; muốn biết thật hay không phải xem log. Đồng thời đây là một **điểm lộ** cho WP-13: máy thật sẽ báo lỗi ngay chứ không treo.
- Shell giả không hiểu tùy chọn `curl -m` (`curl: option -m not recognized`). Đây cũng là một điểm lộ.
- Mặc định Cowrie để `[ssh] forwarding = true`, nghĩa là kẻ tấn công có thể nhờ honeypot mở kết nối tới máy khác. Ở lab này ufw chặn mọi chiều ra nên không đi đâu được; TV1 sẽ tắt tùy chọn này để có thêm một lớp bảo vệ. Khi kiểm tra lại, TV3 nên xác nhận giá trị trong `cowrie.cfg`.
- Log của các lệnh thử trên nằm sau log smoke test và **không** thuộc `evidence/smoke_test/`.
