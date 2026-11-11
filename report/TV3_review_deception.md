# Phần báo cáo tiến độ của TV3 – Review, kiểm thử, deception (BG-12)

**Người viết:** TV3 · **Ngày:** 2026-11-11 · **Dùng cho:** TV4 ghép báo cáo (WP-10) theo dàn ý I.1 của kế hoạch

Mọi khẳng định "đã làm" dưới đây có minh chứng trong repo. Việc chưa làm ghi "dự kiến". Mục 4 là các lưu ý của TV3 khi TV4 ghép.

---

## 1. Dòng cho bảng tiến độ B.3

| Hạng mục | Việc thực tế đã thực hiện | Kết quả/sản phẩm hiện có | Mức độ hoàn thành | Minh chứng | Thành viên | Phần còn thiếu/vướng mắc |
| --- | --- | --- | --- | --- | --- | --- |
| 2. Nghiên cứu và chọn công cụ | Kiểm 12 link nguồn của quyết định công cụ; đối chiếu `userdb.example` và các output được bật với gói Cowrie 3.1.6 chính thức | Review đạt, không có lỗi mức chặn | Đã hoàn thành phần review | `review/review_TV1_WP-01_WP-02_WP-03.md`, mục 1 | TV3 | Hai ghi chú "[cần xem trên máy thật]" trong `docs/01` đã có câu trả lời, chờ TV1 sửa (ISS-04) |
| 3. Thiết kế lab | Review sơ đồ theo checklist RV-THIẾT-KẾ; đối chiếu IP và cổng trong sơ đồ với log smoke test | Review đạt | Đã review trên tài liệu và log; **chưa** kiểm trên máy | `review/review_TV1_WP-01_WP-02_WP-03.md`, mục 2 | TV3 | "Đã tháo NAT" và "Cowrie không chạy bằng root" mới có căn cứ từ tài liệu của TV1 |
| 4. Cài đặt/cấu hình | So `cowrie.cfg` với file mặc định trong gói Cowrie 3.1.6: chỉ khác 2 dòng, đúng như TV1 ghi; kiểm cấu hình không chứa bí mật; soạn biên bản kiểm tra cách ly | Review cấu hình đạt; biên bản cách ly có đủ lệnh và kết quả mong đợi | Review cấu hình: đã hoàn thành. **Kiểm tra cách ly độc lập: dự kiến.** Dựng lại lab theo README: dự kiến | `review/review_TV1_WP-01_WP-02_WP-03.md`, mục 3; `review/kiem_tra_cach_ly.md` (chưa có kết quả) | TV3 | Lab chỉ có trên máy TV1 (mạng host-only), phải hẹn TV1. Chưa có biên bản thì chưa gửi được BG-04, nên RUN-01 chưa được chạy |
| 6. Xử lý/phân tích | Chạy lại bộ xử lý của TV2 trên máy khác; viết phép đếm độc lập không dùng mã của TV2; thử 7 ca biên; thử gắn kịch bản bằng nhật ký dựng từ giờ thật của smoke test | 15/15 test qua; 2 lần chạy cho kết quả giống hệt từng byte; đếm độc lập khớp; tìm ra 4 lỗi (1 trung bình, 3 thấp) | Kiểm trên log smoke test: đã hoàn thành. Kiểm thử tích hợp trên lượt chạy thật (WP-09): dự kiến | `review/review_TV2_WP-05_WP-07.md`, `review/tai_hien/`, `review/issues.md` | TV3 | Chưa có log RUN thật; ISS-01 nên sửa trước RUN-01 |
| 8. Phối hợp nhóm | Tự kiểm điều kiện rồi nhận 3 bàn giao (BG-03, BG-08, BG-10); gửi danh sách lỗi (BG-11) | Nhật ký bàn giao ghi căn cứ của từng điều kiện | Đang làm | `BAN_GIAO.md`, nhật ký ngày 11/11 | TV3 | Không |
| Bổ sung: Deception và telemetry (WP-13), dùng cho phần 1 và phần 5 của slide | Viết ghi chú nguyên lý; kiểm lại yếu tố mồi bằng cấu hình và file TTY; lập bảng điểm lộ ban đầu | Ghi chú; bảng 11 yếu tố mồi; bảng 8 điểm lộ (3 điểm có căn cứ đầy đủ) | Ghi chú: đã hoàn thành, chờ TV4 review. Bảng điểm lộ chính thức (`results/RUN-xx/diem_lo.md`): dự kiến | `docs/00_nguyen_ly_deception_telemetry.md` | TV3 | Bảng điểm lộ chính thức chờ RUN-01 và BG-07 |

