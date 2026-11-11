# KHAC – Đọc hiểu toàn bộ repo để chuẩn bị tạo prompt AI (TV4)

**Ngày:** 2026-11-11 · **Người làm:** TV4 · **Trạng thái:** Xong

Đã đọc toàn bộ 62 tệp dự án hiện có (không tính metadata `.git/`) để nắm bối cảnh trước khi thiết kế prompt; chưa tạo prompt mới hoặc triển khai thêm gói việc.

## Đã làm gì
- Kiểm kê cả tệp ẩn; đọc kế hoạch, prompt gốc, hướng dẫn, tài liệu, mã nguồn, cấu hình, fixture, log và báo cáo công việc qua phân công đọc song song.
- Phân biệt kế hoạch ngày 04/11 với minh chứng và review ngày 10–11/11; xác định trách nhiệm thực nghiệm, diễn giải và tổng hợp của TV4.
- Đọc log smoke test, giải mã bản ghi TTY và đối chiếu SHA-256; ghi nhận những điều kiện còn chờ trước RUN chính thức.

## Kết quả
- Sản phẩm: báo cáo này; bối cảnh tham chiếu từ `Plan/`, `Prompt/`, `docs/`, `Implement/`, `analysis/`, `evidence/`, `review/`, `report/` và các tệp ở gốc repo.
- Kiểm kê bằng `Get-ChildItem -Force -Recurse -File`: 62 tệp, tổng 533.478 byte trước khi thêm báo cáo này. Smoke test: 58/58 dòng JSON hợp lệ; 3/3 hash khớp manifest; TTY đọc được.
- `data/raw/`, `data/processed/`, `results/` chỉ có `.gitkeep`; chưa có `docs/03_kich_ban_thu_nghiem.md` hoặc `experiments/`. Không chạy lab, test hay pipeline trong lượt đọc.
- Sau khi viết báo cáo, đọc lại `BAN_GIAO.md` và chạy `git pull --ff-only` trên nhánh `tv4`: `Already up to date`.

## Còn thiếu / vướng mắc
- Không có PDF slide nguồn trong thư mục; chỉ đọc bản tổng hợp `docs/THONG_TIN_MON_HOC_NT140.md`, không xác nhận lại trích dẫn từ PDF.
- BG-04 chưa hoàn tất; chưa đủ điều kiện chạy WP-06. WP-04, phạm vi của TV4 và cách ghi nhật ký liên quan ISS-01 còn cần chuẩn bị. Một số trạng thái trong tài liệu cũ chưa khớp review mới.

## Liên quan tới người khác
- Bàn giao: việc KHAC này không hoàn thành WP-04, WP-06 hay WP-10, nên không kích hoạt BG-01, BG-06, BG-07 hoặc BG-13; không xác nhận nhận BG-12 và không đổi trạng thái bàn giao.
- Cần review: Bảng B không quy định reviewer cho việc đọc hiểu repo (KHAC); lượt đọc này không thay review WP-09/WP-13 thuộc trách nhiệm TV4.

## Các thành viên khác cần biết
- Smoke test thật và fixture minh họa không phải kết quả RUN-01/RUN-TEST chính thức. Thông tin chưa có minh chứng tiếp tục ghi “dự kiến”.
- Yêu cầu bàn giao/review của sản phẩm tiếp theo chỉ được soạn khi xác định WP và kiểm tra đủ điều kiện tương ứng.
