# Yêu cầu: mở rộng kịch bản tấn công SSH (và Telnet) vào honeypot

**Từ:** TV1 · **Gửi:** TV4 (người viết `docs/03_kich_ban_thu_nghiem.md`) · **Review:** TV3 · **Ngày:** 2026-11-22
**Trạng thái:** chờ TV4 nhận

## 1. Vì sao cần mở rộng

Cô nhận xét nhóm nên **tập trung vào tấn công SSH và Telnet, và thể hiện rõ vai trò của honeypot**.

Kịch bản hiện có (KB-01 → KB-05) mới phủ 4 giai đoạn, mỗi giai đoạn chỉ một kiểu:

| Giai đoạn | Kịch bản hiện có |
| --- | --- |
| Dò quét | KB-01 |
| Đoán mật khẩu | KB-02 (SSH), KB-05 (Telnet) |
| Khám phá sau khi vào | KB-03 (SSH), KB-05 (Telnet) |
| Đưa công cụ vào | KB-04 (lượt riêng) |

Còn thiếu:
- Những kiểu tấn công SSH mà honeypot ngoài thực tế ghi nhận nhiều.
- Nhóm hành vi **B5** (duy trì truy cập / xóa dấu vết). Hiện chưa kịch bản nào tạo ra B5, nên bộ phân loại B1–B5 (kế hoạch H.6) không đánh giá được.

Mỗi kịch bản mới phải **chứng minh thêm một điều về honeypot**, không chỉ thêm số liệu.

## 2. Kịch bản cần bổ sung

Mã đề xuất bắt đầu từ KB-06. TV4 được đổi mã, đổi thứ tự cho hợp với `docs/03`.

### Bắt buộc (SSH)

| Mã | Kịch bản | Mô tả ở mức hành vi | Chứng minh được gì về honeypot | Nhãn H.6 kỳ vọng | ATT&CK ứng viên |
| --- | --- | --- | --- | --- | --- |
| KB-06 | **Rải mật khẩu** | Một mật khẩu giả thử trên nhiều username (ví dụ 4 username), mỗi username một lần | Chỉ nhờ log mà phân biệt được *rải mật khẩu* với *đoán mật khẩu* (KB-02) | B2 (kiểu rải) | T1110.003 |
| KB-07 | **Bot tự động** | Đăng nhập rồi gửi lệnh kèm ngay khi kết nối, **không mở shell tương tác**; vài lệnh xem thông tin máy; phiên chỉ vài giây | Phân biệt được bot với người gõ tay, nhờ cách gửi lệnh, không có kích thước terminal và thời lượng phiên ngắn | B3 (+ thuộc tính "tự động") | T1059.004, T1082, T1033 |
| KB-08 | **Duy trì truy cập và xóa dấu vết** | Trong shell giả: thêm một **khóa SSH giả** vào `authorized_keys`, thêm một dòng lịch chạy (cron) giả, rồi xóa lịch sử lệnh | Bắt được ý đồ ở lại lâu dài; giữ được chuỗi khóa của "kẻ tấn công" làm IOC; lấp nhóm B5 | B5 | T1098.004, T1053.003, T1070.003 |

### Nên có (Telnet, để Telnet không chỉ là bản sao của SSH)

| Mã | Kịch bản | Mô tả ở mức hành vi | Chứng minh được gì | Nhãn H.6 kỳ vọng | ATT&CK ứng viên |
| --- | --- | --- | --- | --- | --- |
| KB-09 | **Kiểu botnet IoT qua Telnet** | Từ **VM-A** (để Telnet có cả hai nguồn): thử nhanh vài cặp tài khoản "mặc định" giả trong một kết nối, vào được thì chạy liền vài lệnh xem loại thiết bị rồi thoát, gần như không nghỉ | Honeypot nhận ra kiểu tấn công tự động nhắm thiết bị IoT, khác kiểu tấn công từng bước trên SSH | B2 + B3 | T1110, T1082 |

### Tùy chọn

