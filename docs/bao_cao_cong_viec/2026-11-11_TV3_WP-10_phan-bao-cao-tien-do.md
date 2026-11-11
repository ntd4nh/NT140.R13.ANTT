# WP-10 – Phần báo cáo tiến độ của TV3

**Ngày:** 2026-11-11 · **Người làm:** TV3 · **Trạng thái:** Xong

Đã viết xong phần của TV3 cho báo cáo tiến độ, cùng khung với phần của TV1 để TV4 ghép.

## Đã làm gì
- Viết `report/TV3_review_deception.md` gồm: các dòng cho bảng B.3 và B.5, nội dung cho phần 1, 2, 4, 5, 6, 7 của slide, và lưu ý cho TV4 khi ghép.
- Thêm `review/tai_hien/doc_tty.py` (giải mã file TTY) để khẳng định "đã kiểm mồi bằng file TTY" chạy lại được.
- Đối chiếu đoạn log trong phần 4 của TV1 với `evidence/smoke_test/cowrie.json` dòng 22–32: khớp.

## Kết quả
- Sản phẩm: `report/TV3_review_deception.md`, `review/tai_hien/doc_tty.py`
- Đã kiểm tra bằng cách: rà từng khẳng định "đã làm" trong báo cáo → mỗi khẳng định đều trỏ tới file trong repo; việc chưa làm (kiểm cách ly độc lập, dựng lại lab, RUN-TEST, bảng điểm lộ chính thức) đều ghi "dự kiến".

## Còn thiếu / vướng mắc
- Không.

## Liên quan tới người khác
- Bàn giao: BG-12 (phần của TV3) → TV4: đã gửi. Dòng BG-12 có ba người gửi nên trạng thái giữ "Chưa" cho tới khi đủ phần của TV1, TV2, TV3.
- Cần review: TV4 dùng khi ghép (WP-10); TV3 rà soát lại bản ghép (BG-13).

## Các thành viên khác cần biết
- TV4: mục 4 của báo cáo có 5 lưu ý khi ghép, quan trọng nhất là không ghi lab "đạt mức cơ bản" khi chưa có biên bản cách ly độc lập (BG-04).
