# Kịch bản thử nghiệm (WP-04)

**Người viết:** TV4 (có AI hỗ trợ) · **Ngày:** 2026-11-11 · **Trạng thái:** bản đề xuất, chờ TV3 review; TV1 chưa xác nhận tính khả thi với cấu hình (kế hoạch E.4, WP-04)

File này chỉ ghi **mong đợi**. Kết quả thực tế của từng lượt chạy ghi ở bảng đối chiếu `experiments/doi_chieu_<RUN>.csv`, không sửa ngược vào đây.

**Căn cứ tên sự kiện:** sự kiện đã thấy trong log thật `evidence/smoke_test/cowrie.json` được trích `json:<dòng>`. `cowrie.command.failed` và `cowrie.session.file_download*` **chưa có** trong log của repo; tên lấy theo tài liệu Cowrie (`docs/01_quyet_dinh_pham_vi_cong_cu.md` mục 3.1) và quan sát của TV1 (`docs/04_hop_dong_du_lieu.md` mục 10 câu h; `evidence/kiem_tra_cach_ly_TV1.md`), đánh dấu **[XM]**.

Cách ghi nhật ký (dòng bắt đầu/kết thúc, định dạng giờ, khoảng nghỉ): `experiments/quy_uoc_nhat_ky.md`.

---

## 0. Quy ước chung

### 0.1. Máy trong lab

| Ký hiệu | Vai trò | IP | Công cụ phía client (theo `evidence/smoke_test/README.md`) |
| --- | --- | --- | --- |
| VM-A | Nguồn 1 | `192.168.239.10` | OpenSSH 9.6p1, `sshpass`, `script`, `python3` |
| Host | Nguồn 2 (máy Windows chạy lab) | `192.168.239.1` | OpenSSH của Git for Windows, Python có `telnetlib` (≤ 3.12) |
| VM-H | Honeypot | `192.168.239.20` | Cowrie 3.1.6: SSH giả `2222`, Telnet giả `2223` |

### 0.2. Tài khoản giả (nội dung bàn giao BG-01)

**Mọi mật khẩu dưới đây là mật khẩu giả của lab**, chỉ dùng trên honeypot, không phải mật khẩu của thành viên nào.

`etc/userdb.txt` giữ nguyên bản tạm hiện có, **đúng một dòng**:

```text
labuser:x:LabOnly-2026
```

| Kịch bản | Kết nối | Username | Mật khẩu gửi lần lượt | Mong đợi |
| --- | --- | --- | --- | --- |
| KB-02 | Kết nối 1 | `labuser` | `LabWrong-01`, `LabWrong-02`, `LabWrong-03` | 3 lần thất bại, client tự ngắt |
| KB-02 | Kết nối 2 | `labuser` | `LabWrong-04`, `LabWrong-05`, `LabOnly-2026` | 2 lần thất bại, 1 lần thành công, rồi `exit` |
| KB-03 | 1 kết nối | `labuser` | `LabOnly-2026` | 1 lần thành công |
| KB-05 | 1 kết nối Telnet | `labuser` | `TelnetWrong-01`, `TelnetWrong-02`, `LabOnly-2026` | 2 lần thất bại, 1 lần thành công |

Việc các cặp sai bị từ chối và cặp đúng được nhận **phải kiểm trên VM-H** ở phiên chuẩn bị (mục 0.5), không suy ra chỉ từ tài liệu. Smoke test mới cho thấy một cặp sai (`json:9`) bị từ chối và cặp đúng (`json:14`) được nhận.

### 0.3. Đơn vị đếm

- **Sự kiện:** một dòng trong `cowrie.json`.
- **Lần đăng nhập:** một sự kiện `cowrie.login.failed` hoặc `cowrie.login.success`.
- **Phiên:** một giá trị `session` (một kết nối TCP).

Không cộng các đơn vị khác nhau với nhau.

### 0.4. Thứ tự trong một lượt chạy (RUN)

