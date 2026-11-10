# WP-05/WP-07 – Khung và fixture minh họa (TV2)

**Ngày:** 2026-11-10 · **Người làm:** TV2 · **Trạng thái:** Xong một phần

Đã tạo khung phân tích và fixture tổng hợp để phát triển, kiểm thử trước khi có log thật; chưa chốt schema hay hoàn thành script xử lý.

## Đã làm gì
- Tạo `analysis/`, `data/raw/`, `data/processed/`, `results/` cùng README, requirements và test.
- Tạo log Cowrie minh họa gồm file xoay vòng, SHA-256, nhật ký H.2 và các bẫy dữ liệu theo yêu cầu.
- Ghi rõ fixture không phải log thật và không dùng trong kết quả.

## Kết quả
- Sản phẩm: `analysis/`, `data/`, `results/`, `analysis/tests/fixtures/`.
- Đã kiểm tra bằng `python -m pytest analysis\tests -q` → 1 passed; fixture có 48 dòng JSON đọc được, 1 dòng hỏng, 1 dòng trống, 1 bản ghi trùng; có 11 session, trong đó 1 kết nối thiếu `session.closed`.
- Đã kiểm tra SHA-256 cho hai file log và xác nhận `data/raw/` chỉ có `.gitkeep`.

## Còn thiếu / vướng mắc
- Cần log smoke test thật để đối chiếu trường Cowrie và hoàn tất hợp đồng dữ liệu; fixture hiện chỉ dùng phát triển/kiểm thử.
- Chưa có script xử lý WP-07.

## Liên quan tới người khác
- Bàn giao: BG-02 chưa đủ điều kiện vì chưa có log smoke test thật; BG-05 và BG-10 chưa kích hoạt.
- Cần review: TV3 sau khi có schema/script tương ứng.

## Các thành viên khác cần biết
- Toàn bộ dữ liệu trong `analysis/tests/fixtures/` là minh họa, không đưa vào phân tích kết quả.
- `data/raw/` chưa chứa log thật; không tạo thư mục `RUN-xx`.
