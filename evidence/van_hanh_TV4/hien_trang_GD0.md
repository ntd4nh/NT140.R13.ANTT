# Bảng hiện trạng repo lúc bắt đầu phiên (Giai đoạn 0)

**Người lập:** TV4, có AI hỗ trợ · **Ngày:** 2026-11-11, khoảng 10:46–10:50 UTC
**Căn cứ:** nhánh `tv4` @ `9c75ec0`. `origin/main` @ `1d115d3` không có commit nào chưa có trong `tv4` (`git log HEAD..origin/main` rỗng; `git diff --ignore-cr-at-eol` chỉ khác 1 báo cáo KHAC của TV4). Hai nhánh `origin/tv2-*` không có thêm file trong `report/`, `results/`, `experiments/`, `data/`.

Bảng chỉ ghi điều đọc được trong file. "Review" nghĩa là có file review của người khác; "tự kiểm" không tính là review.

## 1. Sản phẩm theo thành viên

| TV | Sản phẩm | Có? | Trạng thái ghi trong file | Đã review? Bằng file nào |
| --- | --- | --- | --- | --- |
| TV1 | WP-01 phần công cụ – `docs/01_quyet_dinh_pham_vi_cong_cu.md` mục 2–6 | Có | Dòng 3: "đã soạn, chờ TV3 review" | Có: `review/review_TV1_WP-01_WP-02_WP-03.md` mục 1 – Đạt |
| TV1 | WP-02 – `docs/02_so_do_lab.md` | Có | Dòng 3: "đã dựng thật đúng thiết kế, chờ TV3 review" | Có: cùng file review, mục 2 – Đạt; 2 mục ⚠️ (NAT, user chạy Cowrie) mới dựa vào tài liệu của TV1 |
| TV1 | WP-03 – `Implement/lab/README_chay_lab.md`, `Implement/lab/cowrie/` | Có | README Bước 16 đã điền; Phụ lục 6 còn 1 ô chưa tick (snapshot) | Có: cùng file review, mục 3 – cấu hình Đạt; "README làm lại được" ⏳ (TV3 chưa dựng lại) |
| TV1 | WP-03 – log smoke test `evidence/smoke_test/` | Có | "Kết quả: ĐẠT" | TV2 tự kiểm khi nhận BG-02 (`BAN_GIAO.md`, nhật ký 10/11 15:32); TV3 chạy đếm độc lập trên bản sao (`review/review_TV2_WP-05_WP-07.md` mục 1) |
| TV1 | Tự kiểm cách ly – `evidence/kiem_tra_cach_ly_TV1.md` | Có | "Kết quả: ĐẠT" (tự kiểm) | **Chưa có kiểm độc lập**: `review/kiem_tra_cach_ly.md` ghi "CHƯA THỰC HIỆN"; BG-04 "Chưa" |
| TV1 | Trả lời xác minh schema – `evidence/xac_minh_hop_dong_du_lieu.md` | Có | – | Dùng trong review WP-05 của TV3 |
| TV1 | WP-10 phần TV1 – `report/TV1_lab.md` | Có | – | Chưa có review. Nhật ký `BAN_GIAO.md` không có dòng "BG-12 TV1 → TV4 Đã gửi" |
| TV2 | WP-05 – `docs/04_hop_dong_du_lieu.md` | Có | Dòng 3: "chờ TV3 review (BG-05 chưa gửi)"; mục 11: "Chưa" | Có: `review/review_TV2_WP-05_WP-07.md` mục 2 – Đạt (ISS-03) |
| TV2 | WP-07 – `analysis/process_run.py`, `analysis/README.md`, `analysis/tests/` | Có | Báo cáo công việc: "Hoàn thành, BG-10 đã gửi TV3" | Có: cùng file review, mục 1 – Đạt (ISS-01, ISS-02). Chưa chạy trên RUN thật |
| TV2 | WP-08 bảng O1, O4, O6 – `results/RUN-xx/` | **Không** | – | – (`results/` chỉ có `.gitkeep` ở mọi nhánh) |
| TV2 | WP-10 phần TV2 – `report/` | **Không** | – | – |
| TV3 | Review TV1, TV2 – `review/review_TV1_*.md`, `review/review_TV2_*.md` | Có | "Đạt, không có lỗi mức chặn" | Chưa có người review lại (Bảng B không bắt buộc) |
| TV3 | Danh sách lỗi – `review/issues.md` | Có | ISS-01 (Trung bình), ISS-02, ISS-03, ISS-04 (Thấp): đều "Mở" | – |
| TV3 | Biên bản cách ly – `review/kiem_tra_cach_ly.md` | Có khung | "CHƯA THỰC HIỆN" | – |
| TV3 | Công cụ tái hiện – `review/tai_hien/` (`dem_doc_lap.py`, `doc_tty.py`, `nhat_ky_smoke_tv3.csv`) | Có | – | – |
| TV3 | WP-13 – `docs/00_nguyen_ly_deception_telemetry.md` | Có | Dòng 3: "chờ TV4 review, TV1 kiểm tra phần cấu hình (mục 4)" | **Chưa** – TV4 review trong phiên này |
| TV3 | WP-09 – `RUN-TEST`, `review/kiem_thu_tich_hop.md` | **Không** | – | – |
| TV3 | WP-10 phần TV3 – `report/TV3_review_deception.md` | Có | BG-12 TV3 → TV4 "Đã gửi" (nhật ký 11/11 06:18) | Chưa |
| TV4 | WP-01 phần phạm vi – `docs/01_quyet_dinh_pham_vi_cong_cu.md` mục 1 | **Không** (chỉ có chỗ trống) | "[TV4 điền …]" | – |
| TV4 | WP-04 – `docs/03_kich_ban_thu_nghiem.md`, `experiments/` | **Không** | BG-01 "Chưa" | – |
| TV4 | WP-06 – `data/raw/RUN-xx/`, nhật ký, bảng đối chiếu | **Không** | BG-06, BG-07 "Chưa" | – |
| TV4 | WP-08 nhận xét, WP-10 báo cáo ghép, WP-11 | **Không** | BG-13 "Chưa" | – |
| TV4 | Review WP-13, lặp phép đối chiếu WP-09 | **Không** | – | – |
| TV4 | Báo cáo KHAC: đọc hiểu repo, merge main, soạn prompt | Có | "Xong" | – (Bảng B không quy định) |

