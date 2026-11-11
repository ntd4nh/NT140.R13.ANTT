# Nguyên lý deception và cách honeypot sinh telemetry (WP-13)

**Người viết:** TV3 · **Ngày:** 2026-11-11 · **Trạng thái:** bản ghi chú + quan sát điểm lộ ban đầu; chờ TV4 review, TV1 kiểm tra phần cấu hình (mục 4)

Mọi ví dụ về sự kiện trỏ tới log thật `evidence/smoke_test/cowrie.json` (viết tắt `json:<dòng>`) và cấu hình thật `Implement/lab/cowrie/cowrie.cfg` (viết tắt `cfg:<dòng>`). Phần chưa có trong log của repo ghi **dự kiến**.

## 1. Deception trong phòng vệ

Deception (đánh lừa) là đặt vào hệ thống những tài nguyên **giả nhưng trông như thật**: một máy chủ, một tài khoản, một file. Người dùng hợp lệ không có lý do chạm vào chúng, nên **mọi tương tác với tài nguyên giả đều đáng ngờ**. Nhờ vậy deception cho ba lợi ích:

- **Phát hiện** với tỉ lệ báo động giả thấp: không cần phân biệt lưu lượng tốt/xấu như IDS, vì tài nguyên giả vốn không có lưu lượng tốt.
- **Làm chậm** kẻ tấn công: thời gian họ dành cho máy giả là thời gian không dành cho máy thật.
- **Nghiên cứu** hành vi: ghi lại kẻ tấn công thử mật khẩu nào, gõ lệnh gì, tải gì về. Đây là mục tiêu của đề tài.

Honeypot là dạng deception phổ biến nhất: một máy hoặc dịch vụ giả, được theo dõi kỹ. Giá trị của nó nằm ở hai thứ: **mồi** (thứ làm kẻ tấn công tin là thật, mục 4) và **telemetry** (dữ liệu ghi được khi họ tương tác, mục 3). Mồi càng giống thật, kẻ tấn công càng ở lâu và telemetry càng nhiều; mồi lộ (mục 5) thì kẻ tấn công rời đi sớm hoặc cố tình cho dữ liệu giả.

## 2. Mức tương tác và đánh đổi

| Mức | Kẻ tấn công được làm gì | Ví dụ | Độ thật | Rủi ro | Công sức |
| --- | --- | --- | --- | --- | --- |
| Thấp | Thấy banner, thử đăng nhập; không bao giờ vào được | OpenCanary: SSH luôn từ chối (`docs/01_quyet_dinh_pham_vi_cong_cu.md`, mục 2) | Thấp | Thấp: không có shell | Ít |
| **Trung bình** | Đăng nhập được vào **shell giả lập**; lệnh do honeypot tự trả lời, không có hệ điều hành thật phía sau | **Cowrie `backend = shell`** (`cfg:124`) – nhóm đang dùng | Trung bình: lệnh phổ biến giống thật, lệnh lạ thì lộ | Trung bình: chỉ lỗi trong chính Cowrie mới chạm được máy thật | Vừa |
| Cao | Vào **hệ điều hành thật** (VM), honeypot đứng giữa ghi lại | Cowrie chế độ proxy (`[proxy]`, `cfg:364`, nhóm không bật) | Cao | Cao: kẻ tấn công điều khiển máy thật, phải cách ly rất chặt | Nhiều |

Đánh đổi: tăng độ thật thì thu được hành vi sâu hơn nhưng rủi ro bị dùng làm bàn đạp cũng tăng. Nhóm chọn mức trung bình vì đủ để quan sát lệnh (Q2, Q3) mà rủi ro vẫn kiểm soát được bằng cách ly mức VM (`docs/02_so_do_lab.md`, mục 6). Ngay cả ở mức này, Cowrie vẫn **tải file thật** khi gặp `wget`/`curl`, nên cách ly vẫn bắt buộc (`evidence/kiem_tra_cach_ly_TV1.md`).

## 3. Telemetry sinh ra từ đâu

Mỗi lớp tương tác sinh một nhóm sự kiện. Cowrie ghi mỗi sự kiện thành một dòng JSON, có chung `eventid`, `timestamp` (UTC), `session`, `src_ip`, `protocol`.

