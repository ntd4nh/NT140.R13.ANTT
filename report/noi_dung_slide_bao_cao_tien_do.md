# Nội dung slide – Báo cáo tiến độ đồ án NT140, đề tài 13

**Bản nháp do TV1 soạn ngày 2026-11-11, để TV4 ghép và chỉnh (WP-10).** Số liệu lấy từ repo tại commit `1d115d3`; mọi khẳng định "đã làm" có minh chứng ghi ở cuối mỗi slide. Việc chưa làm ghi "dự kiến".

**Cách dùng file:** mỗi slide có ba phần:
- **Trên slide:** chữ đặt lên slide, giữ ngắn.
- **Hình/bảng:** thứ nên đặt lên slide.
- **Nói:** ý người trình bày nói thêm, không đưa lên slide.

Dòng "Minh chứng" để nhóm tra khi bị hỏi, không cần đưa lên slide.

**Trước khi trình bày, cần cập nhật:**
- Tên thành viên.
- Slide 4: câu hỏi nghiên cứu, khi TV4 chốt.
- Slide 9, 10: nếu đã chạy RUN-01 hoặc có biên bản cách ly của TV3.

**Phân vai trình bày (theo kế hoạch F.4):**

| Người | Slide |
| --- | --- |
| TV4 | 1–4, 9, 13–14 |
| TV3 | 5, 11, 12 |
| TV1 | 6–8 |
| TV2 | 10 |

---

## Slide 1 – Tiêu đề

**Trên slide:**
- NT140 – An toàn mạng · Đề tài 13
- **Nghiên cứu và xây dựng Honeypot phục vụ thu thập và phân tích hành vi tấn công**
- Báo cáo tiến độ
- Nhóm: TV1 [tên] · TV2 [tên] · TV3 [tên] · TV4 [tên]

---

## Slide 2 – Đề tài yêu cầu gì

**Trên slide:**
- **Mục tiêu:** hiểu nguyên lý *deception* và cách honeypot tạo *security telemetry* để nghiên cứu hành vi kẻ tấn công.
- **Gợi ý của đề tài:**
  - Thiết kế, triển khai honeypot.
  - Tạo tương tác trong môi trường kiểm soát.
  - Phân tích nguồn, dịch vụ bị nhắm, lệnh, timeline.
  - Trích xuất IOC; phân loại hành vi; ánh xạ MITRE ATT&CK.
  - Thống kê / security report.

**Nói:**
- Honeypot là hệ thống mồi, người dùng hợp lệ không có lý do chạm vào. Vì vậy **mọi tương tác với nó đều đáng quan sát**.
- Đề tài thuộc nhánh phòng vệ của môn (Lecture 11: Firewalls, IDPS, Honeypot). Trong chuỗi Prevent → Detect → Recover, honeypot đóng góp ở khâu Detect.

**Minh chứng:** `Project.md`; `docs/THONG_TIN_MON_HOC_NT140.md`

---

## Slide 3 – Nguyên lý deception và telemetry

**Trên slide:**
- **Mồi:** làm kẻ tấn công tin đây là máy thật: tên máy, banner SSH, shell, file hệ thống giả.
- **Telemetry:** mỗi hành động của kẻ tấn công sinh ra một sự kiện có mã phiên và giờ UTC.
- **Mức tương tác:**
  - Thấp: chỉ thấy banner.
  - **Trung bình: vào được shell giả lập ← nhóm chọn.**
  - Cao: hệ điều hành thật, rủi ro lớn.

**Hình/bảng:**

| Kẻ tấn công làm gì | Sự kiện Cowrie ghi |
| --- | --- |
| Mở kết nối | `session.connect` |
| Client SSH tự giới thiệu | `client.version`, `client.kex` (vân tay HASSH) |
| Thử mật khẩu | `login.failed` / `login.success` |
| Gõ lệnh | `command.input` (lệnh lạ: thêm `command.failed`) |
| Tải file | `session.file_download` |
| Màn hình phiên | file TTY, phát lại được |
| Ngắt kết nối | `session.closed` (`duration_ms`) |

**Nói:** mức trung bình cho quan sát được lệnh kẻ tấn công gõ. Rủi ro còn lại được kiểm soát bằng cách ly ở mức máy ảo (slide 7).

**Minh chứng:** `docs/00_nguyen_ly_deception_telemetry.md` (TV3); ví dụ từng loại sự kiện trỏ tới dòng trong `evidence/smoke_test/cowrie.json`

---

## Slide 4 – Hướng đi: câu hỏi nghiên cứu và phạm vi

