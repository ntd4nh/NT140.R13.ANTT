# WP-03 – Hướng dẫn dựng lab (TV1)

**Ngày:** 2026-11-10 · **Người làm:** TV1 · **Trạng thái:** Xong một phần

Đã có hướng dẫn dựng lab kiểu cầm tay chỉ việc, người chưa từng dựng máy ảo cũng làm theo được. **Lab chưa được dựng**; bước tiếp theo là TV1 làm theo hướng dẫn trên máy.

## Đã làm gì
- Viết hướng dẫn 16 bước, có giải thích từ ngữ. Mỗi bước gồm: làm gì, sẽ thấy gì, lỗi thì sửa sao. Nội dung: tạo hai VM trên VMware, cài Ubuntu Server (từng màn hình), cài Cowrie bằng pip, bật Telnet, tạo `userdb.txt`, chuyển sang mạng host-only, bật firewall, chụp snapshot.
- Điều khiển VM qua SSH từ PowerShell để copy-paste được lệnh.
- Viết sẵn cách chạy smoke test từ hai nguồn, cách kiểm tra cách ly và cách lấy log về repo kèm hash.
- Có bảng xử lý sự cố thường gặp và checklist hoàn thành WP-03.

## Kết quả
- Sản phẩm: `Implement/lab/README_chay_lab.md`
- Đã kiểm tra bằng cách: chưa chạy thử trên máy thật. Các chỗ phải xem kết quả thật được đánh dấu **[kiểm tra]**.

## Còn thiếu / vướng mắc
- Chưa dựng lab, chưa có log smoke test.
- `userdb.txt` đang dùng bản tạm; chờ danh sách credential của TV4 (BG-01).

## Liên quan tới người khác
- Bàn giao: chưa đủ điều kiện cho BG-02, BG-03, BG-08; sẽ gửi khi dựng xong theo checklist mục 13.
- Đã đổi đường dẫn lab trong `BAN_GIAO.md` từ `lab/` sang `Implement/lab/`.
- Cần review: **TV3** có thể đọc trước hướng dẫn, để khi dựng lại lab (BG-03) dùng đúng file này.

## Các thành viên khác cần biết
- **TV4:** gửi sớm danh sách credential cho KB-02 và KB-05 (BG-01).
- **TV2:** log smoke test sẽ có cả SSH và Telnet, từ hai IP nguồn.