## 2. Mâu thuẫn giữa các file (chỉ ghi lại, không tự chọn bản nào)

| # | Nội dung | File A | File B | Ghi chú |
| --- | --- | --- | --- | --- |
| M1 | Trạng thái review WP-01 | `docs/01_…` dòng 3: "chờ TV3 review" | `review/review_TV1_WP-01_WP-02_WP-03.md`: đã review, Đạt | Trạng thái trong `docs/01_quyet_dinh_pham_vi_cong_cu.md` lỗi thời |
| M2 | Trạng thái review WP-02 | `docs/02_so_do_lab.md` dòng 3: "chờ TV3 review" | Cùng file review, mục 2 | Như M1 |
| M3 | Trạng thái BG-05 | `docs/04_…` dòng 3 và mục 11: "chưa gửi"/"Chưa" | `BAN_GIAO.md` Bảng A dòng 64: "Đã gửi" | TV3 đã ghi là ISS-03 |
| M4 | Trạng thái review trong phần báo cáo của TV1 | `report/TV1_lab.md` B.3 dòng 2, 3: "Chờ TV3 review" | File review của TV3 | TV3 đã nêu ở lưu ý 1 của `report/TV3_review_deception.md` |
| M5 | Cấu hình lúc chạy smoke test | `evidence/smoke_test/README.md` dòng 13: "chỉ đổi `[telnet] enabled = true`" | `Implement/lab/cowrie/README.md`: đổi 2 dòng, gồm `forwarding = false` | TV3 review mục 3: smoke test chạy **trước** khi tắt `forwarding` (README lab Phụ lục 3). Nghĩa là `cowrie.cfg` trong repo không đúng y cấu hình lúc smoke test |
| M6 | Snapshot | README lab Phụ lục 6: ô "Snapshot …" chưa tick | README lab Phụ lục 3: nêu tên `sau-smoke-test`, `sau-cai-cowrie`, `sau-cai-dat` | Không rõ snapshot đã chụp đủ chưa |
| M7 | Phiên bản VMware | `docs/02_so_do_lab.md` mục 1: "`<phiên bản>`" | `docs/02_so_do_lab.md` mục 8: "25H2" | TV3 đã ghi là ISS-04 |
| M8 | Ghi chú "[cần xem trên máy thật]" | `docs/01_quyet_dinh_pham_vi_cong_cu.md` mục 3.5 | `Implement/lab/cowrie/cowrie.cfg` dòng 813, 944 | ISS-04 |
| M9 | Trích dẫn `[proxy]` | `docs/00_nguyen_ly_deception_telemetry.md` dòng 23: "`[proxy]`, `cfg:364`" | `cowrie.cfg`: tiêu đề `[proxy]` ở dòng 359, dòng 364 là `backend = pool` | Lệch nhỏ, không đổi ý |
| M10 | BG-12 | `report/TV1_lab.md` đã có | `BAN_GIAO.md` nhật ký: chỉ có TV3 gửi BG-12 | TV2 chưa có phần viết |

## 3. Hệ quả cho phiên này

- WP-13 chờ TV4 review → làm ở Giai đoạn 1.
- BG-04 "Chưa", biên bản cách ly độc lập của TV3 chưa có. Theo prompt, TV4 chỉ được chạy RUN khi **phép kiểm của chính TV4** đạt ở Giai đoạn 2; kết quả đó không thay biên bản của TV3.
- Không có bảng O1/O4/O6 của TV2 ở bất kỳ nhánh nào. Nếu có RUN thật thì TV4 tự làm bảng và ghi rõ không phải sản phẩm TV2.
- Lab được dựng trên **máy TV1** (`docs/02_so_do_lab.md` mục 1, `report/TV3_review_deception.md` phần 6). Máy này là máy TV4; cần kiểm ở Giai đoạn 2.
