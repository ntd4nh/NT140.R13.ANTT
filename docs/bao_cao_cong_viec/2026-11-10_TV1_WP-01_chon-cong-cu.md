# WP-01 – Chọn công cụ honeypot (TV1)

**Ngày:** 2026-11-10 · **Người làm:** TV1 (AI agent soạn, chờ TV1 xác nhận) · **Trạng thái:** Xong một phần

Đã chốt công cụ: **Cowrie** (SSH + Telnet) là chính, **OpenCanary** là dự phòng. Phần phạm vi của TV4 và xác nhận trường dữ liệu của TV2 vẫn chưa có.

## Đã làm gì
- Đọc tài liệu chính thức của Cowrie, OpenCanary, Dionaea và so sánh.
- Trả lời 5 câu hỏi của WP-01: Cowrie ghi gì, log ở đâu, cài thế nào, cần quyền gì, tính năng nào có thể kết nối ra ngoài.
- Lập bảng: hành vi muốn quan sát → sự kiện Cowrie → trường dữ liệu.

## Kết quả
- Sản phẩm: `docs/01_quyet_dinh_pham_vi_cong_cu.md`
- Đã kiểm tra bằng cách: mỗi nhận định về công cụ có link tài liệu chính thức ở cuối file. Chưa cài thử trên máy thật.

## Còn thiếu / vướng mắc
- Phần 1 (câu hỏi và phạm vi) chờ TV4 điền.
- Bảng trường dữ liệu chờ TV2 xác nhận.
- Hai điểm chỉ xem được khi cài: các plugin xuất log và tùy chọn SSH forwarding trong `cowrie.cfg`.

## Liên quan tới người khác
- Bàn giao: WP-01 không kích hoạt bàn giao nào trong `BAN_GIAO.md`.
- Cần review: **TV3**, kiểm tra từng nhận định có link nguồn.

## Các thành viên khác cần biết
- **Phải tạo `etc/userdb.txt` riêng.** Mặc định Cowrie chấp nhận gần như mọi mật khẩu. TV4 gửi danh sách credential cho TV1 (BG-01).
- VM honeypot cần **Python ≥ 3.11**: dùng Ubuntu 24.04 hoặc Debian 12 trở lên.