**Trên slide** (bản nháp từ kế hoạch; **TV4 chốt**, sửa slide này nếu khác):
- **Q1.** Honeypot ghi được gì với từng loại tương tác? Phản hồi nào làm lộ đây là hệ thống giả?
- **Q2.** Từ log có dựng lại được diễn biến một phiên và đối chiếu khớp với kịch bản thực tế không?
- **Q3.** Trích được chỉ dấu nào (credential, lệnh, URL, hash)? Phân loại thành nhóm hành vi nào? Đủ căn cứ ánh xạ ATT&CK tới đâu?

| Trong phạm vi | Ngoài phạm vi |
| --- | --- |
| 1 honeypot, 2 dịch vụ (SSH, Telnet), 2 nguồn tương tác | Đưa honeypot ra Internet |
| Lab cô lập, tương tác theo kịch bản do nhóm thực hiện | Dùng công cụ hay mã độc tấn công thật |
| Thu log → chuẩn hóa → thống kê → phân tích | Quy kết danh tính kẻ tấn công từ IP |

**Nói:** nhóm **không** đưa honeypot ra Internet, vì không kiểm soát được rủi ro. Dữ liệu do nhóm tự tạo theo kịch bản, nên kết luận dừng ở mức "honeypot thu được gì và phân tích được tới đâu", không suy rộng ra hành vi kẻ tấn công ngoài thực tế.

**Minh chứng:** `Plan/KE_HOACH_BAO_CAO_TIEN_DO_HONEYPOT.md` mục A; mục 1 của `docs/01_quyet_dinh_pham_vi_cong_cu.md` (TV4, đang trống)

---

## Slide 5 – Giải pháp (1): chọn công cụ

**Trên slide:**

| Công cụ | Quyết định | Lý do |
| --- | --- | --- |
| **Cowrie 3.1.6** | **Chính** | Giả lập cả SSH và Telnet, có shell giả để quan sát lệnh; log JSON mỗi dòng một sự kiện, có mã phiên; đang được phát triển |
| OpenCanary | Dự phòng | Nhiều dịch vụ, nhưng SSH không cho đăng nhập, không có shell, nên chỉ thấy lần thử mật khẩu |
| Dionaea | Loại | Ngừng phát triển: bản cuối 11/2020, commit cuối 02/2021 |

- Xử lý dữ liệu: **Python / Pandas**.

**Nói:** mỗi nhận định về công cụ đều đối chiếu với tài liệu chính thức; TV3 đã kiểm lại 12 link nguồn.

**Minh chứng:** `docs/01_quyet_dinh_pham_vi_cong_cu.md`; `review/review_TV1_WP-01_WP-02_WP-03.md`

---

## Slide 6 – Giải pháp (2): kiến trúc lab đã dựng

**Hình:** sơ đồ trong `docs/02_so_do_lab.md` (Mermaid), ghi rõ **"đã dựng"**. Hoặc vẽ lại đơn giản:

```
 Máy host Windows 11 – VMware Workstation 25H2 – 16 GB RAM
 ┌──────────────────── VMnet1 host-only 192.168.239.0/24 (không có Internet) ───────────────┐
 │  Nguồn 2: Windows host (.1)        Nguồn 1: VM-A (.10)        VM-H honeypot (.20)          │
 │  SSH + Telnet client               Ubuntu 24.04.5              Ubuntu 24.04.5               │
 │        │                                 │                     Cowrie: SSH :2222            │
 │        └──────────── SSH / Telnet ───────┴───────────────────►        Telnet :2223          │
 │                                                                ufw chặn mọi chiều ra        │
 └───────────────────────────────────────────────────────────────────────────────────────────┘
```

**Trên slide:**
- 2 máy ảo + máy host = **2 nguồn tấn công × 2 dịch vụ**.
- Cowrie chạy bằng user riêng không có quyền quản trị; cấu hình chỉ khác bản mặc định 2 dòng: **bật Telnet**, **tắt chuyển tiếp cổng SSH**.
- Tài khoản giả riêng (`userdb.txt`): sai mật khẩu bị từ chối, đúng thì vào shell giả.

**Nói:**
- Mặc định Cowrie chấp nhận gần như mọi mật khẩu, nên nhóm tạo danh sách tài khoản riêng để kịch bản "gõ sai rồi gõ đúng" có ý nghĩa.
- Mặc định Cowrie cũng cho phép chuyển tiếp cổng SSH, tức là cho mượn honeypot làm trạm trung chuyển. Nhóm đã tắt; khi thử lại, Cowrie từ chối.

