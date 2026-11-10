# Bàn giao giữa các thành viên

File này dùng cho **AI agent** của từng thành viên (và chính các thành viên). Mỗi khi agent làm xong một việc, agent phải đọc file này, kiểm tra việc vừa xong có kích hoạt bàn giao nào không, rồi yêu cầu bàn giao cho đúng người.

Mã gói việc (WP-xx) và quy ước thư mục theo [kế hoạch đầy đủ](Plan/KE_HOACH_BAO_CAO_TIEN_DO_HONEYPOT.md) (mục E.3–E.5). Nếu nhóm đặt file ở chỗ khác, cập nhật cột "Vị trí" trong Bảng A.

## Thành viên

| Vai | Tên | GitHub username |
| --- | --- | --- |
| TV1 – Dựng lab | [CẦN BỔ SUNG] | [CẦN BỔ SUNG] |
| TV2 – Xử lý dữ liệu | [CẦN BỔ SUNG] | [CẦN BỔ SUNG] |
| TV3 – Review, kiểm thử, deception | [CẦN BỔ SUNG] | [CẦN BỔ SUNG] |
| TV4 – Thực nghiệm, tổng hợp | [CẦN BỔ SUNG] | [CẦN BỔ SUNG] |

---

## Quy trình cho AI agent

### Khi vừa làm xong một việc (phía gửi)

1. Chạy `git pull` để có bản mới nhất của file này.
2. Xác định **vai của người dùng** (TV1–TV4) và **mã gói việc vừa xong**. Không rõ thì hỏi người dùng, không tự đoán.
   - Nếu chưa có, viết báo cáo ngắn của việc vừa xong vào `docs/bao_cao_cong_viec/` theo mẫu trong README của thư mục đó.
3. Tra **Bảng A**: lấy các dòng có cột "Từ" là vai của người dùng và cột "Kích hoạt khi" khớp với việc vừa xong.
4. Với từng dòng, kiểm tra **từng điều kiện sẵn sàng** bằng cách mở file hoặc chạy lệnh kiểm tra thật. Ghi kết quả từng điều kiện: đạt hay không, căn cứ là gì.
5. **Nếu tất cả điều kiện đạt:**
   - Đổi cột "Trạng thái" của dòng đó thành `Đã gửi`.
   - Thêm một dòng vào **Nhật ký bàn giao** ở cuối file.
   - Commit với message `ban-giao: BG-xx <tóm tắt>` rồi push.
   - Soạn tin yêu cầu bàn giao theo **Mẫu yêu cầu** và đưa cho người dùng gửi tới người nhận.
   - Chỉ tạo GitHub Issue hoặc comment khi người dùng đồng ý. Khi đó gắn nhãn `ban-giao`, và chỉ mention username đã điền trong bảng Thành viên.
6. **Nếu còn điều kiện chưa đạt:** giữ nguyên trạng thái, báo người dùng điều kiện nào thiếu và cần làm thêm gì. Không gửi bàn giao dở dang.
7. Tra **Bảng B** và soạn yêu cầu review sản phẩm vừa xong cho người review mặc định.

### Khi nhận bàn giao (phía nhận)

1. Đọc dòng nhật ký của mã BG tương ứng, mở đúng file hoặc commit được ghi.
2. Tự kiểm tra lại các điều kiện sẵn sàng từ phía người nhận.
3. Nếu đạt: đổi trạng thái thành `Đã nhận`, ghi nhật ký, commit `ban-giao: nhận BG-xx`.
4. Nếu chưa đạt: đổi trạng thái thành `Trả lại`, ghi rõ lý do vào nhật ký và báo người dùng để chuyển lại cho người gửi.

### Quy tắc

- Không đánh dấu đạt khi chưa kiểm tra thật. Không bịa log, số liệu hay kết quả.
- Agent không làm thay việc của người nhận. Bàn giao chỉ chuyển sản phẩm và mở khóa việc tiếp theo.
- `Đã gửi` không có nghĩa là đã qua review; review theo Bảng B là bước riêng.
- Dữ liệu minh họa phải ghi nhãn "minh họa" và không được dùng để bàn giao thay cho log thật.
- Không đưa mật khẩu thật, khóa SSH, file máy ảo hay slide môn học vào nội dung bàn giao.
- Mỗi lần sửa file này chỉ sửa đúng dòng liên quan, commit ngay, để tránh xung đột khi nhiều người cùng sửa.

