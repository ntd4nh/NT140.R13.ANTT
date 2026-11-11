# WP-06 – Chuẩn bị chạy RUN: kiểm lab và script tự động hóa (TV4)

**Ngày:** 2026-11-11 · **Người làm:** TV4 (thực hiện, có AI hỗ trợ) · **Trạng thái:** Bị chặn

**Chưa chạy RUN nào.** Lab không có trên máy TV4, nên dừng ở bước kiểm lab. Phần làm được: script tự động hóa và script đối chiếu, sẵn để chạy trên máy có lab.

## Đã làm gì
- Kiểm lab trên máy TV4 (chỉ đọc): `vmrun list` → 0 VM chạy; inventory VMware không có `VM-H`, `VM-A`; host không có card VMnet nào, không có `192.168.239.1`. Không bật VM nào.
- Viết `experiments/scripts/`: `kb_vma.py` (KB-01/02/03 và đối chứng trên VM-A), `kb_host.py` (KB-05 Telnet, KB-01 lặp), `do_lech_gio.py`, `gop_nhat_ky.py`, `doi_chieu.py`, kèm README có trình tự một RUN.
- Tách bước "mở kết nối"/"gửi mật khẩu" ở KB-03, KB-05 trong `docs/03_kich_ban_thu_nghiem.md` và thêm nhãn `thao_tac` vào quy ước nhật ký, để bảng đối chiếu đọc được bằng script.

## Kết quả
- Sản phẩm: `experiments/scripts/` (nhánh `tv4`, chưa commit); nhật ký lệnh: `evidence/van_hanh_TV4/2026-11-11.md`.
- Đã kiểm tra bằng cách: `py_compile` 5/5 script. `doi_chieu.py` chạy trên bản sao smoke test với nhật ký **thử** (chỉ ở thư mục tạm): 6 phiên có đăng nhập gán đúng từng bước; 3 ca âm (mật khẩu lệch, cửa sổ chồng nhau, thiếu δ) cho kết quả đúng.
- `kb_vma.py`, `kb_host.py`, `do_lech_gio.py`: **chưa chạy thử**.

## Còn thiếu / vướng mắc
- Cần máy có lab (máy TV1), quyền quản trị `labadmin` không phải gõ mật khẩu vào lệnh (ví dụ khóa SSH tạm), và người có sudo cho bước xoay log, `ufw`.
- Kiểm cách ly của TV4 và biên bản độc lập của TV3 (BG-04) đều chưa có.

## Liên quan tới người khác
- Bàn giao: bỏ qua trong lượt này theo yêu cầu của TV4; người review theo Bảng B: TV3.
- Cần review: TV3 (script ghi nhật ký và bảng đối chiếu); TV1 hỗ trợ khi chạy trên máy TV1.

## Các thành viên khác cần biết
- KB-01 từ Windows dùng `SSH_ASKPASS` không trả mật khẩu; nếu askpass thoát lỗi, ssh có thể gửi mật khẩu rỗng. Phiên chuẩn bị phải xác nhận không có `login.failed` ở KB-01.
