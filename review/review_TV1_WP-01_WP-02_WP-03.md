# Review sản phẩm của TV1: WP-01 (phần công cụ), WP-02, WP-03 (cấu hình, README)

**Người review:** TV3 · **Ngày:** 2026-11-11 · **Commit được review:** `cec6308`
**Kết luận:** **Đạt, không có lỗi mức chặn.** Có 1 lỗi mức thấp (ISS-04). Phần tái lập lab và kiểm tra cách ly độc lập **chưa làm** (mục 4).

Ký hiệu: ✅ đạt, đã kiểm thật · ⚠️ đạt nhưng có ghi chú · ⏳ chưa kiểm được, ghi lý do.

## 1. WP-01 – Kiểm tra nguồn của quyết định công cụ

| Mục kiểm | Kết quả | Căn cứ |
| --- | --- | --- |
| Mỗi nhận định về công cụ có link nguồn chính thức | ✅ | 12 link trong mục "Nguồn" đều thuộc trang chính thức (docs.cowrie.org, github.com/cowrie, thinkst/opencanary, DinoTools/dionaea) |
| Link còn truy cập được | ✅ | `curl -L` ngày 2026-11-11: cả 12 link trả HTTP 200 |
| `userdb.example` mặc định chấp nhận gần như mọi cặp (`*:x:*`), chỉ từ chối root với `root`, `123456`, chuỗi chứa "honeypot" | ✅ | Đọc file trong gói `cowrie-3.1.6-py3-none-any.whl` |
| Chỉ bật output JSON ghi file | ✅ | Trong `cowrie.cfg` chỉ có `[ssh]`, `[telnet]`, `[output_jsonlog]` là `enabled = true`. Ghi chú "[cần xem trên máy thật]" nên gỡ (ISS-04) |

## 2. RV-THIẾT-KẾ – `docs/02_so_do_lab.md`

| Mục kiểm | Kết quả | Căn cứ |
| --- | --- | --- |
| Sơ đồ khớp IP/cổng thật | ✅ | IP `.1`, `.10`, `.20` và cổng 2222/2223 khớp `src_ip`, `dst_ip`, `dst_port` trong `evidence/smoke_test/cowrie.json` |
| Honeypot không có NAT khi thử nghiệm | ⚠️ | Thiết kế đúng; bằng chứng hiện là tự kiểm của TV1 (bảng định tuyến không có default route). TV3 chưa kiểm độc lập (mục 4) |
| Cổng quản trị tách cổng honeypot | ✅ | sshd :22 chỉ cho `.1`; Cowrie :2222/:2223. TV1 thử từ VM-A vào :22 bị timeout |
| Cowrie không chạy bằng root | ⚠️ | README Bước 6 tạo user `cowrie`; README smoke test ghi chạy bằng user `cowrie`. TV3 chưa xem trên máy (`ps -eo user,cmd | grep [c]owrie`) |
| Log được sao chép ra ngoài | ✅ | Mục 7: `scp` qua :22 về `data/raw/RUN-xx/` + `SHA256SUMS`; smoke test đã làm đúng cách này, hash khớp (`sha256sum -c`: 3/3 OK) |
| Không có credential thật | ✅ | Chỉ có tài khoản giả `labuser`; cấu hình không chứa khóa (mục 3) |
| Trả lời được "dữ liệu đi từ đâu tới đâu, ai truy cập được" | ✅ | Sơ đồ mục 3 + bảng mục 4 |

## 3. RV-CẤU-HÌNH – `Implement/lab/cowrie/`

| Mục kiểm | Kết quả | Căn cứ |
| --- | --- | --- |
| Liệt kê thay đổi so với mặc định | ✅ | TV3 tải `cowrie==3.1.6` (`pip download --no-deps`), so `cowrie.cfg.dist` với `cowrie.cfg` (bỏ khác biệt CRLF): **chỉ khác dòng 813 và 873**, đúng như bảng trong `Implement/lab/cowrie/README.md` |
| Mỗi thay đổi có lý do | ✅ | `forwarding = false`: thêm một lớp chặn kết nối ra; Telnet: đề tài cần hai dịch vụ |
| Bản đưa lên repo đã bỏ thông tin nhạy cảm | ✅ | Các giá trị dạng khóa/mật khẩu trong `cowrie.cfg` (`backend_pass`, `[output_s3]`, `[output_splunk]`, ...) đều là giá trị mẫu của file mặc định và nằm trong mục `enabled = false`. Không có `ssh_host_*` trong repo |
| README làm lại được | ⏳ | README đủ 16 bước, có phần "Nếu lỗi", phụ lục snapshot và xử lý sự cố. Chỉ xác nhận được khi TV3 dựng lại thật (mục 4) |
| Danh sách yếu tố mồi (BG-08) | ✅ | Có đủ shell giả lập, hệ thống file giả, tên máy, phiên bản SSH, `userdb`, ghi mặc định/đã đổi. TV3 kiểm lại bằng cấu hình và file TTY: `docs/00_nguyen_ly_deception_telemetry.md` mục 4 |

Ghi chú: smoke test chạy **trước** khi tắt `forwarding` (README lab, Phụ lục 3: snapshot `sau-cai-cowrie` là bản trước khi tắt). Dữ liệu smoke test không bị ảnh hưởng, nhưng từ RUN-01, `run_note.txt` nên ghi `config_version` để phân biệt.

## 4. Chưa làm: tái lập lab và kiểm tra cách ly độc lập

Kế hoạch WP-03 yêu cầu TV3 dựng lại (hoặc chạy lại) lab theo README và tự kiểm tra cách ly. Việc này cần thao tác tay trên VMware nên **chưa làm**. Biên bản đã chuẩn bị sẵn lệnh: `review/kiem_tra_cach_ly.md`. Khi làm xong, BG-04 mới đủ điều kiện gửi.
