# Báo cáo tiến độ – Đề tài 13: Honeypot thu thập và phân tích hành vi tấn công

**NT140.R13.ANTT** · Nhóm 4 thành viên (TV1–TV4) · **Bản ghép của TV4** (có AI hỗ trợ), ngày 2026-11-11
**Trạng thái:** bản ghép đầu tiên, **chưa được TV3 rà soát**. Chưa có slide.

**Nguồn ghép:** phần tự viết của TV1 (`report/TV1_lab.md`) và TV3 (`report/TV3_review_deception.md`). **TV2 chưa có phần tự viết**; các dòng về TV2 dưới đây dựng từ mã và minh chứng trong repo đã được TV3 review và TV4 chạy lại, có ghi nguồn, không phải lời của TV2. Mọi "đã làm" có đường dẫn minh chứng; việc chưa có minh chứng ghi **dự kiến**. Bảng hiện trạng dùng để ghép: `evidence/van_hanh_TV4/hien_trang_GD0.md`.

---

## 1. Đề tài, nguyên lý deception, câu hỏi và phạm vi

**Đề tài** (`Project.md`): hiểu nguyên lý deception và cách honeypot tạo security telemetry phục vụ nghiên cứu hành vi kẻ tấn công. Nhóm dựng một honeypot trong lab cô lập, tự tạo tương tác có kiểm soát, thu log và phân tích theo nguồn, dịch vụ bị nhắm, thao tác và diễn biến.

**Deception và telemetry** (ghi chú của TV3: `docs/00_nguyen_ly_deception_telemetry.md`; TV4 review: `review/review_TV4_WP-13_deception.md`):

- Honeypot là tài nguyên giả, không có người dùng hợp lệ, nên mọi tương tác với nó đều **đáng quan sát**. Giá trị nằm ở **mồi** (thứ làm người tương tác tin là máy thật) và **telemetry** (dữ liệu ghi được khi họ tương tác).
- Nhóm chọn mức tương tác **trung bình**: Cowrie `backend = shell` cho đăng nhập vào shell giả lập, đủ để quan sát lệnh; rủi ro kiểm soát bằng cách ly mức máy ảo. Cowrie vẫn tải tệp thật khi gặp `wget`/`curl`, nên cách ly là bắt buộc.
- Mỗi lớp tương tác sinh một nhóm sự kiện, cùng mang mã phiên. Ví dụ trong log thật `evidence/smoke_test/cowrie.json`: kết nối (`session.connect`, dòng 1), chuỗi phiên bản client SSH (`client.version`, dòng 7), thử mật khẩu (`login.failed`, dòng 9; `login.success`, dòng 14), lệnh (`command.input`, dòng 18), bản ghi màn hình (`log.closed` → file TTY, dòng 20), đóng phiên (`session.closed`, dòng 21).
- Các ý "ít báo động giả", "làm chậm kẻ tấn công", "mồi càng thật kẻ tấn công càng ở lâu" là **cơ chế/giả thuyết thường nêu**; dữ liệu lab của nhóm không đo và không kiểm chứng được chúng.

**Câu hỏi** (bản đề xuất của TV4, **chưa được nhóm thống nhất**: `docs/01_quyet_dinh_pham_vi_cong_cu.md` mục 1):

- **Q1.** Với kết nối, đăng nhập, lệnh và tải tệp có kiểm soát, Cowrie ghi được gì, chi tiết tới đâu? Thao tác hay phản hồi nào cho thấy giới hạn hoặc điểm lộ của shell giả?
- **Q2.** Có dựng lại được diễn biến từng phiên và đối chiếu khớp với nhật ký thực nghiệm (nguồn, dịch vụ, thứ tự thao tác, thời gian) không?
- **Q3.** Từ dữ liệu thu được, mô tả được những nhóm hành vi và observable nào; tới đâu thì đủ căn cứ đề xuất mapping ATT&CK?