```text
KB-01 (VM-A, SSH) → KB-02 (VM-A, SSH) → KB-03 (VM-A, SSH) → KB-05 (Host, Telnet) → KB-01 lặp lại (Host, SSH)
```

- Giữa hai kịch bản liên tiếp **cùng nguồn, cùng cổng** nghỉ ít nhất `max(10 s, 2×|δ| + 2 s)`, δ là độ lệch giờ đo trước lượt (`experiments/quy_uoc_nhat_ky.md`, mục 4).
- Lượt chạy không được vắt qua 00:00 UTC (Cowrie xoay log lúc đó).
- Đối chứng KB-03 trên VM-A thật chạy sau lượt, **không** ghi vào nhật ký H.2 (không phải tương tác với honeypot).
- Một kịch bản chạy sai (sai số lần thử, sai nguồn, gõ nhầm): dừng lượt, vẫn xuất RUN đó và ghi "lượt chưa đạt"; chạy lại toàn bộ trong một RUN mới. Không chạy lại một kịch bản bên trong cùng RUN.

Tổng mong đợi của một RUN cơ bản (chưa tính KB-04): **6 phiên**; **7** `login.failed`, **3** `login.success` (10 lần đăng nhập); **15** `command.input` (KB-02: 1, KB-03: 11, KB-05: 3).

### 0.5. Tiền điều kiện chung

1. Phép kiểm cách ly trước lượt đạt (bản của TV4: `evidence/kiem_tra_cach_ly_TV4/`). Bản này **không thay** biên bản độc lập của TV3 (`review/kiem_tra_cach_ly.md`, BG-04).
2. Cowrie nghe cổng 2222, 2223; `userdb.txt` đúng một dòng ở mục 0.2; hash `cowrie.cfg` và `userdb.txt` ghi vào `run_note.txt` (`config_version`).
3. **Phiên chuẩn bị** (trước khi xoay log, không thuộc RUN): chạy thử từng script, xác nhận cặp sai bị từ chối, cặp đúng vào được, số lần thử trong log khớp thiết kế, KB-01 không sinh sự kiện đăng nhập, Telnet cho thử 3 lần trong một kết nối.
4. Đo lệch giờ trước và sau lượt: `experiments/<RUN>/do_lech_gio.md`.
5. Xoay log có kiểm soát để thư mục log chỉ chứa sự kiện của lượt.

### 0.6. Minh chứng chung của một RUN

| Minh chứng | Vị trí |
| --- | --- |
| Nhật ký thử nghiệm (H.2) | `experiments/nhat_ky_thu_nghiem.csv` |
| Transcript phía client (stdout + stderr) | `experiments/transcript/<RUN>/` kèm `README.md` |
| Log gốc + hash + ghi chú lượt | `data/raw/<RUN>/` (`cowrie.json*`, `tty/`, `SHA256SUMS`, `run_note.txt`) |
| Bảng đối chiếu bước ↔ sự kiện | `experiments/doi_chieu_<RUN>.csv` |
| Đo lệch giờ | `experiments/<RUN>/do_lech_gio.md` |

### 0.7. Thế nào là thu thập thành công

Theo kế hoạch H.1: mọi bước trong nhật ký tìm được sự kiện khớp về nguồn, cổng, phiên và thời điểm (trong độ lệch giờ đã đo), **hoặc** giải thích được vì sao không có sự kiện riêng; log gốc nguyên vẹn (hash khớp). **Thu thập thành công không có nghĩa là "tấn công thành công".** Một lần đăng nhập thất bại được ghi đủ cũng là thu thập thành công.

Trường đối chiếu chung: `src_ip`, `dst_port`, `protocol`, `session`, `timestamp`. Trạng thái mỗi dòng đối chiếu: `khop`, `khong_co_su_kien_rieng`, `khong_khop`, `mo_ho`.

---

## KB-01 – Kết nối rồi ngắt, không đăng nhập