7 ca biên đã thử: thiếu file trong manifest, hash sai, trỏ đầu ra vào thư mục log gốc, dòng JSON hỏng, dòng trùng, eventid lạ, file log xoay vòng. Cả 7 đều được xử lý đúng hợp đồng dữ liệu.

## 2. Dòng cho bảng đóng góp B.5

| Thành viên | Việc đã làm | Sản phẩm/minh chứng |
| --- | --- | --- |
| TV3 | Review sản phẩm của TV1 (WP-01 phần công cụ, WP-02, cấu hình WP-03) và TV2 (WP-05, WP-07); chạy lại bộ xử lý trên máy khác, đối chiếu bằng phép đếm độc lập; lập danh sách lỗi; soạn biên bản kiểm tra cách ly; viết ghi chú deception, kiểm lại yếu tố mồi, lập bảng điểm lộ ban đầu | `review/` (2 bản review, `issues.md`, `kiem_tra_cach_ly.md`, `tai_hien/`), `docs/00_nguyen_ly_deception_telemetry.md`, các báo cáo TV3 trong `docs/bao_cao_cong_viec/` |

---

## 3. Nội dung cho từng phần slide

### Phần 1 – Nguyên lý deception và telemetry

**Thông điệp:** honeypot là tài nguyên giả. Người dùng hợp lệ không có lý do chạm vào, nên mọi tương tác với nó đều đáng ngờ. Giá trị của honeypot nằm ở **mồi** (làm kẻ tấn công tin là thật) và **telemetry** (dữ liệu ghi được khi họ tương tác).

- **Deception dùng để làm gì:** phát hiện với ít báo động giả, làm chậm kẻ tấn công, nghiên cứu hành vi. Đề tài dùng mục đích thứ ba.
- **Mức tương tác:** thấp (chỉ thấy banner, không vào được), trung bình (vào được shell giả lập), cao (vào hệ điều hành thật). Nhóm chọn **trung bình** (Cowrie `backend = shell`): quan sát được lệnh, còn rủi ro thì kiểm soát bằng cách ly ở mức máy ảo.
- **Telemetry sinh ra từ đâu:** mỗi lớp tương tác tạo một nhóm sự kiện, tất cả cùng mang mã phiên.

| Kẻ tấn công làm gì | Sự kiện Cowrie | Ví dụ trong log thật (`evidence/smoke_test/cowrie.json`) |
| --- | --- | --- |
| Mở kết nối | `session.connect` | dòng 11 |
| Client SSH tự giới thiệu | `client.version`, `client.kex` (vân tay HASSH) | dòng 12, 13 |
| Thử mật khẩu | `login.failed`, `login.success` | dòng 9, 14 |
| Gõ lệnh | `command.input` | dòng 18, 19 |
| Mọi thứ hiện trên màn hình | file TTY (`log.closed`) | dòng 20 |
| Ngắt kết nối | `session.closed` (`duration_ms`) | dòng 21 |

Muốn có đoạn log minh họa thì dùng chung đoạn log phiên Telnet ở phần 4 của TV1 để slide không lặp.

### Phần 2 – Nhóm đã làm được tới đâu (dòng của TV3)

- **Đã đạt mức cơ bản:**
  - Review xong các sản phẩm hiện có của TV1 và TV2, không có lỗi mức chặn. Minh chứng: `review/review_TV1_WP-01_WP-02_WP-03.md`, `review/review_TV2_WP-05_WP-07.md`.
  - Có ghi chú deception và telemetry, mỗi loại telemetry trỏ tới dòng log thật. Minh chứng: `docs/00_nguyen_ly_deception_telemetry.md`.