| Mã | Kịch bản | Ghi chú |
| --- | --- | --- |
| KB-10 | **Thử cặp tài khoản bị lộ** (mỗi username một mật khẩu khác nhau, mỗi cặp một lần) | T1110.004. Chỉ làm nếu còn thời gian; cần một quy tắc phân loại phân biệt được với KB-06 |

## 3. Ràng buộc

- Chỉ nhắm `192.168.239.20` cổng `2222`, `2223`. Không nhắm máy nào khác.
- **Mọi tài khoản, mật khẩu, khóa SSH và dòng cron đều là dữ liệu giả do nhóm tự đặt**, ghi rõ "giả của lab". Khóa SSH giả chỉ là một chuỗi văn bản, không tạo cặp khóa thật.
- Chỉ dùng client SSH/Telnet và script như các kịch bản hiện có. Không dùng công cụ tấn công bên ngoài, không tải hay chạy mã độc thật.
- Giữ `userdb.txt` một dòng `labuser:x:LabOnly-2026`. Nếu kịch bản cần đổi, báo TV1 trước.
- Theo quy ước nhật ký hiện có (`experiments/quy_uoc_nhat_ky.md`): nhãn `thao_tac`, giờ UTC, khoảng nghỉ giữa hai kịch bản cùng nguồn, cùng cổng.

## 4. Lưu ý kỹ thuật từ TV1

- Bộ xử lý của TV2 (`analysis/process_run.py`) **không giới hạn** `scenario_id`. Thêm KB-06 trở đi không phải sửa code của TV2.
- **Rải mật khẩu qua OpenSSH:** mỗi username phải là một kết nối riêng (username cố định trong một kết nối). KB-06 sẽ có nhiều phiên.
- **Gửi lệnh không mở shell:** khi TV1 chạy thử ngày 10/11, Cowrie ghi **một** `cowrie.command.input` chứa nguyên chuỗi lệnh (ví dụ `whoami; uname -a; hostname`). Log đó không lưu trong repo, nên ghi **[XM]** và xác nhận ở phiên chuẩn bị. Chưa biết kiểu phiên này có sinh file TTY hay `cowrie.client.size` không: ghi [XM].
- **Lệnh trong KB-07, KB-08:** có lệnh Cowrie có thể không hỗ trợ (ví dụ `crontab`, `nproc`). Nếu có `cowrie.command.failed` thì cũng là dữ liệu tốt cho bảng điểm lộ O7. Ghi [XM] cho tới khi chạy thử.
- **Hệ thống file giả:** thay đổi trong shell giả (thêm khóa, sửa file) có thể không còn ở phiên sau. Không thiết kế bước nào phụ thuộc vào việc file còn lại giữa hai phiên.
- **Telnet:** số lần thử mật khẩu Cowrie cho phép trong một kết nối vẫn là [XM] (như ghi chú ở KB-05). KB-09 nên chỉ cần tối đa 3 lần thử.

## 5. Sản phẩm mong đợi từ TV4

1. Thêm các mục KB mới vào `docs/03_kich_ban_thu_nghiem.md`, cùng định dạng với KB hiện có: mục tiêu, nguồn → đích, bảng bước, sự kiện mong đợi, đơn vị đếm, đạt/không đạt.
2. Cập nhật mục 0.2 (tài khoản giả), 0.4 (thứ tự trong RUN và **tổng mong đợi** của một RUN).
3. Script chạy các kịch bản mới: thêm vào `kb_vma.py` / `kb_host.py`, hoặc viết file mới.
4. Bổ sung nhãn kỳ vọng vào bảng đánh giá phân loại (kế hoạch H.6) và các dòng ATT&CK tương ứng (H.8), trạng thái "dự kiến".

## 6. Sau khi xong

- TV3 review kịch bản và script.
- TV1 chạy phiên chuẩn bị rồi **RUN-01** trên lab với đủ kịch bản cũ và mới, sau đó xuất log cho TV2 (BG-06).
- RUN-01 sẽ chờ bản kịch bản này, để không phải chạy lại.