- **Mục tiêu:** xem Cowrie ghi gì khi chỉ có kết nối và bắt tay SSH, không có lần đăng nhập nào (Q1).
- **Nguồn → đích:** VM-A (`.10`) → VM-H `2222`. **Lặp lại** từ Host (`.1`) → VM-H `2222` ở cuối lượt; `scenario_id` vẫn là `KB-01`, phân biệt bằng `ip_nguon`.
- **Tiền điều kiện:** mục 0.5.
- **Lệnh** (tham số giống nhau ở hai nguồn):

  ```bash
  ssh -v -p 2222 -o PubkeyAuthentication=no -o PreferredAuthentications=password \
      -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null labuser@192.168.239.20
  ```

  `-v` để transcript có dòng `remote software version` (banner server). Hai tùy chọn host key để không phải trả lời `yes/no` và không sửa `known_hosts`; chỉ dùng trong lab. Trên Host chạy bằng OpenSSH của Git for Windows như smoke test; nếu dùng OpenSSH của Windows thì kiểm lại `UserKnownHostsFile=/dev/null` ở phiên chuẩn bị **[XM]**.

| Bước | Thao tác | Sự kiện mong đợi | Kiểm bằng |
| --- | --- | --- | --- |
| 0 | Dòng nhật ký **bắt đầu**, trước khi mở kết nối | Không có | Nhật ký |
| 1 | Chạy lệnh trên, chờ tới dấu nhắc `labuser@192.168.239.20's password:` | `cowrie.session.connect` (`protocol=ssh`, `src_ip` của nguồn, `dst_port=2222`; như `json:6`); `cowrie.client.version` (`version` là chuỗi client; như `json:7`); `cowrie.client.kex` (`hassh`; như `json:8`) | Log; transcript có `remote software version OpenSSH_9.2p1 Debian-2+deb12u3` (mong đợi theo `cowrie.cfg:738`) |
| 2 | **Hủy** ở dấu nhắc mật khẩu: đóng client, không gõ gì, không Enter | Không có sự kiện riêng. `cowrie.session.closed` có `duration_ms` (như `json:10`) | Phiên **không có** `cowrie.login.*`; transcript dừng ở dấu nhắc |
| 3 | Dòng nhật ký **kết thúc**, sau khi client đã thoát | Không có | Nhật ký |

- **Trường đối chiếu:** chung + `version`, `hassh`, `duration_ms`.
- **Đơn vị đếm:** mỗi nguồn 1 phiên, 0 lần đăng nhập.
- **Minh chứng:** `KB-01_VM-A.txt`, `KB-01_Host.txt` trong `experiments/transcript/<RUN>/`; dòng nhật ký; đoạn log của 2 phiên.
- **Đạt:** mỗi nguồn có đúng 1 phiên mới trong cửa sổ nhật ký, đủ connect, version, kex, closed; không có sự kiện đăng nhập.
- **Không đạt:** có `cowrie.login.failed` trong phiên (nhất là `password` rỗng: cách hủy đã làm client gửi credential); không có phiên; phiên mang IP hoặc cổng khác.
- **Rủi ro đã biết:** nếu tự động hóa bằng `SSH_ASKPASS` mà chương trình askpass thoát lỗi, OpenSSH có thể gửi mật khẩu rỗng. Script phải dừng client khi đang chờ mật khẩu, không để askpass trả về; phiên chuẩn bị phải xác nhận không có `login.failed`.

## KB-02 – Đăng nhập sai lặp lại rồi đúng

- **Mục tiêu:** xem Cowrie ghi từng lần thử mật khẩu ra sao, trong nhiều kết nối (Q1, Q3).
- **Nguồn → đích:** VM-A → VM-H `2222`. Hai kết nối, **một** cặp dòng bắt đầu/kết thúc bao cả hai.
- **Tiền điều kiện:** mục 0.5; phiên chuẩn bị đã xác nhận ba cặp sai đầu và cặp đúng hoạt động như bảng 0.2.
- **Lệnh** (mỗi kết nối):

  ```bash
  ssh -p 2222 -o PubkeyAuthentication=no -o PreferredAuthentications=password \
      -o NumberOfPasswordPrompts=3 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
      labuser@192.168.239.20
  ```

  `sshpass` chỉ gửi một mật khẩu cố định, nên script dùng `pty` (hoặc `SSH_ASKPASS` + `SSH_ASKPASS_REQUIRE=force`) để trả lần lượt các mật khẩu ở bảng 0.2.