| Lớp tương tác | Kẻ tấn công làm gì | Sự kiện Cowrie | Trường chính | Ví dụ log thật |
| --- | --- | --- | --- | --- |
| Mạng | Mở kết nối TCP tới cổng 2222/2223 | `cowrie.session.connect` | `src_ip`, `src_port`, `dst_port`, `protocol` | `json:1` (SSH), `json:2` (Telnet) |
| Mạng | Đóng kết nối | `cowrie.session.closed` | `duration_ms` | `json:4` (16 ms – chỉ dò cổng), `json:21` (287 ms) |
| Giao thức SSH | Client gửi chuỗi phiên bản | `cowrie.client.version` | `version` | `json:7`; `json:3` có `version` rỗng vì chỉ mở cổng rồi đóng, không bắt tay SSH |
| Giao thức SSH | Thỏa thuận thuật toán | `cowrie.client.kex` | `hassh` (vân tay client) | `json:8`, `json:13`: cùng HASSH vì cùng một client OpenSSH 9.6p1 |
| Giao thức Telnet | Thỏa thuận tùy chọn Telnet | `cowrie.telnet.option` | – | `json:23` |
| Xác thực | Thử username/password | `cowrie.login.failed`, `cowrie.login.success` | `username`, `password` | `json:9` (sai), `json:14` (đúng) |
| Môi trường phiên | Mở terminal, gửi biến môi trường | `cowrie.client.size`, `cowrie.client.var`, `cowrie.session.params` | `name`, `arch` | `json:15`, `json:16`, `json:17` |
| Lệnh | Gõ lệnh trong shell giả | `cowrie.command.input` | `input` | `json:18` (`whoami`), `json:19` (`exit`) |
| Lệnh | Gõ lệnh shell giả không hỗ trợ | `cowrie.command.failed` | `input` | **Dự kiến**: chưa có trong log của repo; TV1 đã gặp khi gõ thêm ngoài smoke test (`docs/04_hop_dong_du_lieu.md`, mục 10 câu h). Kiểm ở KB-03 |
| Tệp | `wget`/`curl` tải file | `cowrie.session.file_download`, `...file_download.failed` | `url`, `shasum` | **Dự kiến**: TV1 thấy `file_download.failed` khi tự kiểm cách ly, log đó không thuộc smoke test. Kiểm ở KB-04 |
| Toàn phiên | Mọi thứ hiện trên màn hình | `cowrie.log.closed` + file TTY | `ttylog` | `json:20` → `evidence/smoke_test/tty/317e…b964` |

File TTY ghi lại cả **đầu ra** mà kẻ tấn công nhìn thấy, không chỉ lệnh gõ vào. TV3 đã giải mã file TTY ở trên (`python -I review/tai_hien/doc_tty.py <file TTY>`): có lời chào Debian, dấu nhắc `labuser@svr04:~$`, lệnh `whoami` trả `labuser`. Đây là nguồn chính để đối chiếu mồi và điểm lộ.

Ngoài `cowrie.json`, `cowrie.log` là log chẩn đoán dạng chữ: không dùng để đếm, nhưng giải thích được sự kiện lạ. Ví dụ `json:3` có `version` rỗng; `cowrie.log` cùng thời điểm ghi `Bad protocol version identification: b''`.

## 4. Yếu tố mồi trong cấu hình của nhóm

Nguồn: danh sách TV1 gửi (BG-08, `Implement/lab/cowrie/README.md`). TV3 đã kiểm lại: so `cowrie.cfg` với file mặc định `cowrie.cfg.dist` trong gói Cowrie 3.1.6 chính thức (tải bằng `pip download cowrie==3.1.6`) thì **chỉ khác 2 dòng**: `forwarding = false` (`cfg:813`) và Telnet `enabled = true` (`cfg:873`). Như vậy **mọi yếu tố mồi đều giữ giá trị mặc định**, trừ `userdb.txt`.

