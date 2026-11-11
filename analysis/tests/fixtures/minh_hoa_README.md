# Fixture minh họa

Dữ liệu MINH HỌA tự soạn, KHÔNG phải log thật, chưa đối chiếu Cowrie thật; không dùng trong kết quả.

Các sự kiện chỉ mô phỏng những event và trường được liệt kê ở mục 3.1 của
`docs/01_quyet_dinh_pham_vi_cong_cu.md`. Cấu trúc này chưa được xác nhận với
phiên bản Cowrie trong lab. Các địa chỉ `192.0.2.10`, `192.0.2.1` và
`192.0.2.20` thuộc TEST-NET, dùng để phân biệt dữ liệu minh họa với log lab.

`minh_hoa_RUN-TEST/` chứa hai phần của một log minh họa: `cowrie.json` và file
xoay vòng `cowrie.json.2026-01-01`. `SHA256SUMS` được sinh từ hai file này.
Trong tổng số 50 dòng vật lý có 48 dòng JSON đọc được (trong đó có một dòng
trùng hoàn toàn), một dòng JSON hỏng bị cắt giữa chừng và một dòng trống.

Các bẫy có chủ ý: eventid lạ, thiếu `src_ip`, thiếu `timestamp`, sự kiện đến
không theo thứ tự thời gian, và timestamp mang hậu tố `Z` hoặc `+00:00`.
Fixture cũng có một kết nối không có `cowrie.session.closed`.

`minh_hoa_nhat_ky_thu_nghiem.csv` dùng đúng các cột mẫu H.2.
`minh_hoa_nhat_ky_gan_kich_ban.csv` là nhật ký nhỏ tổng hợp để kiểm tra khớp
kịch bản đơn, không khớp và khớp nhiều. Tất cả nội dung trong fixture chỉ phục
vụ viết và kiểm thử bộ xử lý; không đại diện cho kết quả thực nghiệm hay log
Cowrie thật.
