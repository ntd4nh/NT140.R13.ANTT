# Khung nhận xét – WP-08, phần diễn giải của TV4 (DỰ KIẾN)

**Người viết:** TV4 (có AI hỗ trợ) · **Ngày:** 2026-11-11 · **Trạng thái:** **khung, chưa có kết quả.** Chưa có lượt chạy RUN nào (`data/raw/` chỉ có `.gitkeep`), nên mọi nhận xét dưới đây là **dự kiến**: chỉ ghi sẽ quan sát gì, bằng dữ liệu nào, để trả lời câu hỏi nào.

Không dùng log smoke test hay dữ liệu minh họa (`analysis/tests/fixtures/`) thay cho RUN. Khi có RUN, bản thật đặt ở `results/<RUN>/nhan_xet.md` và file này giữ nguyên làm khung.

Mỗi nhận xét khi viết thật phải đủ 4 phần: **quan sát → số liệu/sự kiện kèm đường dẫn (`raw_ref`, bảng) → ý nghĩa với Q1/Q2/Q3 → giới hạn hoặc cách giải thích khác.** Câu hỏi Q1–Q3: `docs/01_quyet_dinh_pham_vi_cong_cu.md` mục 1.

## 1. Các nhận xét dự kiến

| # | Sẽ quan sát | Dữ liệu cần | Trả lời | Giới hạn đã biết trước |
| --- | --- | --- | --- | --- |
| N1 | Độ đầy đủ của thu thập: bao nhiêu bước trong nhật ký có sự kiện khớp, bao nhiêu bước không có sự kiện riêng và kiểm bằng cách khác | `experiments/doi_chieu_<RUN>.csv` (đếm theo `trang_thai`); `events.csv` | Q1 (O5) | Kịch bản do nhóm tự đặt, biết trước sự kiện mong đợi; tỉ lệ khớp cao chỉ nói về khả năng ghi của Cowrie với thao tác thông thường |
| N2 | Dựng lại diễn biến phiên KB-03: thứ tự 11 lệnh, khoảng cách thời gian, thời lượng phiên | Bảng O4 (`results/<RUN>/`), `sessions.csv` (`duration_ms` của `session.closed`), file TTY | Q2 (O1, O4) | Lệnh do script gõ đều nhịp, không phản ánh nhịp gõ của người thật |
| N3 | Khác biệt giữa SSH và Telnet, giữa hai nguồn: tập sự kiện mỗi loại phiên (ví dụ `client.version`, `client.kex` chỉ có ở SSH) | Bảng O6 (phiên và lần đăng nhập **tách riêng**), `events.csv` | Q1, Q2 (O6) | Mỗi ô của ma trận chỉ có 1–2 phiên |
| N4 | Điểm lộ của shell giả: phản hồi khác máy thật ở KB-03, banner SSH so với `ssh -V`, lệnh có `command.failed` | Transcript `KB-01_*`, `KB-03_honeypot`, `KB-03_VM-A_that`; số `cowrie.command.failed` | Q1 phần deception (O7) | Bảng điểm lộ chính thức là việc của TV3 (WP-13); TV4 chỉ nêu quan sát. Không đo được kẻ tấn công thật có nhận ra hay không |
| N5 | Nhóm hành vi và observable mô tả được từ dữ liệu: B1 (chỉ kết nối), B2 (thử đăng nhập), B3 (khám phá sau đăng nhập); credential giả, lệnh | `results/<RUN>/behavior.csv`, `observable.csv` (WP-11) | Q3 (O3, H.6–H.8) | Nhãn mô tả **hành vi mô phỏng theo kịch bản**, không phải ý định kẻ tấn công. So nhãn với kịch bản chỉ là kiểm trên tình huống đã biết |

## 2. Giới hạn chung phải nêu khi viết thật

- **Cỡ mẫu:** một lượt chạy cơ bản dự kiến có 6 phiên, 10 lần đăng nhập, 15 lệnh (`docs/03_kich_ban_thu_nghiem.md` mục 0.4). Không đủ để nói về tần suất hay xu hướng.
- **Nguồn dữ liệu:** do thành viên nhóm tạo theo kịch bản trong lab cô lập. Không suy rộng ra kẻ tấn công trên Internet. IP `192.168.239.x` là máy của nhóm, **không phải IOC độc hại**.
- **Shell giả lập:** `backend = shell`; đầu ra lệnh do Cowrie tự tạo, không phải hệ điều hành thật.
- **Nguồn thời gian:** giờ sự kiện theo đồng hồ VM-H; giờ nhật ký theo đồng hồ máy nguồn; độ lệch đo ở `experiments/<RUN>/do_lech_gio.md`; bộ xử lý dùng một δ cho cả hai nguồn (`experiments/quy_uoc_nhat_ky.md` mục 5).
- **Gắn kịch bản:** ghi số phiên theo từng trạng thái `matched / unmatched / ambiguous / needs_review`; ISS-01 vẫn mở.
- **Chưa quan sát được:** tải tệp (KB-04), SFTP, chuyển tiếp cổng (đã tắt), phiên dài quá `idle_timeout`.

## 3. Bằng chứng còn thiếu để viết bản thật

| Cần có | Ai | Trạng thái |
| --- | --- | --- |
| Phép kiểm cách ly trước lượt (của TV4) và biên bản độc lập của TV3 (BG-04) | TV4; TV3 | Chưa có |
| `data/raw/<RUN>/` (log gốc, TTY, `run_note.txt`, `SHA256SUMS`) | TV4 + TV1 | Chưa có |
| `experiments/nhat_ky_thu_nghiem.csv`, `experiments/transcript/<RUN>/`, `experiments/<RUN>/do_lech_gio.md` | TV4 | Chưa có |
| `experiments/doi_chieu_<RUN>.csv` | TV4 | Chưa có (script sẵn: `experiments/scripts/doi_chieu.py`) |
| `data/processed/<RUN>/` và kết quả `review/tai_hien/dem_doc_lap.py` | TV2 chạy; TV4 kiểm | Chưa có |
| Bảng O1, O4, O6 (`results/<RUN>/`) | TV2 (BG-09) | Chưa có |
| `behavior.csv`, `observable.csv`, `attack_mapping.md` | TV4 (WP-11) | Chưa có |
