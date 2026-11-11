# Script thực nghiệm của TV4 (WP-04, WP-06)

**Người viết:** TV4 (có AI hỗ trợ) · **Ngày:** 2026-11-11

> **Trạng thái:** các script chạy vào lab (`kb_vma.py`, `kb_host.py`, `do_lech_gio.py`) **chưa chạy thử trên lab**, vì lab không có trên máy TV4 (`evidence/van_hanh_TV4/2026-11-11.md`, Giai đoạn 2). Mới kiểm cú pháp (`python -m py_compile`). Phải chạy **phiên chuẩn bị** và đọc log Cowrie trước khi dùng cho RUN thật. `doi_chieu.py` đã thử trên bản sao log smoke test với nhật ký thử (mục 3).

Mọi script chỉ dùng thư viện chuẩn của Python, chỉ nhắm `192.168.239.20` cổng 2222/2223 (và cổng quản trị 22 của hai VM cho `do_lech_gio.py`). Mật khẩu trong script là **mật khẩu giả của lab** (`docs/03_kich_ban_thu_nghiem.md` mục 0.2).

## 1. Danh sách

| Script | Chạy ở | Việc |
| --- | --- | --- |
| `kb_vma.py` | VM-A (`python3`, dùng `pty`) | KB-01, KB-02, KB-03 vào honeypot; `KB-03-THAT` chạy cùng 11 lệnh trên VM-A thật trong `script` + `bash --noprofile --norc` (không ghi nhật ký H.2) |
| `kb_host.py` | Máy host Windows chạy lab | KB-05 Telnet (socket, tự xử lý byte IAC); KB-01 lặp lại qua SSH (ssh của Git for Windows + `SSH_ASKPASS` không trả mật khẩu) |
| `do_lech_gio.py` | Máy host | Đo lệch giờ VM-A, VM-H so với host, 5 lần, lấy trung vị; ghi `experiments/<RUN>/do_lech_gio.md` |
| `gop_nhat_ky.py` | Máy host | Gộp `nhat_ky_VM-A.csv`, `nhat_ky_Host.csv` vào `experiments/nhat_ky_thu_nghiem.csv` (chỉ thêm dòng) |
| `doi_chieu.py` | Máy host | Lập `experiments/doi_chieu_<RUN>.csv` từ log gốc + nhật ký (không dùng mã `analysis/`) |

Mỗi script ghi giờ UTC đúng lúc gửi thao tác và ghi transcript thô. Quy ước cột và nhãn `thao_tac`: `experiments/quy_uoc_nhat_ky.md`.

## 2. Trình tự một RUN (trên máy có lab)

Các bước có `sudo` phải do người có quyền tự chạy; script không nhận mật khẩu.

1. Kiểm cách ly (phép kiểm của TV4, theo các lệnh trong `review/kiem_tra_cach_ly.md`), lưu vào `evidence/kiem_tra_cach_ly_TV4/`. Không điền vào biên bản của TV3.
2. Chép script sang VM-A qua cổng quản trị: `scp experiments/scripts/kb_vma.py labadmin@192.168.239.10:~/tv4/`.
3. **Phiên chuẩn bị** (trước khi xoay log, không thuộc RUN), mỗi kịch bản một lần với `--run CHUAN-BI` và thư mục `--out` riêng. Đọc `cowrie.json` trên VM-H để xác nhận: cặp sai bị từ chối, cặp đúng vào được, số lần thử đúng thiết kế, KB-01 **không** có `cowrie.login.*`, Telnet cho thử 3 lần trong một kết nối.
4. `python experiments/scripts/do_lech_gio.py --run RUN-xx --nhan truoc`.
5. Xoay log có kiểm soát trên VM-H (prompt TV4 mục 7.2.5; cần sudo). Không chạy qua 00:00 UTC.
6. Chạy theo thứ tự, nghỉ ≥ `max(10 s, 2×|δ| + 2 s)` giữa hai kịch bản cùng nguồn, cùng cổng:
   ```text
   VM-A:  python3 ~/tv4/kb_vma.py --run RUN-xx --kb KB-01 --out ~/tv4/RUN-xx
   VM-A:  python3 ~/tv4/kb_vma.py --run RUN-xx --kb KB-02 --out ~/tv4/RUN-xx
   VM-A:  python3 ~/tv4/kb_vma.py --run RUN-xx --kb KB-03 --out ~/tv4/RUN-xx
   Host:  python experiments/scripts/kb_host.py --run RUN-xx --kb KB-05 --out experiments/RUN-xx/host
   Host:  python experiments/scripts/kb_host.py --run RUN-xx --kb KB-01 --out experiments/RUN-xx/host
   VM-A:  python3 ~/tv4/kb_vma.py --run RUN-xx --kb KB-03-THAT --out ~/tv4/RUN-xx
   ```