**Phạm vi:** một Cowrie chế độ shell; SSH (2222) và Telnet (2223); hai nguồn trong lab host-only; tương tác có kiểm soát; log gốc bảo toàn bằng SHA-256. **Ngoài phạm vi:** đưa lên Internet, malware thật, SIEM, cloud trả phí, AI/ML, chế độ proxy tới hệ điều hành thật. Buổi này nhắm: lab cơ bản, ít nhất một lượt thử theo kịch bản có log thật, bảng dữ liệu bước đầu; toàn đề tài nhắm thêm phân loại hành vi, IOC có ngữ cảnh, ATT&CK có căn cứ, security report.

---

## 2. Nhóm đã làm được tới đâu

### 2.1. Bảng tiến độ (B.3)

| Hạng mục | Việc thực tế đã thực hiện | Kết quả/sản phẩm hiện có | Mức độ hoàn thành | Minh chứng | Thành viên | Phần còn thiếu/vướng mắc |
| --- | --- | --- | --- | --- | --- | --- |
| 1. Bài toán/phạm vi | Tổng hợp thông tin môn học và đề tài; soạn Q1–Q3, phạm vi trong/ngoài, tách phạm vi buổi này với toàn đề tài | Bản đề xuất câu hỏi và phạm vi | **Đang làm**: bản đề xuất, chưa được nhóm thống nhất | `docs/THONG_TIN_MON_HOC_NT140.md` (người thực hiện chưa xác nhận); `docs/01_quyet_dinh_pham_vi_cong_cu.md` mục 1 | TV4 (Q1–Q3) | Nhóm thống nhất; TV3 review |
| 2. Nghiên cứu và chọn công cụ | Đọc tài liệu chính thức Cowrie, OpenCanary, Dionaea; chọn Cowrie, dự phòng OpenCanary. TV3 kiểm 12 link nguồn (HTTP 200) và `userdb.example` trong gói 3.1.6 | Bản quyết định công cụ | **Đã hoàn thành** (TV3 review đạt) | `docs/01_quyet_dinh_pham_vi_cong_cu.md` mục 2–6; `review/review_TV1_WP-01_WP-02_WP-03.md` mục 1 | TV1; review TV3 | ISS-04: hai ghi chú "[cần xem trên máy thật]" đã có câu trả lời, chưa sửa |
| 3. Thiết kế lab | Sơ đồ hai VM + máy host trên VMnet1 host-only, bảng kết nối, luật ufw, 6 lớp cách ly | Sơ đồ có IP/cổng thật | **Đã hoàn thành thiết kế**, TV1 đã dựng đúng thiết kế; TV3 review đạt trên tài liệu và log | `docs/02_so_do_lab.md`; `review/review_TV1_WP-01_WP-02_WP-03.md` mục 2 | TV1; review TV3 | "Đã tháo NAT" và "Cowrie không chạy bằng root" mới có căn cứ từ tài liệu của TV1 |
| 4. Cài đặt/cấu hình | Cài Cowrie 3.1.6 bằng pip, user riêng `cowrie`; bật Telnet; `userdb.txt` riêng; tắt `forwarding`; tháo NAT, bật ufw. TV3 (gói pip) và TV4 (mã nguồn tag `v3.1.6` trên GitHub) so độc lập với cấu hình mặc định: chỉ khác dòng 813, 873 | Honeypot nhận SSH :2222 và Telnet :2223 từ cả hai nguồn | **Lab chạy được, TV1 tự kiểm cách ly đạt; kiểm tra độc lập của TV3: dự kiến; TV3 dựng lại theo README: dự kiến** | `Implement/lab/`; `evidence/kiem_tra_cach_ly_TV1.md`; `review/review_TV4_WP-13_deception.md` mục 1 | TV1; review TV3, TV4 | Biên bản cách ly độc lập (`review/kiem_tra_cach_ly.md`) chưa chạy; lab chỉ có trên máy TV1 |
| 5. Tạo tương tác và thu log | Smoke test: hai nguồn × hai dịch vụ, có log gốc + SHA-256. TV4 viết kịch bản KB-01–KB-05, tài khoản giả, quy ước nhật ký, script tự động hóa và script đối chiếu | Log smoke test 58 sự kiện; kịch bản; mẫu nhật ký; script | **Đang làm**: có tương tác kiểm soát truy ngược được sang log gốc (smoke test). **Lượt chạy theo kịch bản (RUN): chưa chạy.** Script chạy vào lab: chưa chạy thử | `evidence/smoke_test/`; `docs/03_kich_ban_thu_nghiem.md`; `experiments/` | TV1 (smoke); TV4 (kịch bản, script) | RUN cần lab trên máy TV1 và kiểm cách ly trước lượt; kịch bản chưa được TV3 review, TV1 chưa xác nhận |
| 6. Xử lý/phân tích | Hợp đồng dữ liệu; bộ xử lý một lệnh mỗi lượt (kiểm hash, chuẩn hóa UTC, nhóm phiên, gắn kịch bản, báo cáo chất lượng). TV3 chạy lại trên máy khác và đếm độc lập; TV4 lặp lại phép đối chiếu trên máy thứ ba | `events.csv`, `sessions.csv`, báo cáo chất lượng sinh từ log smoke test | **Đã có bảng chuẩn hóa sinh từ log thật (smoke test), chạy lại được, khớp phép đếm độc lập. Trên log RUN theo kịch bản: dự kiến** | `docs/04_hop_dong_du_lieu.md`; `analysis/`; `review/review_TV2_WP-05_WP-07.md`; `review/review_TV4_doi_chieu_smoke.md` | TV2 (theo mã và báo cáo công việc trong repo); review TV3; TV4 lặp lại | ISS-01, ISS-02, ISS-03 còn mở |
| 7. Thống kê/báo cáo | TV4 lập khung nhận xét và ghép báo cáo này | Khung nhận xét (dự kiến); báo cáo ghép | **Đang làm – chưa đạt**: chưa có bảng O1, O4, O6 từ RUN | `results/khung_nhan_xet_du_kien.md`; file này | TV4 | Cần RUN và bảng của TV2 (BG-09) |
| 8. Phối hợp nhóm | Chốt vai TV1–TV4; quy trình bàn giao có nhật ký; báo cáo công việc sau mỗi việc; review chéo | Bảng bàn giao 13 điểm, nhật ký bàn giao, 2 bản review của TV3, 2 bản review của TV4 | **Đang làm** | `BAN_GIAO.md`; `docs/bao_cao_cong_viec/`; `review/` | Cả nhóm | TV2 chưa có phần viết cho báo cáo; nhiều trạng thái trong tài liệu chưa cập nhật (mục 6) |
| Bổ sung: Deception (WP-13) | Ghi chú nguyên lý; kiểm yếu tố mồi bằng cấu hình và TTY; bảng điểm lộ ban đầu. TV4 review: kiểm mọi trích dẫn log và cấu hình | Ghi chú; 11 yếu tố mồi; 8 điểm lộ (L1–L8) | Ghi chú: **TV4 review đạt có lưu ý** (9 điểm nên sửa, không có lỗi mức chặn). Bảng điểm lộ chính thức: dự kiến | `docs/00_nguyen_ly_deception_telemetry.md`; `review/review_TV4_WP-13_deception.md` | TV3; review TV4 | Bảng điểm lộ từ RUN chờ transcript KB-03 (BG-07) |

