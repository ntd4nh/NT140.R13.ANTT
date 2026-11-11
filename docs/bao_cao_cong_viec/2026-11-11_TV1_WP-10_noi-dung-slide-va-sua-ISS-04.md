# Nội dung slide báo cáo tiến độ và sửa ISS-04

**Ngày:** 2026-11-11 · **Người làm:** TV1 · **Trạng thái:** Xong

Đã soạn bản nháp nội dung slide cho cả buổi báo cáo tiến độ, gồm 14 slide và phụ lục demo, để TV4 ghép và chỉnh. Đã sửa lỗi ISS-04 mà TV3 giao cho TV1.

## Đã làm gì
- Soạn `report/noi_dung_slide_bao_cao_tien_do.md`. Nội dung đi theo thứ tự: tổng quan đề tài → nguyên lý deception → hướng đi (Q1–Q3, phạm vi) → giải pháp (công cụ, kiến trúc lab, cách ly) → làm được đến đâu (log thật, bảng tiến độ, xử lý và kiểm chứng, điểm lộ) → vướng mắc → định hướng tiếp theo → câu hỏi xin góp ý.
- Mỗi slide ghi ba phần: chữ trên slide, hình/bảng, ý cần nói; kèm minh chứng trong repo.
- Số liệu lấy từ phần viết của TV1, TV3, báo cáo của TV2 và các file review. Thống nhất theo lưu ý của TV3: 58 sự kiện, 8 phiên (6 có đăng nhập, 2 dò cổng), 4/4 lần đăng nhập, 8 lệnh.
- Sửa ISS-04:
  - `docs/02_so_do_lab.md` mục 1: điền VMware Workstation 25H2.
  - `docs/01_quyet_dinh_pham_vi_cong_cu.md` mục 3.5: thay hai ghi chú "[cần xem trên máy thật]" bằng kết quả đã kiểm (chỉ `[output_jsonlog]` được bật; `forwarding = false`).
- Kiểm tra phần cấu hình trong ghi chú deception của TV3 (`docs/00` mục 4): 10 số dòng `cowrie.cfg` được trích dẫn đều khớp file thật.
- Cập nhật `report/TV1_lab.md`: thay "chờ TV3 review" bằng kết quả review đạt.

## Kết quả
- Sản phẩm: `report/noi_dung_slide_bao_cao_tien_do.md`; sửa `docs/01`, `docs/02`, `report/TV1_lab.md`; trạng thái ISS-04 trong `review/issues.md`.
- Đã kiểm tra bằng cách: đối chiếu từng số liệu trên slide với file nguồn ghi ở dòng "Minh chứng".

## Còn thiếu / vướng mắc
- Slide 4 (câu hỏi nghiên cứu) đang dùng bản nháp từ kế hoạch; TV4 cần chốt.
- Phần viết của TV2 chưa có trong `report/`. Slide 10 lấy số liệu từ báo cáo công việc của TV2 và review của TV3.
- Phiên thử riêng cho điểm lộ L3, L4, L5, L8 (TV3 đề xuất) chưa chạy, vì lab đang tắt.

## Liên quan tới người khác
- Bàn giao: BG-12 (phần TV1, gồm thêm bản nháp slide). BG-11: ISS-04 đã sửa, gửi lại TV3 kiểm.
- Cần review: **TV4** dùng và chỉnh bản nháp slide; **TV3** kiểm lại ISS-04 và rà soát slide (BG-13).

## Các thành viên khác cần biết
- **TV4:** bản nháp đã chia sẵn người trình bày theo F.4. Phần cần sửa trước khi trình bày ghi ở đầu file.
- **TV2:** nên viết phần mình vào `report/` để TV4 ghép; slide 10 là phần của TV2.
- **TV3:** phần cấu hình trong `docs/00` mục 4 đã được TV1 kiểm, đúng hết.