| Bước | Thao tác | Sự kiện mong đợi | Kiểm bằng |
| --- | --- | --- | --- |
| 0 | Dòng **bắt đầu** | Không có | Nhật ký |
| 1 | Mở kết nối 1 | `session.connect`, `client.version`, `client.kex` (phiên A) | Log |
| 2–4 | Gửi `LabWrong-01`, `LabWrong-02`, `LabWrong-03` | Mỗi lần một `cowrie.login.failed` (`username=labuser`, `password` đúng chuỗi đã gửi; như `json:9`) | Log; transcript có `Permission denied, please try again.` |
| 5 | Client tự ngắt sau 3 lần sai | Không có sự kiện riêng; `cowrie.session.closed` của phiên A | Transcript có `Permission denied (…)`; phiên A đóng |
| 6 | Mở kết nối 2 | `session.connect`, `client.version`, `client.kex` (phiên B, `session` khác phiên A) | Log |
| 7–8 | Gửi `LabWrong-04`, `LabWrong-05` | 2 `cowrie.login.failed` | Log, transcript |
| 9 | Gửi `LabOnly-2026` | `cowrie.login.success` (như `json:14`). Có thể kèm sự kiện phụ `cowrie.client.size`, `cowrie.client.var`, `cowrie.session.params` (như `json:15–17`) | Log; transcript có dấu nhắc `labuser@svr04:~$` |
| 10 | Gõ `exit` | `cowrie.command.input` (`input=exit`; như `json:19`), `cowrie.log.closed`, `cowrie.session.closed` | Log |
| 11 | Dòng **kết thúc** | Không có | Nhật ký |

- **Trường đối chiếu:** chung + `username`, `password`, thứ tự lần thử, `session` của từng kết nối.
- **Đơn vị đếm:** 2 phiên; 6 lần đăng nhập (5 thất bại, 1 thành công); 1 lệnh.
- **Minh chứng:** `KB-02_VM-A.txt`; danh sách credential ở bảng 0.2; nội dung `userdb.txt` (chỉ chứa mật khẩu giả).
- **Đạt:** đếm trên **log thật** (không đếm theo số lần gọi client): đúng 5 `login.failed` và 1 `login.success` trong đúng 2 phiên, đúng thứ tự mật khẩu.
- **Không đạt:** một mật khẩu "sai" lại thành công (kiểm lại `userdb.txt`); số lần thử khác thiết kế; nhiều hơn 2 phiên.

## KB-03 – Chuỗi lệnh khám phá trong phiên

- **Mục tiêu:** xem lệnh và phản hồi của shell giả được ghi ra sao, dựng lại thứ tự; tìm điểm lộ bằng cách so với máy thật (Q1, Q2, O7).
- **Nguồn → đích:** VM-A → VM-H `2222`, kết nối riêng, đăng nhập `labuser` / `LabOnly-2026`.
- **Tiền điều kiện:** mục 0.5.