### 2.2. Ba mức theo dàn ý I.1

**Đã đạt mức cơ bản** (kèm cách kiểm):

- Chọn công cụ có lý do và nguồn chính thức. Kiểm: TV3 review, 12 link còn truy cập được (`review/review_TV1_WP-01_WP-02_WP-03.md`).
- Có log thật của Cowrie cho **SSH và Telnet, từ hai nguồn**, kèm SHA-256. Kiểm: TV2 tự kiểm khi nhận (`BAN_GIAO.md`, nhật ký 10/11 15:32); TV3 và TV4 đếm lại khớp (`review/review_TV4_doi_chieu_smoke.md`).
- Bộ xử lý chạy lại được từ log gốc tới `events.csv`, `sessions.csv`, có kiểm hash và không ghi vào log gốc. Kiểm: TV3 chạy trên máy khác, hai lần giống nhau từng byte; TV4 chạy trên máy thứ ba với pandas 3.1.1, khớp.
- Ghi chú deception có trích dẫn log thật. Kiểm: TV4 mở từng dòng được trích (`review/review_TV4_WP-13_deception.md` mục 2).

**Đã làm sâu hơn:**

- So cấu hình đang dùng với bản mặc định chính thức của Cowrie 3.1.6, bằng hai cách độc lập (TV3: gói pip; TV4: tag `v3.1.6` trên GitHub, commit `ea9513e`).
- Phép đếm độc lập không dùng mã của TV2 (TV3 viết, TV4 chạy lại); giải mã file TTY để kiểm mồi.
- Tắt chuyển tiếp cổng SSH của Cowrie (mặc định đang bật).
- Tái hiện được lỗi gắn kịch bản ISS-01 bằng nhật ký dựng từ giờ thật của smoke test; TV4 đề xuất cách ghi nhật ký có dòng bắt đầu/kết thúc để tránh lỗi này.