**Minh chứng:** `docs/02_so_do_lab.md`; `Implement/lab/README_chay_lab.md`; `Implement/lab/cowrie/cowrie.cfg` và `README.md`

---

## Slide 7 – Giải pháp (3): cách ly an toàn

**Trên slide – 6 lớp cách ly (defense in depth):**
1. **Mạng:** honeypot chỉ có card host-only, không có đường ra Internet.
2. **Tường lửa ufw:** chặn mọi chiều ra; chỉ máy host vào được cổng quản trị 22.
3. **VMware:** tắt thư mục chung, kéo-thả, copy-paste; gỡ USB và âm thanh.
4. **Quyền:** Cowrie chạy bằng user không có quyền quản trị.
5. **Khôi phục:** snapshot từng mốc.
6. **Thói quen:** tắt honeypot khi không dùng; không dùng mật khẩu thật.

**Hình/bảng – kết quả tự kiểm của TV1:**

| Phép thử từ honeypot | Kết quả |
| --- | --- |
| `ping 8.8.8.8` | Network is unreachable |
| `curl https://example.com` | Không phân giải được tên |
| Shell giả: `wget`, `curl` tải file | Thất bại, thư mục tải về trống |
| VM-A vào cổng quản trị 22 | Connection timed out |

**Nói:** đây là bản tự kiểm của người dựng lab. Biên bản kiểm tra độc lập do TV3 soạn lệnh, **dự kiến** chạy trước lượt thử nghiệm đầu tiên. Nhóm quy định chỉ chạy thử nghiệm sau khi biên bản này đạt.

**Minh chứng:** `evidence/kiem_tra_cach_ly_TV1.md`; `review/kiem_tra_cach_ly.md` (chưa có kết quả)

---

## Slide 8 – Làm được đến đâu (1): honeypot chạy và thu log thật

**Trên slide:**
- Smoke test: mỗi nguồn vào cả SSH và Telnet; mỗi lần gõ sai mật khẩu, gõ đúng, `whoami`, `exit`.
- **Thao tác nào cũng có sự kiện tương ứng trong log**, cùng mã phiên, giờ UTC tới micro giây.
- Log gốc niêm phong bằng **SHA-256**.

**Hình/bảng – trích log thật (một phiên Telnet từ VM-A):**

```text
14:47:49.818  cowrie.session.connect   192.168.239.10  telnet
14:47:49.862  cowrie.login.failed      labuser / sai-mat-khau
14:47:49.906  cowrie.login.success     labuser / LabOnly-2026
14:47:51.933  cowrie.command.input     whoami
14:47:53.009  cowrie.command.input     exit
              cowrie.session.closed    duration_ms = 3194
```

| Ma trận nguồn × dịch vụ (phiên có đăng nhập) | SSH :2222 | Telnet :2223 |
| --- | --- | --- |
| Nguồn 1 – VM-A (.10) | 2 | 1 |
| Nguồn 2 – Windows (.1) | 2 | 1 |

- **Tổng:** 58 sự kiện · 8 phiên (6 có đăng nhập, 2 chỉ dò cổng) · 4 lần đăng nhập sai, 4 lần đúng · 8 lệnh.

**Nói:**
- Mật khẩu trong log là mật khẩu giả của lab.
- Smoke test là bước kiểm tra hệ thống, **chưa phải** lượt thử nghiệm theo kịch bản. Lượt đó là RUN-01, dự kiến.

**Minh chứng:** `evidence/smoke_test/` (`cowrie.json`, `SHA256SUMS`, `README.md`)

---

## Slide 9 – Làm được đến đâu (2): bảng tiến độ

**Trên slide:**

| Hạng mục | Trạng thái | Minh chứng |
| --- | --- | --- |
| Chọn công cụ | ✅ Xong, TV3 review đạt | `docs/01` |
| Thiết kế lab | ✅ Xong, đã dựng đúng thiết kế, TV3 review đạt | `docs/02` |
| Cài đặt, cấu hình | ✅ Honeypot chạy SSH + Telnet, 2 nguồn kết nối được | `Implement/lab/` |
| Cách ly | 🟡 TV1 tự kiểm đạt; kiểm độc lập của TV3: dự kiến | `evidence/kiem_tra_cach_ly_TV1.md` |
| Thu log | 🟡 Có log thật từ smoke test; RUN-01 theo kịch bản: dự kiến | `evidence/smoke_test/` |
| Hợp đồng dữ liệu | ✅ Đã đối chiếu log thật; chờ TV3 review | `docs/04` |
| Bộ xử lý log | ✅ Chạy một lệnh mỗi lượt; đã chạy trên log smoke test | `analysis/` |
| Kiểm chứng số liệu | ✅ Đếm độc lập khớp 100% trên smoke test | `review/` |
| Deception | ✅ Ghi chú xong; 🟡 bảng điểm lộ bản đầu | `docs/00` |
| Kịch bản thử nghiệm | 🔴 Chưa có | – |
| Bảng, biểu đồ, nhận xét | 🔴 Chờ RUN-01 | – |

