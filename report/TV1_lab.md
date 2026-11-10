# Phần báo cáo tiến độ của TV1 – Dựng lab (BG-12)

**Người viết:** TV1 · **Ngày:** 2026-11-10 · **Dùng cho:** TV4 ghép báo cáo (WP-10) theo dàn ý I.1 của kế hoạch

Mọi khẳng định "đã làm" dưới đây có minh chứng trong repo. Việc chưa làm ghi "dự kiến".

---

## 1. Dòng cho bảng tiến độ B.3

| Hạng mục | Việc thực tế đã thực hiện | Kết quả/sản phẩm hiện có | Mức độ hoàn thành | Minh chứng | Thành viên | Phần còn thiếu/vướng mắc |
| --- | --- | --- | --- | --- | --- | --- |
| 2. Nghiên cứu và chọn công cụ | Đọc tài liệu chính thức Cowrie, OpenCanary, Dionaea; so sánh; chọn Cowrie làm chính, OpenCanary dự phòng, loại Dionaea (ngừng phát triển từ 2021) | Bản quyết định công cụ | Đã hoàn thành phần công cụ; đã chạy thật Cowrie 3.1.6 nên các nhận định cài đặt đã được kiểm chứng | `docs/01_quyet_dinh_pham_vi_cong_cu.md` | TV1 | Chờ TV3 review; phần phạm vi (mục 1) do TV4 viết |
| 3. Thiết kế lab | Sơ đồ hai VM + máy host, mạng host-only, bảng kết nối, luật firewall, 6 lớp cách ly | Sơ đồ lab có IP/cổng thật | Đã hoàn thành, **đã dựng đúng thiết kế** | `docs/02_so_do_lab.md` (mục 8 ghi thông số thật) | TV1 | Chờ TV3 review theo checklist RV-THIẾT-KẾ |
| 4. Cài đặt/cấu hình | Dựng VM-H và VM-A trên VMware; cài Cowrie bằng pip, chạy bằng user không phải root; bật Telnet; `userdb` riêng; tắt chuyển tiếp cổng; tháo NAT, bật ufw | Honeypot chạy SSH :2222 và Telnet :2223, nhận kết nối từ cả hai nguồn | Đã hoàn thành | `Implement/lab/README_chay_lab.md`, `Implement/lab/cowrie/` | TV1 | `userdb` còn là bản tạm, chờ danh sách credential của TV4 (BG-01) |
| 5. Tạo tương tác và thu log | Smoke test: từ mỗi nguồn chạy SSH và Telnet (đăng nhập sai, đăng nhập đúng, `whoami`, `exit`); đối chiếu từng thao tác với sự kiện trong log | Log gốc 58 sự kiện, 8 phiên, kèm SHA-256 | **Đang làm**: có tương tác kiểm soát truy ngược được sang log gốc; **chưa** chạy lượt thử theo kịch bản (RUN-01) | `evidence/smoke_test/` (README có bảng thao tác ↔ giờ UTC) | TV1 | RUN-01 chờ kịch bản của TV4 và biên bản cách ly của TV3 |

Cách ly (minh chứng cho hạng mục 3–4): `evidence/kiem_tra_cach_ly_TV1.md`. Đây là bản tự kiểm của TV1; biên bản chính thức do TV3 lập (BG-04).

## 2. Dòng cho bảng đóng góp B.5

| Thành viên | Việc đã làm | Sản phẩm/minh chứng |
| --- | --- | --- |
| TV1 | Chọn công cụ; thiết kế lab; dựng hai VM và Cowrie; smoke test hai nguồn × hai dịch vụ; tự kiểm cách ly; liệt kê yếu tố mồi và điểm lộ ban đầu; trả lời các câu hỏi xác minh của hợp đồng dữ liệu | `docs/01`, `docs/02`, `Implement/lab/`, `evidence/smoke_test/`, `evidence/kiem_tra_cach_ly_TV1.md`, `evidence/xac_minh_hop_dong_du_lieu.md`, các báo cáo trong `docs/bao_cao_cong_viec/` |

---

## 3. Nội dung cho từng phần slide

### Phần 2 – Nhóm đã làm được tới đâu (dòng của TV1)

- **Đã đạt mức cơ bản:** lab dựng xong, đúng sơ đồ; Cowrie chạy SSH và Telnet; cả hai nguồn kết nối được; tự kiểm cách ly đạt. Minh chứng: `evidence/smoke_test/`, `evidence/kiem_tra_cach_ly_TV1.md`.
- **Đã làm sâu hơn:**
  - Tắt chuyển tiếp cổng SSH của Cowrie (mặc định đang bật).
  - Gỡ thiết bị thừa của VM, đồng bộ giờ VM theo host.
  - Liệt kê 13 yếu tố mồi và 5 điểm lộ thấy được khi chạy thử.
- **Đang làm – chưa đạt:**
  - Chưa có lượt thử theo kịch bản (RUN-01).
  - TV3 chưa dựng lại lab theo README.

### Phần 3 – Thiết kế và lựa chọn công cụ

**Vì sao chọn Cowrie:**
- Giả lập cả SSH và Telnet, có shell giả để quan sát lệnh.
- Log JSON mỗi dòng một sự kiện, mỗi sự kiện có mã phiên. Nhờ vậy dựng được timeline phiên và đọc thẳng bằng Pandas.
- Đang được phát triển; bản dùng là 3.1.6.

**Dự phòng:** OpenCanary. Nhưng SSH của OpenCanary không cho đăng nhập và không có shell, nên chỉ ghi được lần thử mật khẩu.

**Loại:** Dionaea. Bản phát hành cuối là 11/2020, commit cuối là 02/2021.

