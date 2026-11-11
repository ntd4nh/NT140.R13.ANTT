# WP-09 – TV4 lặp phép đối chiếu trên log smoke test (TV4)

**Ngày:** 2026-11-11 · **Người làm:** TV4 (thực hiện, có AI hỗ trợ) · **Trạng thái:** Xong

Trên máy TV4, bộ xử lý của TV2 và phép đếm độc lập của TV3 cho cùng số liệu với báo cáo của TV3: **KHỚP**. Đây không phải RUN-TEST và không phải hoàn thành WP-09.

## Đã làm gì
- Tạo `.venv` trên máy host (Python 3.11.9, pandas 3.1.1), chạy `pytest analysis/tests`.
- Chép 4 mục trong manifest của `evidence/smoke_test/` ra thư mục tạm, kiểm hash, chạy bộ xử lý, chạy `review/tai_hien/dem_doc_lap.py`, kiểm lại hash log gốc.
- Tìm nguyên nhân 2 test lỗi.

## Kết quả
- Sản phẩm: `review/review_TV4_doi_chieu_smoke.md`, `evidence/doi_chieu_smoke_TV4/` (nhánh `tv4`, chưa commit).
- Đã kiểm tra bằng cách: `dem_doc_lap.py` → 58 sự kiện, 8 phiên, 4/4 đăng nhập thất bại/thành công, 8 lệnh, `KHỚP`, mã 0; `sha256sum -c` của `evidence/smoke_test` sau khi chạy → 3/3 OK.
- `pytest`: 13 passed, 2 failed. Nguyên nhân: `SHA256SUMS` của fixture minh họa tính trên bản CRLF, cây làm việc của TV4 là LF. Trên bản `git archive` (CRLF): 15 passed.

## Còn thiếu / vướng mắc
- Chỉ trên log smoke test; chưa có RUN để kiểm phần gắn kịch bản.

## Liên quan tới người khác
- Bàn giao: bỏ qua trong lượt này theo yêu cầu của TV4; người review theo Bảng B: TV3.
- Cần review: không bắt buộc (đây là phép lặp lại của TV4 đối với kết quả của TV3).

## Các thành viên khác cần biết
- TV2: nên thêm `analysis/tests/fixtures/** -text` vào `.gitattributes` hoặc để test tự sinh manifest fixture; nếu không, máy checkout dạng LF sẽ thấy 2 test đỏ. TV4 không sửa file của TV2.