**Nói:** nhãn "xong" chỉ dùng khi có sản phẩm và đã được người thứ hai kiểm. Đây là quy ước của nhóm.

**Minh chứng:** `report/TV1_lab.md`, `report/TV3_review_deception.md`, `BAN_GIAO.md`

---

## Slide 10 – Làm được đến đâu (3): xử lý dữ liệu và kiểm chứng

**Trên slide:**
- **Hợp đồng dữ liệu:** quy định tên trường, nơi chuyển log, giữ log gốc, múi giờ UTC, xử lý trường thiếu; đã đối chiếu từng trường với log thật.
- **Bộ xử lý** `analysis/process_run.py`: kiểm hash → đọc JSON → khử trùng → chuẩn hóa → nhóm phiên → `events.csv`, `sessions.csv`, báo cáo chất lượng.
  - Một lệnh mỗi lượt; chạy hai lần cho kết quả **giống hệt từng byte**.
  - Không bao giờ ghi vào thư mục log gốc.
  - 15 bài test đạt.
- **Kiểm chứng độc lập (TV3):** đếm bằng mã riêng, không dùng mã của TV2.

**Hình/bảng:**

| Chỉ số (log smoke test) | Đếm độc lập | Bộ xử lý | Khớp |
| --- | --- | --- | --- |
| Sự kiện | 58 | 58 | ✅ |
| Phiên | 8 | 8 | ✅ |
| Đăng nhập sai / đúng | 4 / 4 | 4 / 4 | ✅ |
| Lệnh | 8 | 8 | ✅ |

**Nói:** TV3 thử thêm 7 ca biên (hash sai, JSON hỏng, dòng trùng, sự kiện lạ, log xoay vòng…); bộ xử lý xử lý đúng cả 7. Phát hiện 4 lỗi, không lỗi nào mức chặn.

**Minh chứng:** `docs/04_hop_dong_du_lieu.md`; `analysis/README.md`; `review/review_TV2_WP-05_WP-07.md`; `review/tai_hien/`

---

## Slide 11 – Kết quả ban đầu: điểm lộ của honeypot

**Trên slide – kẻ tấn công có thể nhận ra bẫy qua:**

| Điểm lộ | Mức căn cứ |
| --- | --- |
| Cấu hình trùng bản mặc định công khai: ai cũng đoán trước được tên máy, banner, nhân | Đã kiểm |
| Tên máy `svr04`, giá trị mặc định nổi tiếng của Cowrie | Đã kiểm |
| Banner OpenSSH 9.2p1 nhưng `ssh -V` trong shell giả trả 7.9p1 (bản 2018) | Đã kiểm trên cấu hình |
| `wget` in "connected." rồi treo; `curl -m` không được hỗ trợ | Đã quan sát; ghi log: dự kiến |
| Phản hồi khác máy thật với cùng chuỗi lệnh | Dự kiến (RUN-01) |

**Nói:**
- Mọi yếu tố mồi của nhóm đều là giá trị mặc định công khai, trừ danh sách tài khoản.
- **Giới hạn:** "kẻ tấn công" là thành viên nhóm, nên bảng chỉ cho biết điểm nào **có thể** làm lộ, không đo được kẻ tấn công thật có nhận ra hay không.

**Minh chứng:** `docs/00_nguyen_ly_deception_telemetry.md` mục 4–5; `Implement/lab/cowrie/README.md`

---

## Slide 12 – Còn thiếu và vướng mắc

**Trên slide:**

| Còn thiếu | Lý do | Xử lý |
| --- | --- | --- |
| Lượt thử nghiệm theo kịch bản (RUN-01) | Chưa có kịch bản, danh sách tài khoản; chưa có biên bản cách ly độc lập | TV4 hoàn thành kịch bản; TV3 kiểm cách ly trên máy TV1 |
| Bảng, biểu đồ, nhận xét | Phụ thuộc RUN-01 | Bộ xử lý đã sẵn, chạy ngay khi có log |
| Lỗi gắn kịch bản (ISS-01, mức trung bình) | Khi độ lệch giờ nhỏ, một số phiên không khớp nhật ký | TV2 sửa trước RUN-01 |