| Bước | Lệnh gõ | Sự kiện mong đợi | Kiểm bằng |
| --- | --- | --- | --- |
| 0 | Dòng **bắt đầu** | Không có | Nhật ký |
| 1 | Mở kết nối (lệnh như KB-02, không có `NumberOfPasswordPrompts`) | `session.connect`, `client.version`, `client.kex` | Log |
| 2 | Gửi `LabOnly-2026` | `cowrie.login.success` (+ sự kiện phụ như KB-02 bước 9) | Log; transcript có dấu nhắc shell |
| 3 | `whoami` | `cowrie.command.input` | Log; transcript |
| 4 | `id` | `cowrie.command.input` | Log; transcript |
| 5 | `uname -a` | `cowrie.command.input` | Log; transcript (mong đợi theo cấu hình: nhân `6.1.0-21-amd64`, Debian) |
| 6 | `pwd` | `cowrie.command.input` | Log; transcript |
| 7 | `ls -la` | `cowrie.command.input` | Log; transcript |
| 8 | `cat /etc/passwd` | `cowrie.command.input` | Log; transcript |
| 9 | `ps aux` | `cowrie.command.input` | Log; transcript |
| 10 | `ifconfig` | `cowrie.command.input` | Log; transcript |
| 11 | `ssh -V` (gõ **bên trong** shell Cowrie) | `cowrie.command.input` | Log; transcript giữ cả stdout và stderr (mong đợi theo `cowrie.cfg:617`: `OpenSSH_7.9p1`) |
| 12 | `nt140_cmd_khong_ton_tai` | `cowrie.command.input`; `cowrie.command.failed` **[XM]** (TV1 thấy cặp này khi gõ thêm ngoài smoke test) | Log; transcript |
| 13 | `exit` | `cowrie.command.input`, `cowrie.log.closed` (trường `ttylog`), `cowrie.session.closed` | Log; file TTY giải mã được bằng `review/tai_hien/doc_tty.py` |
| 14 | Dòng **kết thúc** | Không có | Nhật ký |

- `cowrie.command.failed` chỉ ghi nhận khi **thực sự** xuất hiện. Không có `command.failed` **không** có nghĩa là lệnh chạy thật hay được hỗ trợ đầy đủ (`docs/04_hop_dong_du_lieu.md` mục 5).
- **Trường đối chiếu:** chung + `input` (nội dung, thứ tự), khoảng cách thời gian giữa lệnh, `ttylog`, `duration_ms`.
- **Đơn vị đếm:** 1 phiên; 1 lần đăng nhập; 11 lệnh (`command.input`).
- **Đối chứng trên VM-A thật** (không ghi vào nhật ký H.2): cùng 11 lệnh, cùng thứ tự, chạy trong `script` với `bash --noprofile --norc` riêng để `exit` chỉ đóng subshell. Giữ nguyên kết quả thật, kể cả lỗi (ví dụ VM-A không có `ifconfig` thì đó chính là kết quả).
- **Minh chứng:** `KB-03_honeypot.txt`, `KB-03_VM-A_that.txt` và `README.md` ghi rõ file nào là honeypot, file nào là máy thật, hệ điều hành, shell, user, giờ.
- **Đạt:** 11 `command.input` đúng nội dung và thứ tự trong 1 phiên; có `log.closed` và `session.closed`; có đủ hai transcript.
- **Không đạt:** thiếu hoặc sai thứ tự lệnh trong log; lệnh rơi vào phiên khác; thiếu một trong hai transcript.

## KB-05 – Telnet từ nguồn thứ hai

- **Mục tiêu:** so tập sự kiện Telnet với SSH; có dữ liệu từ hai nguồn và hai dịch vụ (Q1, Q2, O6).
- **Nguồn → đích:** Host (`.1`) → VM-H `2223`.
- **Tiền điều kiện:** mục 0.5; phiên chuẩn bị đã xác nhận Cowrie Telnet cho thử **3 lần trong một kết nối** **[XM]** (smoke test mới thấy 2 lần: `json:25–26`). Nếu không được, ghi lại và điều chỉnh kịch bản **trước** RUN.

