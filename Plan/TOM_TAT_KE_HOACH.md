# Tóm tắt kế hoạch – Đề tài 13: Honeypot

Bản đọc nhanh cho cả nhóm. Chi tiết từng việc xem [kế hoạch đầy đủ](KE_HOACH_BAO_CAO_TIEN_DO_HONEYPOT.md).

## 1. Làm gì

Dựng một honeypot trong lab cô lập, tự tạo tương tác có kiểm soát, thu log và phân tích: **nguồn, dịch vụ bị nhắm, lệnh/thao tác, diễn biến (timeline)**. Kết quả cuối là một security report đơn giản, gồm IOC, phân loại hành vi và mapping MITRE ATT&CK ở mức dữ liệu cho phép.

Mục tiêu đề tài còn yêu cầu **hiểu nguyên lý deception**: honeypot đánh lừa bằng cách nào, telemetry sinh ra từ đâu, và chỗ nào làm lộ đây là hệ thống giả.

## 2. Hướng kỹ thuật đã chốt

- **Công cụ chính:** Cowrie, mở hai dịch vụ SSH (cổng 2222) và Telnet (cổng 2223).
- **Dự phòng:** OpenCanary, dùng nếu Cowrie không chạy được.
- **Lab:**
  - VM-H chạy honeypot.
  - Nguồn 1 là VM-A; nguồn 2 là máy host, nối qua mạng host-only.
  - **Không có đường ra Internet.**
- **Phân tích:** Python/Pandas đọc file `cowrie.json` (mỗi dòng một sự kiện).
- **Không làm:** đưa honeypot ra Internet, SIEM, cloud trả phí, AI/ML.

## 3. Ai làm gì

Vai TV1–TV4 chốt theo kỹ năng của từng người.

| | Việc chính | Phải nộp | Người review |
| --- | --- | --- | --- |
| **TV1 – Dựng lab** | Đọc tài liệu Cowrie, chốt công cụ; vẽ sơ đồ lab; cài Cowrie (SSH + Telnet), tạo `userdb.txt`, tháo NAT, bật firewall; chạy smoke test; xuất log gốc sau mỗi lượt thử | Sơ đồ lab, README cách chạy, cấu hình đã bỏ thông tin nhạy cảm, log smoke test, log gốc + SHA-256 | TV3 |
| **TV2 – Xử lý dữ liệu** | Chốt schema dữ liệu; viết script đọc log → `events.csv`, `sessions.csv`; làm bảng/biểu đồ | Script chạy lại được, file CSV, bảng phiên (O1), timeline một phiên (O4), bảng nguồn × dịch vụ (O6) | TV3 |
| **TV3 – Review, kiểm thử, deception** | Soạn checklist review; kiểm tra cách ly; dựng lại lab theo README; tự chạy một lượt thử và đếm độc lập để đối chiếu số liệu; viết ghi chú deception và bảng điểm lộ | Checklist, danh sách lỗi, biên bản cách ly, báo cáo kiểm thử tích hợp, ghi chú deception, bảng điểm lộ | TV1 (cách ly), TV4 (deception, tích hợp) |
| **TV4 – Thực nghiệm, tổng hợp** | Chốt câu hỏi và phạm vi; viết kịch bản; chạy thử nghiệm, ghi nhật ký; đối chiếu thao tác với log; viết nhận xét; ghép báo cáo và slide | Kịch bản, nhật ký + transcript, bảng đối chiếu, nhận xét có căn cứ, slide | TV3, TV2 (dùng số liệu đúng) |

Sau buổi báo cáo: TV4 phụ trách phân loại hành vi, IOC và ATT&CK; TV2 phụ trách security report; TV1 mở rộng thêm kịch bản hoặc honeypot thứ hai nếu cần.

## 4. Thứ tự làm

1. **Khởi động:** cả nhóm điền tiến độ thật, chốt vai, mỗi gói việc tạo một Issue trên GitHub.
2. **Chốt hướng** (làm song song): TV1 chọn công cụ + sơ đồ lab · TV4 câu hỏi + kịch bản · TV2 schema nháp · TV3 checklist + ghi chú deception.
3. **Dựng lab (TV1):** cài Cowrie → smoke test → **gửi ngay log thật cho TV2** → tháo NAT, bật firewall. TV3 kiểm tra cách ly và dựng lại lab.
4. **Thu log (TV4 + TV1):** chạy các kịch bản, lưu log gốc kèm hash, lập bảng đối chiếu.
5. **Xử lý (TV2):** chạy script trên log thật.
6. **Phân tích và kiểm thử** (song song): TV2 làm bảng/biểu đồ, TV4 viết nhận xét, TV3 kiểm thử tích hợp và lập bảng điểm lộ.
7. **Đóng gói báo cáo:** mỗi người viết phần mình, TV4 ghép, TV3 rà soát.