- **Đã làm sâu hơn:**
  - Phép đếm độc lập không dùng mã của TV2 và khớp toàn bộ (bảng ở phần 4).
  - Không chỉ đọc bảng thay đổi của TV1 mà so thẳng cấu hình với gói Cowrie chính thức, và giải mã file TTY để kiểm mồi.
  - Tái hiện được một lỗi gắn kịch bản (ISS-01) bằng nhật ký dựng từ giờ thật của smoke test.
- **Đang làm – chưa đạt:**
  - Chưa kiểm tra cách ly độc lập (BG-04): biên bản mới có lệnh, chưa có kết quả.
  - Chưa dựng lại lab theo README; chưa chạy lượt RUN-TEST (WP-09).
  - Chưa có bảng điểm lộ chính thức, đang chờ RUN-01.

### Phần 4 – Thu thập và xử lý (phần kiểm chứng của TV3)

**Thông điệp:** trên log smoke test thật, số liệu bộ xử lý của TV2 đưa ra khớp với phép đếm độc lập của TV3.

| Chỉ số (log smoke test, 58 dòng) | Đếm độc lập (TV3) | Bộ xử lý (TV2) | Khớp |
| --- | --- | --- | --- |
| Sự kiện | 58 | 58 dòng `events.csv` | ✅ |
| Phiên | 8 | 8 dòng `sessions.csv` | ✅ |
| Lần đăng nhập thất bại / thành công | 4 / 4 | 4 / 4 | ✅ |
| Lệnh (`command.input`) | 8 | 8 | ✅ |
| So từng phiên: số sự kiện, đăng nhập, danh sách lệnh theo thứ tự, thời lượng | 8 phiên | 8 phiên | ✅ |

Chạy lại: `python -I review/tai_hien/dem_doc_lap.py <thư mục lượt chạy> <thư mục đầu ra của bộ xử lý>` → in `KHỚP`. Giới hạn: mới kiểm trên log smoke test, chưa có lượt chạy theo kịch bản.

### Phần 5 – Kết quả sơ bộ: yếu tố mồi và điểm lộ ban đầu (O7)

**Yếu tố mồi:** TV1 liệt kê, TV3 kiểm lại. Cấu hình chỉ khác bản mặc định ở `forwarding` và Telnet, nên mọi mồi đều là giá trị mặc định công khai: tên máy `svr04`, banner `OpenSSH_9.2p1 Debian`, nhân Debian 6.1, lời chào Debian, hệ thống file giả. Chỉ danh sách tài khoản là do nhóm đặt.

| Điểm lộ | Căn cứ | Mức căn cứ |
| --- | --- | --- |
| Cấu hình trùng bản mặc định công khai: ai cũng đoán trước được tên máy, banner, nhân | So `cowrie.cfg` với gói Cowrie 3.1.6 | Đã kiểm |
| Tên máy `svr04`, giá trị mặc định nổi tiếng của Cowrie | `cowrie.cfg:29`; file TTY hiện `labuser@svr04:~$` | Đã kiểm |
| Banner công bố OpenSSH 9.2p1, nhưng `ssh -V` trong shell giả trả 7.9p1 (bản năm 2018) | `cowrie.cfg:738` và `cowrie.cfg:617` | Đã kiểm trên cấu hình; ghi vào log: dự kiến |
| `wget` in "connected." rồi treo; `curl -m` không được hỗ trợ | Quan sát của TV1 khi tự kiểm cách ly | Dự kiến tái hiện |
| Phản hồi khác máy thật; lệnh không được hỗ trợ | So transcript KB-03 với VM-A; đếm `command.failed` | Dự kiến (RUN-01, BG-07) |

**Giới hạn:** người "tấn công" là thành viên nhóm, nên bảng chỉ cho biết điểm nào **có thể** lộ, không đo được kẻ tấn công thật có nhận ra hay không.
**Đề xuất (dự kiến):** đổi tên máy, cho `ssh -V` khớp với banner. Mỗi lần đổi phải ghi `config_version` mới để không trộn dữ liệu trước và sau.

### Phần 6 – Còn thiếu và vướng mắc (danh sách lỗi của TV3)