**Đang làm – chưa đạt:**

- **Lab "cơ bản" chưa đủ tiêu chí I.1:** chưa có kiểm tra cách ly độc lập của TV3 và chưa ai dựng lại lab theo README. Hiện chỉ ghi được: "lab chạy được, TV1 tự kiểm cách ly đạt; kiểm tra độc lập: dự kiến".
- **Chưa chạy lượt thử theo kịch bản (RUN).** Kịch bản, nhật ký mẫu và script đã sẵn nhưng chưa chạy vào lab.
- Chưa có bảng O1, O4, O6 và nhận xét từ RUN.
- Q1–Q3 và phạm vi chưa được nhóm thống nhất.

### 2.3. Đóng góp đã thực hiện (B.5)

| Thành viên | Việc đã làm | Sản phẩm/minh chứng |
| --- | --- | --- |
| TV1 | Chọn công cụ; thiết kế lab; dựng hai VM và Cowrie; smoke test hai nguồn × hai dịch vụ; tự kiểm cách ly; liệt kê yếu tố mồi và điểm lộ ban đầu; trả lời câu hỏi xác minh schema; viết phần báo cáo tiến độ | `docs/01_quyet_dinh_pham_vi_cong_cu.md` mục 2–6, `docs/02_so_do_lab.md`, `Implement/lab/`, `evidence/smoke_test/`, `evidence/kiem_tra_cach_ly_TV1.md`, `evidence/xac_minh_hop_dong_du_lieu.md`, `report/TV1_lab.md` |
| TV2 | Hợp đồng dữ liệu A→B; bộ xử lý log Cowrie và bộ test; fixture minh họa (ghi rõ không dùng trong kết quả) | `docs/04_hop_dong_du_lieu.md`, `analysis/`, báo cáo công việc ngày 10/11 của TV2. *TV2 chưa gửi phần tự viết cho báo cáo này* |
| TV3 | Review TV1, TV2; chạy lại bộ xử lý và đếm độc lập; danh sách lỗi; soạn biên bản cách ly (chưa chạy); ghi chú deception, kiểm yếu tố mồi, bảng điểm lộ ban đầu; viết phần báo cáo tiến độ | `review/` (2 bản review, `issues.md`, `kiem_tra_cach_ly.md`, `tai_hien/`), `docs/00_nguyen_ly_deception_telemetry.md`, `report/TV3_review_deception.md` |
| TV4 | Đọc hiểu repo, gộp nhánh; Q1–Q3 và phạm vi (đề xuất); kịch bản KB-01–KB-05, tài khoản giả, mẫu và quy ước nhật ký; script tự động hóa và đối chiếu (chưa chạy vào lab); review ghi chú deception; lặp phép đối chiếu smoke test; khung nhận xét; ghép báo cáo này. Phần làm ngày 11/11 do TV4 thực hiện, có AI hỗ trợ | `docs/01_quyet_dinh_pham_vi_cong_cu.md` mục 1, `docs/03_kich_ban_thu_nghiem.md`, `experiments/`, `review/review_TV4_*.md`, `evidence/doi_chieu_smoke_TV4/`, `evidence/van_hanh_TV4/`, `results/khung_nhan_xet_du_kien.md`, các báo cáo TV4 trong `docs/bao_cao_cong_viec/` |
| Chưa rõ người thực hiện | Tổng hợp thông tin môn học và đề tài | `docs/THONG_TIN_MON_HOC_NT140.md` |