7. `python experiments/scripts/do_lech_gio.py --run RUN-xx --nhan sau`.
8. Xuất log về `data/raw/RUN-xx/`, viết `run_note.txt` một dòng, tạo `SHA256SUMS` **cuối cùng** (prompt TV4 mục 7.4).
9. Lấy `~/tv4/RUN-xx/` từ VM-A về; chép transcript vào `experiments/transcript/RUN-xx/` kèm `README.md`; rà transcript trước khi lưu.
10. `python experiments/scripts/gop_nhat_ky.py --run RUN-xx <nhat_ky_VM-A.csv> <nhat_ky_Host.csv>`.
11. `python -I experiments/scripts/doi_chieu.py --run-dir data/raw/RUN-xx --logbook experiments/nhat_ky_thu_nghiem.csv --out experiments/doi_chieu_RUN-xx.csv --transcript-dir experiments/transcript/RUN-xx`; tự kiểm bằng tay ít nhất 5 dòng thuộc các kịch bản khác nhau.
12. `.venv` python `-m analysis.process_run --run-dir data/raw/RUN-xx --logbook experiments/nhat_ky_thu_nghiem.csv`; rồi `python -I review/tai_hien/dem_doc_lap.py data/raw/RUN-xx data/processed/RUN-xx`.

Một kịch bản chạy sai: dừng lượt, vẫn xuất RUN đó và ghi "lượt chưa đạt", chạy lại toàn bộ trong RUN mới.

## 3. Đã kiểm gì

| Script | Cách kiểm | Kết quả |
| --- | --- | --- |
| Cả 5 script | `python -I -m py_compile` | Không lỗi cú pháp |
| `doi_chieu.py` | Chạy trên bản sao `evidence/smoke_test` (thư mục tạm) với một **nhật ký thử** dựng quanh mốc giờ trong `evidence/smoke_test/README.md` (không lưu vào repo), `--delta-seconds 0.5` | 6 phiên có đăng nhập gán đúng từng bước: 40 dòng `khop`, 16 dòng `khong_co_su_kien_rieng` (dòng mốc, gửi username), 2 phiên chỉ dò cổng `khong_khop` vì nhật ký thử không có dòng cho chúng. Tổng 40 sự kiện được gán + 13 sự kiện phụ + 5 sự kiện của 2 phiên dò cổng = 58 dòng log |
| `doi_chieu.py` – ca âm | Đổi một mật khẩu trong nhật ký thử; chạy với δ = 10 s; chạy thiếu δ | Mật khẩu lệch → `khong_khop`; cửa sổ chồng nhau → `mo_ho`; thiếu δ → dừng, mã 1 |
| `kb_vma.py`, `kb_host.py`, `do_lech_gio.py` | Chưa chạy | **Dự kiến** kiểm ở phiên chuẩn bị trên máy có lab |

Rủi ro cần xem ở phiên chuẩn bị: chuỗi dấu nhắc thật của Cowrie (`password:`, `login:`, `$ `); Telnet nhận `\r\n` hay `\n` (`--eol`); ssh của Git for Windows có chạy được askpass dạng `.sh` không; `kb_host.py` KB-01 dừng ssh bằng `taskkill /T` trước khi askpass trả về.