| Vướng mắc kỹ thuật đã gặp | Cách xử lý |
| --- | --- |
| Lab chỉ có trên một máy, mạng host-only nên người khác không vào được | Kiểm tra trực tiếp trên máy TV1; không nối máy khác vào lab, vì như vậy phá chính lớp cách ly |
| Cowrie mặc định chấp nhận mọi mật khẩu, cho phép chuyển tiếp cổng | Tạo `userdb.txt` riêng; tắt `forwarding` |
| Máy ảo không có Internet nên không tự chỉnh giờ | Đồng bộ giờ với host; ba máy lệch dưới 1 giây |

**Minh chứng:** `review/issues.md`; `report/TV1_lab.md` phần 6

---

## Slide 13 – Định hướng tiếp theo

**Trên slide:**

**Trước khi kết thúc giai đoạn này:**

```
Kịch bản + tài khoản giả (TV4) ─┐
                                ├─► RUN-01 (TV4 + TV1) ─► xử lý (TV2) ─► bảng O1/O4/O6 ─► nhận xét (TV4)
Kiểm tra cách ly độc lập (TV3) ─┘                         └─► đếm độc lập + bảng điểm lộ chính thức (TV3)
```

**Sau buổi báo cáo – phân tích hành vi sâu:**

| Hướng | Phụ trách |
| --- | --- |
| Thêm kịch bản: tải file (KB-04), lượt hỗn hợp, lặp lại để kiểm tra ổn định | TV4, TV1, TV3 |
| Phân loại hành vi theo quy tắc, đánh giá bằng nhãn kịch bản | TV4, TV2 |
| IOC có ngữ cảnh; ánh xạ MITRE ATT&CK có căn cứ | TV4, TV2, TV3 kiểm |
| Sửa điểm lộ (tên máy, phiên bản SSH), so sánh trước và sau | TV1, TV3 |
| Honeypot thứ hai OpenCanary để so sánh telemetry | TV1 |
| Security report tự sinh (có thể kèm dashboard) | TV2 |

**Nói:** khi có RUN-01, bộ xử lý đã sẵn nên ra bảng kết quả gần như ngay. Khâu tốn thời gian là thực nghiệm cẩn thận và đối chiếu.

**Minh chứng:** `Plan/KE_HOACH_BAO_CAO_TIEN_DO_HONEYPOT.md` mục E.2, C7

---

## Slide 14 – Xin góp ý

**Trên slide:**
1. Phạm vi một honeypot Cowrie (SSH + Telnet, hai nguồn) trong lab cô lập có đủ cho đề tài không, hay cần thêm honeypot thứ hai?
2. Nhóm có được dùng dataset honeypot công khai làm dữ liệu tham khảo không? (Nhóm mặc định không đưa honeypot ra Internet.)
3. Đầu ra cuối mong muốn là security report hay dashboard? Mức kỳ vọng với IOC và ATT&CK?
4. Hình thức, thời lượng và mức demo của các buổi báo cáo sau?

**Nói:** câu 1 và 2 ảnh hưởng trực tiếp tới việc dữ liệu có đủ đa dạng để phân loại hành vi hay không.

**Minh chứng:** `Plan/KE_HOACH_BAO_CAO_TIEN_DO_HONEYPOT.md` mục I.4

---

## Phụ lục – Demo (nếu được yêu cầu, khoảng 2 phút)

**Chuẩn bị:**
- Bật VM-H, VM-A; khởi động Cowrie.
- Mở sẵn hai cửa sổ.

**Cửa sổ 1, trên VM-H** (`labadmin`), xem log trực tiếp:

```bash
tail -f /home/cowrie/var/log/cowrie/cowrie.json | jq -r '[.timestamp[11:19], .eventid, .src_ip, (.username // .input // "")] | @tsv'
```

**Cửa sổ 2, trên VM-A:**

```bash
ssh -p 2222 -o PubkeyAuthentication=no labuser@192.168.239.20
```

Gõ sai mật khẩu, gõ đúng, rồi gõ `uname -a`, `ssh -V`, `cat /etc/passwd`: mỗi thao tác hiện một dòng ở cửa sổ 1.

**Dự phòng:** nếu lab lỗi lúc trình bày, dùng slide 8 (log thật) và ảnh chụp màn hình.