---

## 3. Thiết kế, công cụ, cách ly và tái lập

**Công cụ** (`docs/01_quyet_dinh_pham_vi_cong_cu.md` mục 2): **Cowrie** (chính) giả lập SSH và Telnet, có shell giả để quan sát lệnh, log JSON mỗi dòng một sự kiện có mã phiên. **OpenCanary** (dự phòng) chỉ ghi được lần thử mật khẩu, không có shell. **Dionaea** không chọn: nhắm thu mẫu malware, bản phát hành cuối 11/2020.

**Lab đã dựng** (TV1, `docs/02_so_do_lab.md` mục 8; VMware Workstation 25H2 trên máy TV1):

| Máy | Vai trò | IP |
| --- | --- | --- |
| Máy host Windows của TV1 | Nguồn 2 + quản trị | `192.168.239.1` |
| VM-A, Ubuntu Server 24.04.5 | Nguồn 1 | `192.168.239.10` |
| VM-H, Ubuntu Server 24.04.5 | Cowrie 3.1.6: SSH :2222, Telnet :2223 | `192.168.239.20` |

**Cách ly và mức căn cứ:**

| Lớp | Căn cứ hiện có | Ai kiểm |
| --- | --- | --- |
| Mạng host-only, không có card NAT, không có default route | `evidence/kiem_tra_cach_ly_TV1.md` | TV1 tự kiểm |
| ufw chặn mặc định cả hai chiều; cổng 22 chỉ từ `.1` | Như trên | TV1 tự kiểm |
| Mọi thử kết nối ra ngoài từ VM-H và từ shell giả đều thất bại | Như trên (5 lệnh trên VM-H, 3 lệnh trong shell giả) | TV1 tự kiểm |
| Tắt Shared Folders, kéo-thả, copy-paste | Như trên | TV1 tự kiểm |
| Cowrie chạy bằng user riêng, `forwarding = false` | `Implement/lab/cowrie/cowrie.cfg:813`; README lab Bước 6 | TV1; TV3, TV4 kiểm file cấu hình trong repo |
| **Kiểm tra độc lập** | `review/kiem_tra_cach_ly.md`: "CHƯA THỰC HIỆN" | **Dự kiến** (TV3) |

**Tái lập:** README 16 bước (`Implement/lab/README_chay_lab.md`). Chưa thành viên nào khác dựng lại. Máy của TV4 không có lab (kiểm ngày 11/11: không có VM-H, VM-A, không có card VMnet1; `evidence/van_hanh_TV4/2026-11-11.md`), nên TV4 cũng chưa kiểm được lab.

---

## 4. Thu thập và xử lý

**Luồng dữ liệu:**

```text
kịch bản (docs/03) → nhật ký H.2 (experiments/nhat_ky_thu_nghiem.csv) + transcript
      → Cowrie ghi cowrie.json, TTY trên VM-H → scp về data/raw/RUN-xx/ + SHA256SUMS + run_note.txt
      → analysis.process_run → data/processed/RUN-xx/{events.csv, sessions.csv, bao_cao_chat_luong.txt}
      → kiểm chứng: dem_doc_lap.py (đếm độc lập) + doi_chieu.py (bước nhật ký ↔ sự kiện)
```

