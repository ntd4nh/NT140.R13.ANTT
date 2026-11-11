# KHAC – Đồng bộ công việc TV4 lên tv4 và main

**Ngày:** 2026-11-11 · **Người làm:** TV4 (có AI hỗ trợ) · **Trạng thái:** Xong

Đã commit 30 tệp công việc TV4, hợp nhất bản main mới nhất và push thành công cùng một commit lên `origin/tv4` và `origin/main`.

## Đã làm gì
- Kiểm tra các tệp thay đổi; không phát hiện khóa riêng, bí mật thật, file máy ảo, malware hay slide môn học trong tập tệp được commit.
- Tạo commit `1ebf547` cho kịch bản, script, minh chứng và báo cáo đang có của TV4.
- Hợp nhất `origin/main` tại `5c2667b` vào TV4, tạo commit `3da45cb`; Git tự hợp nhất, không có xung đột.
- Chạy `git push --atomic origin tv4:tv4 tv4:main` thành công; hai nhánh trên GitHub cùng trỏ tới `3da45cb` ở lần push này, không force-push.

## Kết quả
- Sản phẩm: toàn bộ 30 tệp trong commit `1ebf547`; bản hợp nhất ở `3da45cb`.
- Kiểm cú pháp 5 script trong `experiments/scripts/` bằng `python -I -m py_compile`: đạt.
- Chạy `.venv/Scripts/python.exe -m pytest -q`: 13 passed, 2 failed; cả hai lỗi báo `SHA256SUMS` không khớp fixture. Đây cũng là lỗi đã lưu tại `evidence/van_hanh_TV4/pytest_cuoi_phien.txt` trước lượt đồng bộ này.

## Còn thiếu / vướng mắc
- Hai lỗi kiểm thử fixture vẫn còn; lượt này không sửa code xử lý dữ liệu hay dữ liệu gốc.
- Script chạy lab chưa được kiểm chứng trên lab; chưa có RUN thực nghiệm, theo các báo cáo WP-06 và WP-09 hiện có.

## Liên quan tới người khác
- Việc vừa hoàn thành là KHAC – đồng bộ Git; không hoàn thành thêm WP nào và không tự đổi trạng thái bàn giao.
- Cần review: Bảng B không chỉ định người review cho bảo trì Git. Các yêu cầu review sản phẩm TV4 tiếp tục theo các báo cáo WP tương ứng.
- Nhật ký kiểm tra ngày 2026-11-11: sau khi viết báo cáo này, đã chạy `git pull --ff-only origin tv4` (Already up to date) và đọc lại `BAN_GIAO.md`. Bảng A không có dòng kích hoạt bởi đồng bộ Git; không phát sinh yêu cầu bàn giao/review mới cho việc KHAC này.

## Các thành viên khác cần biết
- Bản main mới của TV1 đã được giữ lại khi hợp nhất. Tài liệu TV4 vẫn phân biệt kết quả smoke test, sản phẩm chưa review và việc dự kiến làm trên lab.
