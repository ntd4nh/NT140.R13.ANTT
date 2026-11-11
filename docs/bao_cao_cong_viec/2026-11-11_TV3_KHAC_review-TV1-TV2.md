# Review sản phẩm TV1 (WP-01, WP-02, WP-03) và TV2 (WP-05, WP-07) (TV3)

**Ngày:** 2026-11-11 · **Người làm:** TV3 · **Trạng thái:** Xong một phần

Review xong phần làm được trong repo: không có lỗi mức chặn, ghi 4 lỗi (1 trung bình, 3 thấp). Chưa dựng lại lab và chưa kiểm tra cách ly độc lập.

## Đã làm gì
- TV1: kiểm 12 link nguồn của WP-01; review sơ đồ lab theo RV-THIẾT-KẾ; so cấu hình Cowrie với bản mặc định chính thức theo RV-CẤU-HÌNH.
- TV2: chạy lại test và bộ xử lý trên máy TV3; viết phép đếm độc lập `review/tai_hien/dem_doc_lap.py` (chỉ thư viện chuẩn) và so với đầu ra; thử các ca biên (hash sai, ghi vào raw, JSON hỏng, dòng trùng, event lạ, file xoay vòng, gắn kịch bản).
- Chuẩn bị biên bản kiểm tra cách ly với đủ lệnh và kết quả mong đợi, để trống cột kết quả.

## Kết quả
- Sản phẩm: `review/review_TV1_WP-01_WP-02_WP-03.md`, `review/review_TV2_WP-05_WP-07.md`, `review/issues.md`, `review/kiem_tra_cach_ly.md`, `review/tai_hien/`
- Đã kiểm tra bằng cách:
  - `pytest` → 15 passed.
  - Chạy bộ xử lý 2 lần trên bản sao smoke test → giống hệt từng byte; đếm độc lập → khớp 58 sự kiện, 8 phiên, 4/4 đăng nhập, 8 lệnh.
  - `git status` sạch, `sha256sum -c` OK sau mọi lần chạy.

## Còn thiếu / vướng mắc
- Dựng lại lab theo README và kiểm tra cách ly (BG-04) cần thao tác tay trên VMware: **dự kiến**.
- WP-09 (`RUN-TEST` trên lab thật) chờ lab và kịch bản của TV4 (`docs/03_kich_ban_thu_nghiem.md` chưa có).

## Liên quan tới người khác
- Bàn giao: nhận BG-03 và BG-10. BG-11 → TV2 (ISS-01..03) và TV1 (ISS-04): đã gửi. BG-04: chưa đủ điều kiện vì chưa kiểm tra cách ly.
- Cần review: TV1 kiểm tra lại biên bản cách ly sau khi TV3 chạy; TV4 lặp lại một phép đối chiếu (chạy `dem_doc_lap.py`).

## Các thành viên khác cần biết
- **TV2, TV4 (ISS-01):** kịch bản chỉ có một dòng nhật ký sẽ không khớp được phiên khi δ nhỏ. Cần chốt cách ghi nhật ký (dòng bắt đầu + kết thúc) hoặc thêm dung sai trước RUN-01.
- Cấu hình Cowrie trên repo đúng là bản mặc định + 2 dòng như TV1 ghi.