**Một phiên trong log thật** (smoke test, phiên Telnet từ nguồn 1, `evidence/smoke_test/cowrie.json` dòng 22–32, trích gọn, bỏ sự kiện phụ; TV3 đã đối chiếu; mật khẩu là mật khẩu giả của lab):

```text
14:47:49.818  cowrie.session.connect   192.168.239.10  telnet
14:47:49.862  cowrie.login.failed      labuser / sai-mat-khau
14:47:49.906  cowrie.login.success     labuser / LabOnly-2026
14:47:51.933  cowrie.command.input     whoami
14:47:53.009  cowrie.command.input     exit
14:47:53.012  cowrie.session.closed    duration_ms = 3194
```

**Đơn vị đếm:** sự kiện = một dòng log; lần đăng nhập = một sự kiện `login.failed`/`login.success`; phiên = một mã `session`. Không cộng các đơn vị với nhau.

**Gắn kịch bản:** bộ xử lý ghép phiên với nhật ký theo IP nguồn, cổng và khoảng thời gian nới `|δ|`. Với nhật ký mỗi kịch bản chỉ một dòng, phiên Telnet bị trượt khi δ nhỏ (ISS-01). TV4 đề xuất mỗi kịch bản có dòng bắt đầu và kết thúc, nghỉ giữa hai kịch bản cùng nguồn, cùng cổng ≥ `max(10 s, 2×|δ| + 2 s)` (`experiments/quy_uoc_nhat_ky.md`). Đây là quy ước phía nhật ký; TV2 chưa xem, ISS-01 chưa đóng.

**Kiểm chứng trên log smoke test:**

| Phép kiểm | TV3 (máy TV3) | TV4 (máy TV4) |
| --- | --- | --- |
| `pytest analysis/tests` | 15 passed | 13 passed, 2 failed vì `SHA256SUMS` của fixture minh họa tính trên bản CRLF; trên bản xuất CRLF: 15 passed |
| Bộ xử lý trên bản sao smoke test | Mã 0; chạy 2 lần giống nhau từng byte | Mã 0 (pandas 3.1.1) |
| Đếm độc lập `dem_doc_lap.py` | KHỚP | KHỚP |
| Hash log gốc sau khi chạy | Không đổi | Không đổi (3/3 OK) |

---

## 5. Kết quả sơ bộ và giới hạn

### 5.1. Log smoke test (không phải lượt chạy theo kịch bản)

Smoke test do TV1 chạy bằng script ngày 10/11, mục đích kiểm lab và schema, **không** theo kịch bản KB. Số liệu (TV1 báo cáo; TV3, TV4 đếm lại khớp):

- **58 sự kiện; 8 phiên** (6 phiên có đăng nhập, 2 phiên chỉ dò cổng); **4 lần đăng nhập thất bại, 4 lần thành công; 8 lệnh** (`whoami`, `exit` ở 4 phiên).

Ma trận nguồn × dịch vụ (tính từ `evidence/doi_chieu_smoke_TV4/sessions.csv`; **phiên** và **lần đăng nhập** ghi tách riêng):

| Nguồn | SSH :2222 – phiên | SSH – lần đăng nhập (sai/đúng) | Telnet :2223 – phiên | Telnet – lần đăng nhập (sai/đúng) |
| --- | --- | --- | --- | --- |
| VM-A `192.168.239.10` | 3 (1 phiên chỉ dò cổng) | 1 / 1 | 2 (1 phiên chỉ dò cổng) | 1 / 1 |
| Host `192.168.239.1` | 2 | 1 / 1 | 1 | 1 / 1 |

Quan sát ban đầu trên log này: mỗi thao tác trong bảng giờ của TV1 đều có sự kiện cùng mã phiên; phiên Telnet không có `client.version`/`client.kex` mà có `telnet.option`; một phiên chỉ mở cổng 2222 rồi đóng sinh `client.version` rỗng (`json:3`, `cowrie.log` dòng 18).