| Mã | Mức | Người sửa | Lỗi | Ảnh hưởng |
| --- | --- | --- | --- | --- |
| ISS-01 | Trung bình | TV2 (TV4 phối hợp về nhật ký) | Kịch bản chỉ có một dòng nhật ký không khớp được phiên khi độ lệch giờ nhỏ: thử với δ = 0,5 s thì 2 trong 6 phiên đăng nhập không khớp | Nhiều phiên RUN-01 sẽ phải xét tay; không gán sai kịch bản |
| ISS-02 | Thấp | TV2 | Báo cáo chất lượng tính phiên chỉ dò cổng là "thiếu trường bắt buộc" | Dễ hiểu nhầm là mất dữ liệu |
| ISS-03 | Thấp | TV2 | Trạng thái BG-05 ghi trong hợp đồng dữ liệu đã lỗi thời | Tài liệu |
| ISS-04 | Thấp | TV1 | Tài liệu lab còn chỗ trống dù đã có câu trả lời | Tài liệu |

Không có lỗi mức chặn. Bước tái hiện từng lỗi: `review/issues.md`.

| Vướng mắc của TV3 | Cách xử lý |
| --- | --- |
| Lab chỉ có trên máy TV1 và dùng mạng host-only, máy khác không vào được | Kiểm cách ly ngay trên máy TV1 (ngồi cùng hoặc điều khiển từ xa). Không nối máy khác vào lab, vì như vậy là phá chính lớp cách ly đang kiểm |
| Chưa có lượt chạy thật để kiểm phần gắn kịch bản | Tạm thử bằng nhật ký dựng từ giờ thật của smoke test; nhờ đó tìm ra ISS-01 |

### Phần 7 – Dự định tiếp theo của TV3

1. Kiểm tra cách ly độc lập trên lab của TV1, nhờ TV1 kiểm tra lại biên bản, rồi gửi BG-04 để mở khóa RUN-01 cho TV4.
2. Review kịch bản WP-04 và danh sách tài khoản giả (BG-01) khi TV4 viết xong.
3. Kiểm lại ISS-01 đến ISS-04 sau khi TV1, TV2 sửa.
4. Sau RUN-01: kiểm ngẫu nhiên bảng đối chiếu; lập bảng điểm lộ chính thức từ transcript KB-03 và kết quả trên VM-A (BG-07); đối chiếu số liệu bảng, biểu đồ (WP-08).
5. Dựng lại lab theo README trên máy TV3, tự chạy RUN-TEST và kiểm thử tích hợp (WP-09).
6. Rà soát báo cáo và slide đã ghép (BG-13).
7. Hướng tiếp theo: soạn một lượt chạy hỗn hợp để đánh giá bộ phân loại hành vi; kiểm từng mã ATT&CK trên trang chính thức (WP-11).

---

## 4. Lưu ý cho TV4 khi ghép

1. Cột cuối hai dòng 2 và 3 trong phần B.3 của TV1 còn ghi "Chờ TV3 review". TV3 đã review, kết quả đạt: `review/review_TV1_WP-01_WP-02_WP-03.md`.
2. Nhãn "đã đạt mức cơ bản" cho lab: theo I.1, nhãn này phải kèm "TV3 dựng lại được theo README, kiểm tra cách ly đạt". Hiện mới có bản tự kiểm của TV1, nên tạm ghi "lab chạy được, TV1 tự kiểm cách ly đạt; kiểm tra độc lập của TV3: dự kiến" cho tới khi có BG-04.
3. Phần 5 của slide: dùng bảng điểm lộ ở trên thay cho danh sách trong phần 5 của TV1 để không trùng. Bảng của TV3 đã gồm các điểm TV1 nêu và có thêm mức căn cứ.
4. Đoạn log phiên Telnet trong phần 4 của TV1 khớp với `evidence/smoke_test/cowrie.json` dòng 22–32 (TV3 đã đối chiếu). Mật khẩu trong đoạn log là mật khẩu giả của lab.
5. Dùng thống nhất số liệu smoke test: 58 sự kiện; 8 phiên (6 phiên có đăng nhập, 2 phiên chỉ dò cổng); 4 lần đăng nhập thất bại, 4 lần thành công; 8 lệnh.
