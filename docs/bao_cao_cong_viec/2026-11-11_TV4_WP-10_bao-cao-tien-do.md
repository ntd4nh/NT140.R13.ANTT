# WP-10 – Ghép báo cáo tiến độ (TV4)

**Ngày:** 2026-11-11 · **Người làm:** TV4 (thực hiện, có AI hỗ trợ) · **Trạng thái:** Xong một phần

Đã ghép bản đầu của báo cáo tiến độ (Markdown, 7 phần theo I.1); chưa có slide, chưa có phần tự viết của TV2, chưa được TV3 rà soát.

## Đã làm gì
- Lập bảng hiện trạng repo (sản phẩm từng người, trạng thái ghi trong file, đã review chưa, 10 mâu thuẫn giữa các file).
- Ghép phần của TV1, TV3; dựng phần TV2 từ mã và minh chứng đã review, ghi rõ không phải lời của TV2; áp dụng 5 lưu ý của TV3 và các điểm review WP-13.
- Tách log smoke test khỏi lượt chạy theo kịch bản (chưa có); viết khung nhận xét WP-08 ở dạng dự kiến.

## Kết quả
- Sản phẩm: `report/bao_cao_tien_do.md`, `results/khung_nhan_xet_du_kien.md`, `evidence/van_hanh_TV4/hien_trang_GD0.md` (nhánh `tv4`, chưa commit).
- Đã kiểm tra bằng cách: script kiểm đường dẫn trong các file `.md` mới → mọi đường dẫn trỏ tới file có thật, trừ các file **dự kiến** tạo khi chạy RUN (`experiments/nhat_ky_thu_nghiem.csv`, `evidence/kiem_tra_cach_ly_TV4/`) và file được ghi là "không có"; ma trận nguồn × dịch vụ tính lại từ `sessions.csv` của smoke test.

## Còn thiếu / vướng mắc
- Chưa có RUN, nên phần 5 chỉ có kết quả smoke test và mong đợi; chưa có bảng O1/O4/O6.
- TV2 chưa gửi phần viết; slide chưa làm (bỏ trong lượt này theo yêu cầu của TV4).

## Liên quan tới người khác
- Bàn giao: bỏ qua trong lượt này theo yêu cầu của TV4; người review theo Bảng B: TV3.
- Cần review: TV3 (rà soát cuối).

## Các thành viên khác cần biết
- Lab chưa đạt nhãn "cơ bản" theo I.1 vì chưa có kiểm tra cách ly độc lập và chưa ai dựng lại lab; báo cáo ghi đúng như vậy.