### 5.2. Yếu tố mồi và điểm lộ ban đầu (O7, quan sát ban đầu)

Cấu hình chỉ khác bản mặc định ở `forwarding` và Telnet, nên mọi mồi là giá trị mặc định công khai: tên máy `svr04`, banner `OpenSSH_9.2p1 Debian`, nhân Debian 6.1, lời chào Debian, hệ thống file giả. Chỉ tài khoản là do nhóm đặt. Bảng dưới theo TV3, mức căn cứ theo review của TV4:

| Điểm lộ | Căn cứ | Mức căn cứ |
| --- | --- | --- |
| Cấu hình trùng bản mặc định công khai: đoán trước được tên máy, banner, nhân | So `cowrie.cfg` với Cowrie 3.1.6 (TV3 và TV4 độc lập) | Đã kiểm trên cấu hình trong repo |
| Tên máy `svr04` là giá trị mặc định | `cowrie.cfg:29`; TTY hiện `labuser@svr04:~$` | Đã kiểm |
| Banner công bố OpenSSH 9.2p1, `ssh -V` trong shell giả trả 7.9p1 | `cowrie.cfg:738`, `cowrie.cfg:617`; TV1 thấy cả hai | Cấu hình + quan sát của TV1. Ghi nhận bằng transcript KB-01 (`ssh -v`) và KB-03: dự kiến |
| `wget` tới URL dạng IP in "connected." rồi treo; `curl -m` không được hỗ trợ | Quan sát của TV1 khi tự kiểm cách ly | Quan sát của người khác, log không có trong repo; tái hiện: dự kiến |
| Phản hồi khác máy thật; lệnh không được hỗ trợ | So transcript KB-03 với VM-A; đếm `command.failed` | Dự kiến (cần RUN) |

Giới hạn: người "tấn công" là thành viên nhóm, nên bảng chỉ cho biết điểm nào **có thể** lộ, không đo được kẻ tấn công thật có nhận ra hay không.

### 5.3. Lượt chạy theo kịch bản

**Chưa có.** Khi chạy, lượt cơ bản dự kiến cho 6 phiên, 7 lần đăng nhập thất bại, 3 lần thành công, 15 lệnh (`docs/03_kich_ban_thu_nghiem.md` mục 0.4); đây là **mong đợi**, không phải kết quả. Đầu ra dự kiến: bảng phiên O1, timeline KB-03 (O4), ma trận nguồn × dịch vụ (O6), bảng đối chiếu, 3–5 nhận xét theo khung `results/khung_nhan_xet_du_kien.md`.

### 5.4. Giới hạn chung

Dữ liệu do nhóm tạo trong lab, cỡ mẫu nhỏ; shell là giả lập; IP trong lab không phải IOC độc hại; không suy rộng ra kẻ tấn công trên Internet; giờ sự kiện theo đồng hồ VM-H, giờ nhật ký theo máy nguồn.

---

## 6. Còn thiếu, lỗi, ảnh hưởng và hướng xử lý

