# Phần báo cáo của TV1 và xác minh schema cho TV2

**Ngày:** 2026-11-10 · **Người làm:** TV1 · **Trạng thái:** Xong

Đã trả lời 10 câu hỏi xác minh mà TV2 để lại trong hợp đồng dữ liệu, bằng log smoke test thật. Đã viết xong phần báo cáo tiến độ của TV1 để TV4 ghép.

## Đã làm gì
- Chạy đúng các lệnh `jq` của TV2 (`docs/04_hop_dong_du_lieu.md` mục 10) trên bản sao của log smoke test. Liệt kê các trường có ở mọi sự kiện và các trường riêng của từng loại sự kiện.
- Gõ thêm một lệnh không tồn tại vào honeypot để có sự kiện `command.failed` thật, vì log smoke test không có loại này.
- Viết phần TV1 cho báo cáo tiến độ, gồm các dòng cho bảng B.3, B.5, nội dung cho phần 2–7 của slide và kịch bản demo.

## Kết quả
- Sản phẩm:
  - `evidence/xac_minh_hop_dong_du_lieu.md`
  - `report/TV1_lab.md`
- Đã kiểm tra bằng cách:
  - Kiểm hash bản sao trước khi chạy `jq`.
  - Chạy thử lệnh `jq` dùng cho demo trên VM-H.
  - Mọi con số trong phần báo cáo đều đối chiếu lại với log.

## Còn thiếu / vướng mắc
- Chưa xác minh được tên file JSON sau khi xoay vòng, vì chưa có lượt nào chạy qua nửa đêm.
- Telnet Client của Windows cần quyền quản trị để bật; TV1 tự bật.

## Liên quan tới người khác
- Bàn giao: BG-12 cần đủ phần viết của TV1, TV2 và TV3 mới gửi được. Phần của TV1 đã xong, chưa đổi trạng thái.
- Cần review: **TV3** đọc `report/TV1_lab.md`; **TV2** đọc `evidence/xac_minh_hop_dong_du_lieu.md`.

## Các thành viên khác cần biết
- **TV2:**
  - Mọi sự kiện đều có `protocol`, `dst_ip`, `dst_port`, `src_port`.
  - `duration_ms` có ở cả `session.closed` và `log.closed`; `shasum` có ở `log.closed`. Phải lọc theo `eventid` trước khi lấy các trường này.
  - `client.version` có thể là chuỗi rỗng.
  - Lệnh có thật nhưng dùng tùy chọn lạ thì không sinh `command.failed`.
- **TV4:** phần TV1 ở `report/TV1_lab.md` đã viết theo dàn ý I.1, có sẵn đoạn log và ma trận nguồn × dịch vụ để đưa lên slide.
