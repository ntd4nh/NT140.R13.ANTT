# Yêu cầu TV4 mở rộng kịch bản tấn công SSH/Telnet (TV1)

**Ngày:** 2026-11-22 · **Người làm:** TV1 (có AI hỗ trợ) · **Trạng thái:** Xong

Đã gửi TV4 yêu cầu bổ sung kịch bản, theo nhận xét của cô: tập trung vào tấn công SSH và Telnet, và thể hiện rõ vai trò của honeypot. RUN-01 sẽ chạy sau khi có kịch bản mới, để không phải chạy lại.

## Đã làm gì
- Đối chiếu kịch bản hiện có với các kiểu tấn công SSH phổ biến. Kịch bản hiện có mới phủ 4 giai đoạn, mỗi giai đoạn một kiểu, và chưa kịch bản nào tạo ra nhóm hành vi B5.
- Viết yêu cầu gồm:
  - 3 kịch bản SSH bắt buộc: rải mật khẩu, bot tự động không mở shell, duy trì truy cập và xóa dấu vết.
  - 1 kịch bản Telnet nên có: kiểu botnet IoT, chạy từ VM-A.
  - 1 kịch bản tùy chọn.
  - Mỗi kịch bản ghi rõ chứng minh được gì về honeypot, nhãn hành vi và ATT&CK ứng viên.
- Đọc `kb_vma.py`, `kb_host.py` của TV4: chỉ nhắm `192.168.239.20` cổng 2222/2223, chỉ dùng mật khẩu giả.
- Kiểm tra `analysis/process_run.py` không giới hạn `scenario_id`, nên mã KB mới không cần sửa code của TV2.

## Kết quả
- Sản phẩm: `docs/yeu_cau/2026-11-22_TV1-TV4_mo-rong-kich-ban.md`
- Đã kiểm tra bằng cách: đọc mã script của TV4 và TV2; đối chiếu sự kiện Telnet trong `evidence/smoke_test/cowrie.json`. Những điểm chưa có log làm căn cứ được ghi [XM] trong yêu cầu.

## Còn thiếu / vướng mắc
- RUN-01 chưa chạy; chờ TV4 bổ sung kịch bản và TV3 review.
- `report/BAO_CAO_TIEN_DO_GIUA_KY.md` (bản local, chưa từng commit) đã được chuyển vào Thùng rác theo yêu cầu của TV1. Hai báo cáo `2026-11-11_NHOM_WP-10_*` nói về file này vẫn còn trên máy TV1 và chưa commit.

## Liên quan tới người khác
- Bàn giao: không kích hoạt mã BG nào trong `BAN_GIAO.md`. Đây là yêu cầu đầu vào cho WP-04 của TV4.
- Cần review: TV3 review kịch bản mới sau khi TV4 viết xong.

## Các thành viên khác cần biết
- **TV4:** đọc yêu cầu và nhận việc. Phần bắt buộc là 3 kịch bản SSH.
- **TV2:** sẽ có thêm kịch bản KB-06 trở đi và nhóm B5; bộ phân loại cần nhận diện được rải mật khẩu và phiên tự động.
- **TV3:** review kịch bản mới trước khi chạy RUN-01.