Trạng thái hợp lệ: `Chưa` · `Đã gửi` · `Đã nhận` · `Trả lại`

---

## Bảng A – Các điểm bàn giao

| Mã | Từ → Đến | Kích hoạt khi | Bàn giao gì | Vị trí | Điều kiện sẵn sàng (phải kiểm tra được) | Mở khóa việc | Trạng thái |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **BG-01** | TV4 → TV1 | WP-04 xong phần credential | Danh sách credential cho từng kịch bản: cặp bị từ chối, cặp được chấp nhận | `docs/03_kich_ban_thu_nghiem.md` | Mỗi kịch bản KB-02, KB-05 có danh sách cặp sai/đúng; không có mật khẩu thật của thành viên; có định dạng dòng `userdb` tương ứng | TV1 tạo `etc/userdb.txt` (WP-03) | Chưa |
| **BG-02** | TV1 → TV2 | WP-03 xong smoke test | Log smoke test thật | `evidence/smoke_test/` | Log có sự kiện kết nối và đóng phiên cho **cả SSH và Telnet**, từ **cả hai nguồn**; mỗi dòng là một JSON đọc được; ghi kèm phiên bản Cowrie và cách cài | TV2 chốt schema (WP-05) | Đã gửi |
| **BG-03** | TV1 → TV3 | WP-03 xong cài đặt và README | Lab chạy được, README, cấu hình đã làm sạch | `Implement/lab/README_chay_lab.md`, `Implement/lab/cowrie/` | README có đủ bước dựng lại; honeypot chạy bằng user không phải root; đã tháo NAT và bật firewall; cấu hình không chứa khóa hay mật khẩu thật | TV3 kiểm tra cách ly, dựng lại lab | Đã gửi |
| **BG-04** | TV3 → TV4, TV1 | Kiểm tra cách ly đạt | Biên bản kiểm tra cách ly | `review/kiem_tra_cach_ly.md` | Mọi thử nghiệm kết nối ra Internet từ VM-H và từ shell giả lập đều thất bại; có lệnh và kết quả kèm theo; TV1 đã kiểm tra lại biên bản | TV4 được chạy thử nghiệm (WP-06) | Chưa |
| **BG-05** | TV2 → TV1 | WP-05 chốt | Hợp đồng dữ liệu A→B | `docs/04_hop_dong_du_lieu.md` | Tên trường đã đối chiếu với log smoke test thật; có quy định nơi chuyển log, cách giữ log gốc, múi giờ UTC, xử lý trường thiếu; TV3 đã review | TV1 xuất log đúng quy định | Chưa |
| **BG-06** | TV1 + TV4 → TV2 | WP-06 xong một lượt chạy | Log gốc của lượt chạy, nhật ký thử nghiệm, bảng đối chiếu | `data/raw/RUN-xx/`, `experiments/` | Có `SHA256SUMS` và hash khớp; nhật ký ghi giờ UTC và độ lệch giờ; mọi bước trong nhật ký có sự kiện tương ứng hoặc có giải thích | TV2 chạy script trên dữ liệu thật (WP-07) | Chưa |
| **BG-07** | TV4 → TV3 | WP-06 xong KB-03 | Transcript KB-03 và kết quả chạy cùng các lệnh trên VM-A | `experiments/transcript/` | Có cả hai bản, cùng danh sách lệnh, cùng thứ tự | TV3 lập bảng điểm lộ (WP-13) | Chưa |
| **BG-08** | TV1 → TV3 | WP-03 xong cấu hình | Danh sách yếu tố mồi trong cấu hình Cowrie | `Implement/lab/cowrie/` hoặc ghi chú kèm | Liệt kê shell giả lập, hệ thống file giả, tên máy, phiên bản SSH công bố, `userdb`; ghi rõ cái nào giữ mặc định, cái nào đã đổi | TV3 hoàn thiện ghi chú deception (WP-13) | Đã gửi |
| **BG-09** | TV2 → TV4 | WP-08 xong bảng/biểu đồ | Bảng O1, O4, O6 (và O2, O3 nếu có) | `results/RUN-xx/` | Sinh ra từ log thật bằng script; mỗi bảng ghi đơn vị đếm (sự kiện, lần đăng nhập hay phiên) và nguồn dữ liệu | TV4 viết nhận xét (WP-08) | Chưa |
| **BG-10** | TV2 → TV3 | WP-07 xong | Script xử lý và README cách chạy | `analysis/` | Chạy được bằng một lệnh cho mỗi lượt; không ghi vào `data/raw/`; có báo cáo chất lượng dữ liệu | TV3 kiểm thử tích hợp (WP-09) | Chưa |
| **BG-11** | TV3 → TV1, TV2 | WP-09 phát hiện lỗi | Danh sách lỗi kèm mức độ | `review/issues.md` | Mỗi lỗi có bước tái hiện, kết quả mong đợi, kết quả thực tế | Người xây sửa; xong thì gửi lại để TV3 kiểm tra lại | Chưa |
| **BG-12** | TV1, TV2, TV3 → TV4 | Trước buổi báo cáo | Phần viết của từng người: cách làm, kết quả, minh chứng, vướng mắc | `report/` | Mọi khẳng định "đã làm" có minh chứng; việc chưa xong ghi "dự kiến" | TV4 ghép báo cáo (WP-10) | Chưa |
| **BG-13** | TV4 → TV3 | WP-10 ghép xong | Báo cáo/slide đã ghép | `report/` | Đủ 7 phần theo dàn ý; phần "đã làm được tới đâu" đứng trước phần "dự định tiếp theo" | TV3 rà soát lần cuối | Chưa |