| Yếu tố mồi | Giá trị | Mặc định / Đã đổi | Căn cứ TV3 kiểm |
| --- | --- | --- | --- |
| Shell giả lập | `backend = shell` | Mặc định | `cfg:124` |
| Tên máy | `svr04` | Mặc định | `cfg:29`; TTY có `labuser@svr04:~$` |
| Banner SSH công bố | `SSH-2.0-OpenSSH_9.2p1 Debian-2+deb12u3` | Mặc định | `cfg:738` |
| `ssh -V` trong shell giả | `OpenSSH_7.9p1, OpenSSL 1.1.1a 20 Nov 2018` | Mặc định | `cfg:617` |
| Nhân hệ điều hành (`uname`) | `6.1.0-21-amd64`, Debian | Mặc định | `cfg:611` |
| Kiến trúc | `linux-x64-lsb` | Mặc định | `json:17` (`arch`) |
| Lời chào sau đăng nhập | Lời chào Debian GNU/Linux | Mặc định | TTY |
| Hệ thống file giả, nội dung file | `fs.pickle`, `honeyfs` đi kèm gói | Mặc định | Không ghi đè: `cfg:63` (`contents_path`) và `cfg:525` (`filesystem`) đều là dòng chú thích |
| Tài khoản chấp nhận | Chỉ `labuser` với mật khẩu giả; cặp khác bị từ chối | **Đã đổi** (bản tạm, chờ BG-01) | `json:9` bị từ chối, `json:14` được nhận |
| Cổng dịch vụ | SSH 2222, Telnet 2223 | Mặc định | `cfg` mục `[ssh]`, `[telnet]`; `json:1–2` |
| SFTP | Bật | Mặc định | `cfg:808`; chưa thử |

## 5. Điểm lộ (O7) – quan sát ban đầu

Điểm lộ là dấu hiệu giúp kẻ tấn công nhận ra đây là honeypot. Bảng đầy đủ từ RUN-01 sẽ nằm ở `results/RUN-xx/diem_lo.md`. Hiện chỉ có cấu hình, log smoke test và quan sát của TV1, nên bảng dưới ghi rõ mức căn cứ.

| # | Điểm lộ | Căn cứ | Mức căn cứ |
| --- | --- | --- | --- |
| L1 | Cấu hình trùng hoàn toàn bản mặc định công khai: ai đọc `cowrie.cfg.dist` trên GitHub cũng biết trước tên máy, banner, kernel | So khớp `cowrie.cfg` với gói 3.1.6 (mục 4) | Đã kiểm |
| L2 | Tên máy `svr04` là giá trị mặc định nổi tiếng của Cowrie | `cfg:29`, TTY | Đã kiểm |
| L3 | Hai phiên bản OpenSSH mâu thuẫn: banner 9.2p1 nhưng `ssh -V` trả 7.9p1 (bản năm 2018) | `cfg:738` và `cfg:617`; TV1 thấy cả hai khi chạy thử | Đã kiểm trên cấu hình; **dự kiến** ghi vào log ở KB-03 nếu thêm `ssh -V` |
| L4 | `wget` in "connected." rồi treo, máy thật báo lỗi ngay | TV1 quan sát (`evidence/kiem_tra_cach_ly_TV1.md`) | Quan sát của TV1, log không thuộc repo; **dự kiến** tái hiện |
| L5 | `curl -m 5` báo `option -m not recognized` dù tùy chọn này phổ biến | TV1 quan sát (như trên) | Như L4 |
| L6 | Cổng 2222/2223 thay vì 22/23 | `json:1–2` | Đã kiểm; là lựa chọn của lab (kế hoạch D.6), không phải lỗi mồi |
| L7 | Phản hồi khác máy thật với cùng danh sách lệnh KB-03 | So transcript KB-03 với kết quả trên VM-A | **Dự kiến**, chờ BG-07 |
| L8 | Lệnh không được hỗ trợ (`cowrie.command.failed`) | Đếm trong log RUN-01 | **Dự kiến**, chờ RUN-01 |

Giới hạn: lab chỉ có thành viên nhóm "tấn công", nên bảng này cho biết **điểm nào có thể lộ**, không đo được kẻ tấn công thật có nhận ra hay không.

**Đề xuất cải thiện mồi (hướng nâng cao, chưa làm):** đổi tên máy, cho `[shell] ssh_version` khớp với banner, đổi `kernel_version` cho cùng thời kỳ với banner. Mỗi thay đổi phải ghi vào bảng ở `Implement/lab/cowrie/README.md`, chụp snapshot mới và ghi `config_version` khác trong `run_note.txt` để không trộn dữ liệu trước và sau khi đổi.
