# Biên bản kiểm tra cách ly (WP-03, BG-04)

**Người kiểm:** TV3 · **Người kiểm tra lại biên bản:** TV1
**Trạng thái:** **CHƯA THỰC HIỆN.** Bảng dưới là các lệnh sẽ chạy; cột kết quả để trống cho tới khi chạy thật. Không điền kết quả từ biên bản tự kiểm của TV1 (`evidence/kiem_tra_cach_ly_TV1.md`).

Cách làm: mở lab theo `Implement/lab/README_chay_lab.md` (Phụ lục 1), chạy từng lệnh, **chép nguyên văn** dòng kết quả quan trọng vào cột "Kết quả thực tế". Kết quả mong đợi của mọi thử kết nối ra ngoài là **thất bại**. Nếu một lệnh thành công: dừng thử nghiệm, tắt VM-H, ghi vào `review/issues.md` mức **Chặn** và báo TV1.

- Ngày, giờ bắt đầu (UTC, `date -u`): ……
- Máy chạy lab: …… (máy TV1 / máy TV3 dựng lại theo README)
- Snapshot VM-H đang dùng: ……
- Phiên bản Cowrie (`~/cowrie-env/bin/cowrie version` hoặc dòng `Cowrie Version` trong `cowrie.log`): ……

## 1. Trạng thái VM-H

| # | Lệnh (trên VM-H, user quản trị) | Mong đợi | Kết quả thực tế | Đạt? |
| --- | --- | --- | --- | --- |
| 1.1 | VMware → VM-H → Settings → Network Adapter | Chỉ một card, Host-only (VMnet1); không có NAT/Bridged | | |
| 1.2 | `ip route` | Chỉ có dòng subnet lab, **không có** `default via` | | |
| 1.3 | `sudo ufw status verbose` | `deny (incoming), deny (outgoing)`; chỉ 3 luật: 22 từ `.1`, 2222 và 2223 từ subnet lab | | |
| 1.4 | `ps -eo user,cmd \| grep [c]owrie` | Tiến trình Cowrie chạy bằng user `cowrie`, không phải `root` | | |
| 1.5 | `sudo -u cowrie grep -nE '^(forwarding\|enabled) *=' /home/cowrie/etc/cowrie.cfg` | `forwarding = false`; chỉ `[ssh]`, `[telnet]`, `[output_jsonlog]` bật | | |
| 1.6 | VMware → VM-H → Settings → Options | Shared Folders, drag and drop, copy-paste đều tắt | | |

## 2. Thử kết nối ra ngoài từ VM-H

| # | Lệnh | Mong đợi | Kết quả thực tế | Đạt? |
| --- | --- | --- | --- | --- |
| 2.1 | `ping -c 2 -W 2 8.8.8.8` | `Network is unreachable` hoặc mất 100% gói | | |
| 2.2 | `curl -m 5 https://example.com` | Không phân giải được tên | | |
| 2.3 | `curl -m 5 http://1.1.1.1` | Không kết nối được | | |
| 2.4 | `timeout 5 bash -c '</dev/tcp/1.1.1.1/443' ; echo $?` | Mã khác 0 | | |
| 2.5 | `timeout 5 bash -c '</dev/tcp/192.168.239.1/445' ; echo $?` | Mã khác 0 (ufw chặn chiều ra cả trong lab) | | |
| 2.6 | `timeout 5 bash -c '</dev/tcp/192.168.239.10/22' ; echo $?` | Mã khác 0 | | |

## 3. Thử từ shell giả của honeypot

Đăng nhập từ VM-A: `ssh -p 2222 labuser@192.168.239.20` (mật khẩu giả trong `userdb.txt`).

| # | Lệnh trong shell giả | Mong đợi | Màn hình hiển thị | Log VM-H (`cowrie.json`, `cowrie.log`) | Đạt? |
| --- | --- | --- | --- | --- | --- |
| 3.1 | `wget http://example.com` | Không tải được | | | |
| 3.2 | `curl http://1.1.1.1` | `cowrie.session.file_download.failed`; `cowrie.log` báo không có đường | | | |
| 3.3 | `wget http://1.1.1.1/x.sh` | Như 3.2 (màn hình có thể in "connected." giả – xem log, không tin màn hình) | | | |
| 3.4 | Từ VM-A: `ssh -p 2222 -N -L 8080:1.1.1.1:80 labuser@192.168.239.20`, rồi ở terminal khác `curl -m 5 http://127.0.0.1:8080` | Bị từ chối (`forwarding = false`) | | | |
| 3.5 | Sau khi thử: `ls /home/cowrie/var/lib/cowrie/downloads/` trên VM-H | Thư mục trống | | | |

## 4. Cổng quản trị

| # | Lệnh | Mong đợi | Kết quả thực tế | Đạt? |
| --- | --- | --- | --- | --- |
| 4.1 | Từ VM-A: `ssh -o ConnectTimeout=5 <user quản trị>@192.168.239.20` | Timeout | | |
| 4.2 | Từ host `.1`: cùng lệnh | Kết nối được | | |

## 5. Kết luận

- Kết quả chung: …… (ĐẠT chỉ khi mọi dòng ở mục 2, 3, 4.1 thất bại đúng như mong đợi)
- Giờ kết thúc (UTC): ……
- Log của lần kiểm này **không** đưa vào `data/raw/`; nếu lưu làm minh chứng thì để ở `evidence/kiem_tra_cach_ly_TV3/` kèm `SHA256SUMS`.
- TV1 kiểm tra lại biên bản: …… (tên, ngày, đồng ý / ý kiến)
