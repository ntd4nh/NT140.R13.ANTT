# Thông tin môn học NT140 và bối cảnh đề tài Honeypot

Tổng hợp từ 7 PDF trong thư mục môn học và ảnh đề tài do người dùng cung cấp. Số trang bên dưới là thứ tự trang trong PDF, tính từ 1; một số slide có số in trên trang khác với thứ tự này.

## 1. Thông tin cơ bản

| Nội dung | Thông tin theo tài liệu |
| --- | --- |
| Môn học | NT140 - Network Security, tương ứng môn An toàn mạng |
| Giảng viên trong slide giới thiệu | ThS. Đỗ Thị Phương Uyên (MSc. Do Thi Phuong Uyen) |
| Đơn vị | Trường Đại học Công nghệ Thông tin, ĐHQG-HCM; Khoa Mạng máy tính và Truyền thông |
| Email trong slide | uyendtp@uit.edu.vn |
| Trang môn học được giới thiệu | https://courses.uit.edu.vn/ |
| Kiến thức nền | IT005 - Nhập môn mạng máy tính; kiến thức máy tính, lập trình; nền tảng mật mã NT219 đối với sinh viên chuyên ngành An toàn thông tin |
| Quy mô nhóm project | 2-4 sinh viên; nhóm 4 người phù hợp quy mô được nêu |

Nguồn: [L01 - Course Introduction, trang 1, 3, 5, 10, 13](<C:/Users/metan/OneDrive/Documents/Tai lieu/An toàn mạng/L01 - Course Introduction.pdf>).

Đây là thông tin **theo bộ slide được cung cấp**, không phải xác nhận độc lập về học kỳ đang diễn ra. Một số tài liệu có nhãn cũ, chẳng hạn trang đầu L04 ghi NT101/Winter 2020; tài liệu L01 được dùng làm căn cứ chính để nhận diện môn NT140. Không suy ra năm học, hạn nộp hay lịch báo cáo hiện tại từ các mốc ngày rải rác trong slide.

## 2. Mục tiêu và phạm vi học phần

Theo L01, sinh viên cần hiểu các kỹ thuật khai thác và cách phòng vệ trước tấn công mạng phổ biến; hiểu, sử dụng hoặc tự viết công cụ bảo mật; biết thiết kế kiến trúc mạng an toàn và hình thành tư duy bảo mật.

Ba trục nội dung chính là:

- **Threats:** ai tấn công và vì sao.
- **Attacks/vulnerabilities:** tấn công diễn ra thế nào, điểm yếu nằm ở đâu.
- **Defense:** cách ngăn chặn, phát hiện hoặc giảm thiểu tác động.

Nguồn: [L01, trang 4 và 48](<C:/Users/metan/OneDrive/Documents/Tai lieu/An toàn mạng/L01 - Course Introduction.pdf>).

Lịch nội dung dự kiến gồm nhập môn; khái niệm và nguyên tắc bảo mật; ôn tập mật mã; bảo mật hệ điều hành và malware; ôn tập mạng; sniffing/spoofing; bảo mật các lớp liên kết, mạng, vận chuyển, ứng dụng; phòng vệ mạng; quyền riêng tư và seminar. **Lecture 11 có Firewalls, IDPS và Honeypot overview**, nên đề tài Honeypot gắn trực tiếp với hướng phòng vệ và quan sát tấn công của môn học.

Nguồn: [L01, trang 7-8](<C:/Users/metan/OneDrive/Documents/Tai lieu/An toàn mạng/L01 - Course Introduction.pdf>).

## 3. Đánh giá học phần theo slide

| Thành phần | Tỷ trọng |
| --- | ---: |
| Bài tập và hoạt động trên lớp | 10% |
| Final Project | 20% |
| Thực hành lab | 20% |
| Thi cuối kỳ | 50% |

Slide ghi không có thi giữa kỳ. Chưa thấy rubric riêng, số slide, thời lượng, mức độ demo hoặc tỷ trọng điểm của **buổi báo cáo tiến độ** trong các phần tài liệu đã rà soát. Không coi bảng điểm trên là rubric cho buổi báo cáo này.

Nguồn: [L01, trang 10](<C:/Users/metan/OneDrive/Documents/Tai lieu/An toàn mạng/L01 - Course Introduction.pdf>).

