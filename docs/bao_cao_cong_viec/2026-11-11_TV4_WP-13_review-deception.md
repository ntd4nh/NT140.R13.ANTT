# WP-13 – Review ghi chú deception của TV3 (TV4)

**Ngày:** 2026-11-11 · **Người làm:** TV4 (thực hiện, có AI hỗ trợ) · **Trạng thái:** Xong

Ghi chú deception của TV3 **đạt có lưu ý**: mọi trích dẫn log và cấu hình đúng (1 trích dẫn lệch dòng nhỏ); có 9 điểm nên sửa, không có lỗi mức chặn.

## Đã làm gì
- Mở từng dòng `json:<dòng>` được trích trong `evidence/smoke_test/cowrie.json`, đọc cả sự kiện cùng phiên; kiểm từng dòng `cfg:<dòng>`; giải mã TTY bằng `review/tai_hien/doc_tty.py`.
- Tự tải `cowrie.cfg.dist` ở tag `v3.1.6` (commit `ea9513e`) từ GitHub chính thức và `diff` với `Implement/lab/cowrie/cowrie.cfg` → chỉ khác dòng 813, 873, khớp kết luận của TV3.
- Phân loại căn cứ của các yếu tố mồi và L1–L8 (cấu hình / log / TTY / người khác quan sát / dự kiến); tìm câu khẳng định rộng hơn căn cứ.

## Kết quả
- Sản phẩm: `review/review_TV4_WP-13_deception.md` (nhánh `tv4`, chưa commit).
- Đã kiểm tra bằng cách: lệnh và output trong `evidence/van_hanh_TV4/2026-11-11.md` (GĐ0, GĐ1).

## Còn thiếu / vướng mắc
- Chưa kiểm cấu hình đang chạy trên VM-H (lab không có trên máy TV4); L3–L5, L7, L8 chưa có log.
- Đây là review ghi chú và quan sát ban đầu, không phải bảng điểm lộ O7 chính thức từ RUN.

## Liên quan tới người khác
- Bàn giao: bỏ qua trong lượt này theo yêu cầu của TV4; người review theo Bảng B: TV3 (TV3 là người nhận kết quả review; Bảng B không có dòng riêng cho bản review của TV4).
- Cần review: không bắt buộc. TV1 vẫn cần kiểm phần cấu hình (mục 4 của ghi chú).

## Các thành viên khác cần biết
- 4 câu nên ghi là giả thuyết/cơ chế, không phải kết quả: "mọi tương tác đều đáng ngờ", "tỉ lệ báo động giả thấp", "mồi càng thật kẻ tấn công càng ở lâu", "chỉ lỗi trong Cowrie mới chạm được máy thật".
- Banner 9.2p1 chỉ thấy ở transcript phía client (`ssh -v`); `cowrie.json` không ghi đầu ra lệnh.