| Bước | Thao tác | Sự kiện mong đợi | Kiểm bằng |
| --- | --- | --- | --- |
| 0 | Dòng **bắt đầu** | Không có | Nhật ký |
| 1 | Mở Telnet tới `192.168.239.20:2223` | `cowrie.session.connect` (`protocol=telnet`, `src_ip=192.168.239.1`, `dst_port=2223`; như `json:48`); sự kiện phụ `cowrie.telnet.option` (như `json:49–50`) | Log; transcript có `login:` |
| 2 | Gửi `labuser` ở `login:` | Không có sự kiện riêng; username nằm trong sự kiện đăng nhập kế tiếp | Transcript có `Password:` |
| 3 | Gửi `TelnetWrong-01` | `cowrie.login.failed` | Log; transcript có `Login incorrect` |
| 4 | Gửi `labuser` | Không có sự kiện riêng | Như bước 2 |
| 5 | Gửi `TelnetWrong-02` | `cowrie.login.failed` | Như bước 3 |
| 6 | Gửi `labuser` | Không có sự kiện riêng | Như bước 2 |
| 7 | Gửi `LabOnly-2026` | `cowrie.login.success` (như `json:52`), sự kiện phụ `cowrie.session.params` | Log; transcript có dấu nhắc shell |
| 8 | `whoami` | `cowrie.command.input` | Log; transcript |
| 9 | `uname -a` | `cowrie.command.input` | Log; transcript |
| 10 | `exit` | `cowrie.command.input`, `cowrie.log.closed`, `cowrie.session.closed` | Log |
| 11 | Dòng **kết thúc** | Không có | Nhật ký |

- Phiên Telnet **không có** `cowrie.client.version`, `cowrie.client.kex` (`docs/04_hop_dong_du_lieu.md` mục 10 câu b); thiếu hai sự kiện này là bình thường.
- **Trường đối chiếu:** chung + `username`, `password`, `input`.
- **Đơn vị đếm:** 1 phiên; 3 lần đăng nhập (2 thất bại, 1 thành công); 3 lệnh.
- **Minh chứng:** `KB-05_Host.txt` (byte nhận được đã giải mã, bỏ byte điều khiển Telnet nhưng ghi rõ đã bỏ).
- **Đạt:** 1 phiên Telnet từ `.1` có đúng 2 `login.failed`, 1 `login.success`, 3 `command.input` đúng thứ tự.
- **Không đạt:** Cowrie ngắt kết nối trước lần thử thứ 3; số lần thử hoặc số lệnh khác thiết kế.

## KB-04 – Tải tệp vô hại từ máy trong lab (nâng cao, lượt riêng)

Chỉ làm ở **lượt riêng** (`RUN-xx+1`) khi lượt cơ bản xong, có quyền sudo trên VM-H và chứng minh được ngoại lệ firewall vẫn giữ cách ly. Thiếu một điều kiện: ghi "dự kiến", không làm.

- **Nguồn → đích:** VM-A → VM-H `2222` (đăng nhập `labuser`); từ shell giả, VM-H tải tệp từ `http://192.168.239.10:8000/`.
- **Chuẩn bị:** snapshot VM-H `truoc-KB04-TV4`; trên VM-A tạo `/tmp/kb04/nt140_kb04.txt` (văn bản vô hại), tính `sha256sum`; chạy `python3 -m http.server 8000 --bind 192.168.239.10 --directory /tmp/kb04` và ghi access log; trên VM-H thêm **đúng một** luật `ufw allow out to 192.168.239.10 port 8000 proto tcp`, kiểm `ufw status numbered`, chạy lại phép thử ra Internet (vẫn phải thất bại).
- **Thao tác:** trong shell Cowrie gõ `wget http://192.168.239.10:8000/nt140_kb04.txt`, rồi `exit`.
- **Sự kiện mong đợi:** `cowrie.command.input` (`input` là lệnh `wget`); `cowrie.session.file_download` với `url`, `shasum`, `outfile` **[XM]**, hoặc `cowrie.session.file_download.failed` **[XM]**. Tải thất bại cũng là kết quả, ghi đúng như vậy.
- **Đối chiếu:** `url`; `shasum` so với SHA-256 tính trước; tệp trong `var/lib/cowrie/downloads/`; dòng access log của `http.server`. Không lấy hash của file TTY làm hash tệp tải.
- **Dọn dẹp:** xóa luật ufw vừa thêm và xác nhận đã gỡ; tắt `http.server`; chạy lại phép kiểm cách ly.
- **Đơn vị đếm:** 1 phiên; 1 lần đăng nhập; 2 lệnh; 0 hoặc 1 sự kiện tải tệp.