---

## Bảng B – Người review mặc định

| Sản phẩm của | Sản phẩm | Người review |
| --- | --- | --- |
| TV1 | Quyết định công cụ, sơ đồ lab, cấu hình, README, log | TV3 |
| TV2 | Hợp đồng dữ liệu, script, bảng/biểu đồ | TV3 |
| TV4 | Kịch bản, nhật ký, bảng đối chiếu | TV3 |
| TV4 | Nhận xét | TV3; TV2 kiểm tra số liệu |
| TV3 | Biên bản cách ly | TV1 |
| TV3 | Báo cáo kiểm thử tích hợp | TV4 (lặp lại một phép đối chiếu) |
| TV3 | Ghi chú deception, bảng điểm lộ | TV4; TV1 kiểm tra phần cấu hình |
| TV4 | Báo cáo/slide đã ghép | TV3 |

---

## Mẫu yêu cầu bàn giao

```text
[BÀN GIAO BG-xx] <tên ngắn>
Từ: TVx (<tên>) → Đến: TVy (<tên>)
Sản phẩm: <mô tả ngắn>
Vị trí: <đường dẫn trong repo> @ <mã commit>
Báo cáo: docs/bao_cao_cong_viec/<tên file>.md
Điều kiện đã kiểm tra:
- [x] <điều kiện 1> – <căn cứ>
- [x] <điều kiện 2> – <căn cứ>
Việc được mở khóa: <WP-xx của người nhận>
Lưu ý / giới hạn: <nếu có>
Người nhận xác nhận: đổi trạng thái BG-xx trong BAN_GIAO.md thành "Đã nhận" hoặc "Trả lại" kèm lý do.
```

## Mẫu yêu cầu review

```text
[REVIEW] <tên sản phẩm> (<WP-xx>)
Người làm: TVx → Người review: TVy
Vị trí: <đường dẫn> @ <mã commit>
Cần kiểm tra theo: checklist <RV-...> (kế hoạch mục F.6)
```

---

## Nhật ký bàn giao

Chỉ thêm dòng mới ở cuối bảng, không sửa dòng cũ.

| Thời điểm (UTC) | Mã | Từ → Đến | Trạng thái | Commit / đường dẫn | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| 2026-11-10 14:56 | BG-02 | TV1 → TV2 | Đã gửi | `448fee5` · `evidence/smoke_test/` | SSH + Telnet từ `192.168.239.10` và `.1`; 58 dòng JSON; Cowrie 3.1.6 cài bằng pip. Đọc README trong thư mục trước |
| 2026-11-10 14:56 | BG-03 | TV1 → TV3 | Đã gửi | `448fee5` · `Implement/lab/README_chay_lab.md`, `Implement/lab/cowrie/` | Lab chạy trên máy TV1; tự kiểm cách ly ở `evidence/kiem_tra_cach_ly_TV1.md`. `userdb.txt` còn là bản tạm (chờ BG-01) |
| 2026-11-10 14:56 | BG-08 | TV1 → TV3 | Đã gửi | `448fee5` · `Implement/lab/cowrie/README.md` | 13 yếu tố mồi, kèm 5 điểm lộ đã gặp khi chạy thử |