**Lab đã dựng** (hình: sơ đồ Mermaid trong `docs/02_so_do_lab.md`, ghi "đã dựng"):

| Máy | Vai trò | IP |
| --- | --- | --- |
| Windows host (VMware Workstation 25H2, 16 GB RAM) | Nguồn 2 + quản trị | `192.168.239.1` |
| VM-A, Ubuntu Server 24.04.5 | Nguồn 1 | `192.168.239.10` |
| VM-H, Ubuntu Server 24.04.5 | Honeypot Cowrie, SSH :2222, Telnet :2223 | `192.168.239.20` |

**Cách ly (6 lớp):**
1. Mạng host-only, không có card NAT.
2. ufw chặn mọi chiều ra; chỉ máy host vào được cổng quản trị 22.
3. Tắt Shared Folders, kéo-thả, copy-paste.
4. Cowrie chạy bằng user không có quyền quản trị.
5. Snapshot để khôi phục.
6. Thói quen: tắt VM khi không dùng, không đưa mật khẩu thật vào VM.

### Phần 4 – Thu thập (phần log của TV1)

Đoạn log gốc gợi ý đưa lên slide: một phiên Telnet từ nguồn 1 (session `e02625c405d3`), trích từ `evidence/smoke_test/cowrie.json`.

```text
14:47:49.818  cowrie.session.connect   192.168.239.10  telnet
14:47:49.862  cowrie.login.failed      labuser / sai-mat-khau
14:47:49.906  cowrie.login.success     labuser / LabOnly-2026
14:47:51.933  cowrie.command.input     whoami
14:47:53.009  cowrie.command.input     exit
              cowrie.session.closed    duration_ms = 3194
```

Thông điệp: mỗi thao tác phía client đều có sự kiện tương ứng, cùng một mã phiên, giờ UTC tới micro giây. Mật khẩu trên là mật khẩu giả của lab.

**Ma trận nguồn × dịch vụ của smoke test** (đếm phiên có đăng nhập, không tính 2 phiên kiểm tra cổng):

| | SSH :2222 | Telnet :2223 |
| --- | --- | --- |
| Nguồn 1 (VM-A, `.10`) | 2 phiên (1 sai, 1 đúng) | 1 phiên (sai rồi đúng) |
| Nguồn 2 (Windows, `.1`) | 2 phiên (1 sai, 1 đúng) | 1 phiên (sai rồi đúng) |

### Phần 5 – Điểm lộ ban đầu (đầu vào cho TV3)

Thấy được khi chạy thử, chi tiết ở `Implement/lab/cowrie/README.md`:
1. Banner SSH công bố OpenSSH 9.2p1, nhưng `ssh -V` trong shell giả trả 7.9p1.
2. `wget` in "connected." rồi treo, trong khi thực tế không có mạng.
3. `curl -m` báo không hiểu tùy chọn.
4. Tên máy `svr04` là giá trị mặc định nổi tiếng của Cowrie.

### Phần 6 – Vướng mắc đã gặp và cách xử lý

| Vướng mắc | Cách xử lý |
| --- | --- |
| Trình cài Ubuntu chỉ dành 10 GB cho ổ hệ thống dù đĩa 20 GB | Mở rộng bằng `lvextend` khi còn mạng NAT |
| Tên card mạng là `ens32`, khác `ens33` trong hướng dẫn | Lệnh đặt IP tự tìm tên card nên không ảnh hưởng; đã ghi lại vào README |
| Cowrie mặc định cho phép chuyển tiếp cổng SSH | Đã tắt; kiểm tra lại thì Cowrie từ chối (`unknown channel: direct-tcpip`) |
| VM không có Internet nên không tự chỉnh giờ được | Bật đồng bộ giờ với host của VMware; ba máy lệch dưới 1 giây |
| Các phiên gõ giống nhau dùng chung một file TTY | Đã báo TV2 cách ghép bằng trường `ttylog` |
| Telnet Client của Windows chưa bật | Smoke test dùng Python thay thế; cần bật trước khi chạy KB-05 bằng tay |

### Phần 7 – Dự định tiếp theo của TV1

1. Thay `userdb.txt` theo danh sách credential của TV4 (BG-01).
2. Cùng TV4 chạy RUN-01, lấy log gốc về `data/raw/RUN-01/` kèm SHA-256 và `run_note.txt` (BG-06).
3. Kiểm tra lại biên bản cách ly của TV3 (BG-04).
4. Tùy chọn: cho Cowrie tự chạy khi bật VM, viết script dựng lại VM-H, thêm OpenCanary sau buổi báo cáo.

---

## 4. Nếu demo trực tiếp (dự kiến, khoảng 2 phút)

**Chuẩn bị trước:**
- Bật VM-H và VM-A.
- Mở sẵn hai cửa sổ: một cửa sổ SSH vào VM-A, một cửa sổ SSH vào VM-H để xem log.

**Trên VM-H** (`labadmin`), theo dõi log trực tiếp:

```bash
tail -f /home/cowrie/var/log/cowrie/cowrie.json | jq -r '[.timestamp[11:19], .eventid, .src_ip, (.username // .input // "")] | @tsv'
```

**Trên VM-A**, đăng nhập vào honeypot, gõ sai rồi gõ đúng mật khẩu, sau đó gõ vài lệnh:

```bash
ssh -p 2222 -o PubkeyAuthentication=no labuser@192.168.239.20
```

Mỗi lần gõ, cửa sổ log hiện thêm một dòng tương ứng.

**Phương án dự phòng nếu lab lỗi lúc trình bày:** dùng ảnh chụp và đoạn log gốc ở phần 4.