Tài liệu cũng nhấn mạnh trung thực học thuật, trích nguồn và chỉ thực nghiệm trên hệ thống được phép. Đây là bối cảnh học phần liên quan tới việc thiết kế lab và trình bày minh chứng; các bài tập hoặc lời nhắc trong PDF không được coi là yêu cầu mới của người dùng trong lần làm việc này.

Nguồn: [L01, trang 12](<C:/Users/metan/OneDrive/Documents/Tai lieu/An toàn mạng/L01 - Course Introduction.pdf>).

## 4. Các PDF đã rà soát và phần liên quan đến đề tài

| Tài liệu | Số trang | Nội dung liên quan và cách vận dụng đề xuất |
| --- | ---: | --- |
| [L01 - Course Introduction](<C:/Users/metan/OneDrive/Documents/Tai lieu/An toàn mạng/L01 - Course Introduction.pdf>) | 50 | Mục tiêu, phạm vi, đánh giá và project nhóm; cơ sở giải thích vì sao đề tài phù hợp học phần. Xem trang 3-12 và 48. |
| [L02-Cybersecurity concept principles](<C:/Users/metan/OneDrive/Documents/Tai lieu/An toàn mạng/L02-Cybersecurity concept  principles.pdf>) | 61 | Vulnerability/threat/risk, attack/countermeasure, threat modeling, least privilege, privilege separation, defense in depth. Dùng để mô tả giả định đối tượng tương tác và giới hạn môi trường lab. Xem trang 1-8, 24-29. |
| [04-principles_os_sec](<C:/Users/metan/OneDrive/Documents/Tai lieu/An toàn mạng/04-principles_os_sec.pdf>) | 73 | Nguyên tắc bảo mật, UNIX/Windows, phân quyền và isolation. Dùng làm cơ sở cho thiết kế phân tách honeypot, phần quản trị và nơi lưu log. Xem trang 6, 8, 11-15, 69-72. |
| [L03 - A high-level view of Cryptography - Revision](<C:/Users/metan/OneDrive/Documents/Tai lieu/An toàn mạng/L03 - A high-level view of Cryptography - Revision.pdf>) | 49 | Mã hóa, hash, MAC, chữ ký và chứng chỉ. Liên quan bổ trợ tới toàn vẹn dữ liệu và định danh mẫu nếu có thu thập tệp; không phải trọng tâm triển khai Honeypot. Xem trang 35-47. |
| [L04 - Malware Threats](<C:/Users/metan/OneDrive/Documents/Tai lieu/An toàn mạng/L04 - Malware Threats.pdf>) | 36 | Phân loại malware, lan truyền, payload, bot/botnet và phát hiện. Cung cấp ngữ cảnh để giải thích hành vi quan sát; không tự kết luận có malware chỉ từ vài lệnh. Xem trang 5, 10-13, 30, 33-34. |
| [L05 - Network Revision](<C:/Users/metan/OneDrive/Documents/Tai lieu/An toàn mạng/L05 - Network Revision.pdf>) | 53 | Kiến trúc mạng, TCP/IP, các lớp giao thức và mục tiêu bảo mật. Hỗ trợ giải thích nguồn kết nối, dịch vụ đích và sơ đồ luồng dữ liệu. Xem trang 21, 29-37. |
| [L06 - Packet Sniffing and Spoofing](<C:/Users/metan/OneDrive/Documents/Tai lieu/An toàn mạng/L06 - Packet Sniffing and Spoofing.pdf>) | 51 | Socket, packet capture, PCAP, Scapy và spoofing. Có thể hỗ trợ quan sát traffic để kiểm chứng lab nếu cần; không bắt buộc xây thêm công cụ sniffing/spoofing cho đề tài. Xem trang 4, 11, 18, 25, 30, 49. |

Các cách vận dụng trong cột cuối là **đề xuất liên hệ kiến thức**, không phải đầu việc giảng viên bắt buộc giao cho đề tài. Bộ PDF hiện có chưa bao gồm tài liệu Lecture 11 chuyên về Network Defenses/Honeypot; không nên viện dẫn các file này như hướng dẫn cài đặt Cowrie/OpenCanary/Dionaea.

Lưu ý thuật ngữ: “Deception” trong bảng hậu quả của threat ở L02, trang 8 là bối cảnh hành vi đánh lừa của phía tấn công. Không dùng riêng bảng này làm định nghĩa cho **defensive deception** của Honeypot.