| Vấn đề | Ảnh hưởng | Hướng xử lý | Người |
| --- | --- | --- | --- |
| Chưa có kiểm tra cách ly độc lập (BG-04); chưa ai dựng lại lab | Lab chưa đạt nhãn "cơ bản"; theo kế hoạch chưa được chạy RUN | Kiểm ngay trên máy TV1 (biên bản đã có lệnh); không nối máy khác vào lab | TV3, TV1 |
| Lab chỉ có trên máy TV1; máy TV4 không có lab | TV4 chưa chạy được RUN và chưa thử script | Chạy RUN trên máy TV1 theo `experiments/scripts/README.md` mục 2 | TV4 + TV1 |
| ISS-01 (Trung bình): kịch bản một dòng nhật ký không khớp được phiên khi δ nhỏ | Nhiều phiên RUN phải xét tay | Phía nhật ký: dòng bắt đầu/kết thúc (đã có quy ước); phía mã: TV2 quyết định | TV2 (+ TV4) |
| ISS-02, ISS-03 (Thấp) | Báo cáo chất lượng dễ hiểu nhầm; trạng thái BG-05 lỗi thời | `review/issues.md` | TV2 |
| ISS-04 (Thấp) | Tài liệu lab còn chỗ trống | `review/issues.md` | TV1 |
| `pytest` lỗi 2 test trên máy có fixture dạng LF | Người khác clone repo có thể thấy test đỏ dù bộ xử lý đúng | Đề nghị thêm `analysis/tests/fixtures/** -text` vào `.gitattributes` (`review/review_TV4_doi_chieu_smoke.md` mục 2); chưa ghi vào `review/issues.md` | TV2 quyết định |
| Ghi chú deception có 9 điểm nên sửa (4 câu rộng hơn căn cứ) | Dễ bị hỏi "đo bằng gì" | `review/review_TV4_WP-13_deception.md` mục 4 | TV3 |
| Trạng thái trong một số tài liệu lỗi thời (ví dụ `docs/01_quyet_dinh_pham_vi_cong_cu.md`, `docs/02_so_do_lab.md` còn "chờ TV3 review" dù đã review) | Người đọc hiểu sai tiến độ | Danh sách M1–M10 ở `evidence/van_hanh_TV4/hien_trang_GD0.md` mục 2; mỗi người sửa phần mình | TV1, TV2 |
| TV2 chưa có phần viết cho báo cáo; chưa có bảng O1/O4/O6 | Phần xử lý trong báo cáo này do TV4 ghép từ minh chứng | TV2 viết phần mình | TV2 |
| Kịch bản, quy ước nhật ký, script chưa được review; TV2 chưa xem quy ước nhật ký | Có thể phải sửa trước RUN | TV3 review; TV1 xác nhận khả thi; TV2 xem quy ước | TV3, TV1, TV2 |

---

## 7. Dự định tiếp theo và phân công

Không đặt lịch ngày ở đây; thứ tự theo phụ thuộc.

| Thành viên | Việc tiếp theo | Nguồn |
| --- | --- | --- |
| TV1 | Kiểm tra lại biên bản cách ly của TV3; cùng TV4 chạy RUN-01 trên máy TV1, xuất log gốc + SHA-256 + `run_note.txt`; xác nhận kịch bản khả thi với cấu hình; sửa ISS-04 | `report/TV1_lab.md` phần 7 |
| TV2 | Xem quy ước nhật ký và quyết định cách xử lý ISS-01, ISS-02, ISS-03; chạy bộ xử lý trên RUN-01; tạo bảng O1, O4, O6 | Phân công kế hoạch F.4 (TV2 chưa gửi phần tự viết) |
| TV3 | Kiểm tra cách ly độc lập trên lab của TV1; review kịch bản; kiểm lại ISS-01–ISS-04; sau RUN-01: kiểm ngẫu nhiên bảng đối chiếu, lập bảng điểm lộ chính thức; dựng lại lab, chạy RUN-TEST (WP-09); rà soát báo cáo ghép | `report/TV3_review_deception.md` phần 7 |
| TV4 | Chạy phiên chuẩn bị rồi RUN-01 trên máy TV1; lập bảng đối chiếu; viết nhận xét từ RUN; sau đó phân loại hành vi, observable và mapping ATT&CK có `raw_ref` (WP-11); cập nhật báo cáo này | `docs/03_kich_ban_thu_nghiem.md`, `experiments/scripts/README.md`, `results/khung_nhan_xet_du_kien.md` |

**Điểm xin giảng viên góp ý** (kế hoạch I.4): một Cowrie (SSH + Telnet, hai nguồn) trong lab cô lập đã đủ chưa, hay cần honeypot thứ hai; có được dùng dataset honeypot công khai làm dữ liệu tham khảo không; đầu ra cuối là security report hay dashboard, mức kỳ vọng với IOC và ATT&CK.