Bước 3 là bước quyết định. Trong lúc chờ lab, TV2 và TV4 vẫn làm được phần của mình (code trên dữ liệu minh họa, viết kịch bản).

## 5. Kịch bản thử nghiệm

| Mã | Nguồn | Dịch vụ | Làm gì |
| --- | --- | --- | --- |
| KB-01 | 1 (lặp lại từ 2) | SSH | Kết nối rồi ngắt, không đăng nhập |
| KB-02 | 1 | SSH | Gõ sai mật khẩu 5 lần, rồi đăng nhập đúng |
| KB-03 | 1 | SSH | Gõ chuỗi lệnh khám phá (`whoami`, `uname -a`, `ps`…), thêm một lệnh không tồn tại |
| KB-05 | 2 | Telnet | Sai 2 lần, đúng 1 lần, gõ vài lệnh |
| KB-04 | 1 | SSH | *(Nâng cao)* tải một tệp vô hại từ máy trong lab |

Thu thập "thành công" nghĩa là mỗi thao tác trong nhật ký đều tìm được sự kiện tương ứng trong log. Không có nghĩa là "tấn công thành công".

## 6. Cần có trước buổi báo cáo tiến độ

- [ ] Bản chốt công cụ có lý do; ghi chú nguyên lý deception
- [ ] Lab chạy SSH + Telnet, cách ly đạt, TV3 dựng lại được theo README
- [ ] Đã chạy KB-01, 02, 03, 05 từ hai nguồn; có log gốc + hash + bảng đối chiếu
- [ ] `events.csv`, `sessions.csv` sinh ra từ log thật
- [ ] Bảng O1, O4, O6; 1–2 điểm lộ; nhận xét kèm giới hạn
- [ ] Bảng tiến độ thật kèm minh chứng; slide 7 phần

Chưa xong phần nào thì báo đúng phần đã đạt, lỗi đang gặp và bước xử lý tiếp. Nếu Cowrie không chạy được, chuyển sang OpenCanary.

## 7. Quy tắc chung

- **Lab không ra Internet**, chỉ tương tác giữa các máy của nhóm.
- **Bắt buộc tạo `etc/userdb.txt`:** mặc định Cowrie chấp nhận gần như mọi mật khẩu, nên nếu bỏ qua bước này thì lần "đăng nhập sai" sẽ thành công.
- **Không sửa log gốc.** Trước mỗi lượt thử, chạy `date -u` trên cả hai máy để ghi giờ UTC.
- **Phân biệt đơn vị đếm:** sự kiện ≠ lần đăng nhập ≠ phiên.
- **Không gắn nhãn khi thiếu căn cứ:** IP trong lab không phải IOC độc hại. Chỉ gán mã ATT&CK khi có sự kiện cụ thể làm căn cứ; dùng tên tactic theo ATT&CK v20 ("Stealth" thay cho "Defense Evasion").
- **Chưa có minh chứng thì ghi "dự kiến"**, không ghi "đã làm".
- **Mỗi người tự lưu minh chứng phần mình.** Nộp bài qua Pull Request, TV3 review.
- **Không commit** mật khẩu thật, khóa SSH, file máy ảo hay slide môn học.

## 8. Nhóm cần trả lời sớm

1. Mỗi người đã làm được gì, minh chứng nằm ở đâu?
2. Máy ai chạy được hai VM hoặc Docker? Ai quen Linux/Docker, ai quen Python/Pandas?
3. Buổi báo cáo dài bao lâu, giảng viên có yêu cầu demo hay mẫu slide không?

## Tra cứu nhanh trong kế hoạch đầy đủ

- Sơ đồ lab và cách ly: mục D.4, D.5
- Cấu hình Cowrie cần chốt: mục D.6
- Chi tiết 13 gói việc: mục E.3, E.4
- Phân công đầy đủ: mục F.4
- Kịch bản, schema, đầu ra phân tích: mục H.1, H.3, H.5
- Mẫu security report cuối: mục H.9
- Dàn ý slide: mục I.1