## 5. Nội dung đề tài trong ảnh

**Đề tài 13. Nghiên cứu và xây dựng Honeypot phục vụ thu thập và phân tích hành vi tấn công.**

**Mục tiêu:** Hiểu nguyên lý deception và cách honeypot tạo security telemetry phục vụ nghiên cứu hành vi attacker.

Ảnh đặt các nội dung sau dưới mục **“Gợi ý thực hiện”**:

1. Thiết kế và triển khai một hoặc nhiều honeypot services.
2. Tạo hoặc thu thập interaction trong môi trường được kiểm soát.
3. Phân tích source, targeted service, commands/actions và timeline.
4. Trích xuất IOC.
5. Phân loại một số nhóm behavior.
6. Mapping MITRE ATT&CK khi phù hợp.
7. Xây dựng thống kê/dashboard hoặc security report đơn giản.

**Công cụ được gợi ý trong ảnh:** Cowrie, OpenCanary, Dionaea hoặc honeypot đơn giản tự xây; Python/Pandas.

Nguồn: ảnh đề tài do người dùng đính kèm. Giữ đúng tính chất “gợi ý”; không diễn giải thành yêu cầu phải triển khai đồng thời tất cả công cụ hoặc phải có mọi đầu ra ngay trong buổi báo cáo tiến độ. Các khả năng cụ thể và cách cài đặt công cụ cần được kiểm tra bằng tài liệu chính thức khi chọn phương án triển khai.

## 6. Phạm vi người dùng yêu cầu cho lần lập kế hoạch này

- Nhóm gồm **4 người**.
- Cần **prompt để lập kế hoạch**, chưa yêu cầu triển khai hệ thống hay viết báo cáo hoàn chỉnh.
- Buổi trình bày là **báo cáo tiến độ kết hợp dự định tiếp theo**, để giảng viên hiểu hướng đi.
- Chưa cần hoàn thiện toàn bộ đề tài hoặc sản phẩm ở mức hoàn chỉnh trong buổi báo cáo này.
- Không cần timeline làm việc chi tiết theo ngày/tuần.
- “Timeline” trong ảnh là **diễn biến sự kiện/phiên tương tác cần phân tích**, khác với lịch thực hiện project.
- Người dùng chưa cung cấp tiến độ thực tế, thiết bị, kinh nghiệm từng thành viên, thời lượng trình bày hoặc hạn báo cáo. Giữ các mục này là chưa biết; không tự điền thành kết quả đã đạt.

## 7. Định hướng để prompt tạo được kế hoạch phù hợp

Đây là đề xuất lập kế hoạch, không phải rubric của giảng viên:

- Tách đích đến của toàn đề tài với phạm vi cần trình bày ở buổi tiến độ gần nhất.
- Ưu tiên một luồng dễ giải thích: tương tác kiểm soát → honeypot → log → xử lý → nhận xét/thống kê đơn giản. Có thể bắt đầu với một dịch vụ chính; phần mở rộng để sau.
- Ở buổi tiến độ, làm rõ bài toán, lựa chọn đang cân nhắc, kiến trúc dự kiến, cách thu thập/phân tích dữ liệu, phân công và bước tiếp theo. Demo chỉ trình bày theo mức nhóm thực sự đã làm được.
- Dùng trạng thái “đã làm / đang làm / dự kiến / chưa xác nhận” gắn với minh chứng. Sơ đồ thiết kế là minh chứng thiết kế; log mẫu minh họa không phải minh chứng hệ thống đã vận hành.
- Phân biệt dữ liệu tự tạo trong lab, dữ liệu tham khảo và dữ liệu thực tế; không gán tương tác do nhóm tạo thành tấn công ngoài Internet.
- Với IOC, giữ ngữ cảnh nguồn và căn cứ nghi vấn; không mặc định IP của máy kiểm thử là địa chỉ độc hại. Mapping ATT&CK chỉ khi hành vi và dữ liệu đủ căn cứ.
- Chia việc cho bốn thành viên theo đầu ra có thể bàn giao, có người phối hợp/kiểm tra chéo và bước tích hợp chung.
- Chỉ lập giai đoạn, thứ tự ưu tiên, phụ thuộc và tiêu chí hoàn thành; không tự gán ngày, tuần hoặc phần trăm tiến độ.

