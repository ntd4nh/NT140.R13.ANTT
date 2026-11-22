# WP-04 – Mở rộng kịch bản tấn công SSH/Telnet (TV4)

**Ngày:** 2026-11-22 · **Người làm:** TV4 (Thực nghiệm, tổng hợp) · **Trạng thái:** Xong (bản đề xuất, chờ TV3 review; chưa chạy lab)

Đã thêm 4 kịch bản mới theo yêu cầu của TV1 (`docs/yeu_cau/2026-11-22_TV1-TV4_mo-rong-kich-ban.md`): 3 kịch bản SSH bắt buộc (KB-06 rải mật khẩu, KB-07 bot tự động, KB-08 duy trì truy cập/xóa dấu vết) và 1 kịch bản Telnet nên có (KB-09 botnet IoT từ VM-A). Mỗi KB chứng minh thêm một điều về honeypot, không chỉ thêm số liệu.

## Đã làm gì

- **`docs/03`:** thêm mục đầy đủ cho KB-06, KB-07, KB-08, KB-09 (mục tiêu, nguồn→đích, bảng bước, sự kiện mong đợi, đơn vị đếm, đạt/không đạt, nhãn H.6, ATT&CK) và ghi chú KB-10 (tùy chọn, chưa làm). Cập nhật mục 0.2 (tài khoản giả), 0.4 (thứ tự RUN và tổng mong đợi: **13 phiên; 13 login.failed, 6 login.success; 27 command.input**).
- **`experiments/scripts/kb_vma.py`:** thêm hàm `kb06`/`kb07`/`kb08`/`kb09` và một lớp Telnet tự chứa (socket + xử lý IAC) cho KB-09 chạy từ VM-A; thêm `--kb KB-06..KB-09`, `--eol`.
- **Quy ước nhật ký + Plan:** bổ sung `scenario_id` KB-06..KB-09; thêm nhãn kỳ vọng KB-06..KB-09 vào H.6 và bảng ánh xạ KB→ATT&CK ở H.8 (trạng thái *dự kiến*).
- Ghi rõ **[XM]** mọi chỗ còn phụ thuộc hành vi thật của Cowrie (ghi lệnh exec của KB-07, hỗ trợ `crontab`/`history` của KB-08, số lần thử Telnet của KB-09).

## Kết quả

- Sản phẩm: `docs/03_kich_ban_thu_nghiem.md`, `experiments/scripts/kb_vma.py`, `experiments/quy_uoc_nhat_ky.md`, `experiments/scripts/README.md`, `Plan/…H.6/H.8` (commit sẽ ghi khi push nhánh `tv4`).
- Đã kiểm tra bằng cách:
  - `python -I -m py_compile` cả 3 script → không lỗi cú pháp.
  - **Dựng log Cowrie tổng hợp + nhật ký** cho KB-06..KB-09 (thư mục tạm, không lưu repo) rồi chạy `doi_chieu.py --delta-seconds 1` → **50 `khop`, 11 `khong_co_su_kien_rieng`, 0 `khong_khop`, 0 `mo_ho`**: nhãn nhật ký của 4 KB mới khớp bộ đối chiếu (rải mật khẩu gán đúng 4 phiên; `CLIENT_TU_NGAT` của bot gán `session.closed`; `GUI_USERNAME`/`GUI_MAT_KHAU` Telnet tách đúng; `command.failed` của KB-08 được gán). Đây chỉ là kiểm **logic đối chiếu**, không thay cho log thật.

## Còn thiếu / vướng mắc

- **Chưa chạy vào honeypot** (lab không có trên máy TV4). Các điểm **[XM]** phải xác nhận ở **phiên chuẩn bị** trước RUN-01, nhất là: Cowrie ghi phiên `exec` của KB-07 ra sao (một `command.input`? có file TTY?), Cowrie có hỗ trợ `crontab`/`history` không (KB-08), Telnet cho thử mấy lần/kết nối (KB-09 — nếu chỉ 2 thì bỏ cặp giả thứ hai).
- `userdb.txt` **giữ nguyên một dòng** `labuser:x:LabOnly-2026`: mọi username giả của KB-06/KB-09 phải bị từ chối; cặp hợp lệ của KB-09 (`labuser`/`LabOnly-2026`) đóng vai "cặp mặc định đoán trúng". Không đổi userdb; nếu muốn đổi phải báo TV1 trước.

## Liên quan tới người khác

- **Bàn giao BG-01 → TV1:** danh sách credential cho mọi KB đã chốt, không có mật khẩu thật, định dạng userdb = một dòng. Đủ điều kiện (xem `BAN_GIAO.md`).
- **Báo TV1:** kịch bản mở rộng đã xong; **RUN-01 có thể chạy sau khi TV3 review và phiên chuẩn bị đạt** (RUN-01 chờ bản này — mục 6 của yêu cầu).
- **Cần review:** TV3 (Bảng B: kịch bản, nhật ký, bảng đối chiếu).

## Các thành viên khác cần biết

- Bộ xử lý của TV2 **không** cần sửa: `analysis/process_run.py` lấy `scenario_id` từ nhật ký, không hard-code KB-01..KB-05 (đã kiểm mã).
- Tổng mong đợi một RUN cơ bản đã đổi: 13 phiên / 19 lần đăng nhập / 27 `command.input` (chi tiết ở `docs/03` mục 0.4) — TV2 dùng khi đối chiếu số liệu RUN-01.
