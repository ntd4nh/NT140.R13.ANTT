# Review ghi chú deception của TV3 (WP-13)

**Người review:** TV4, có AI hỗ trợ · **Ngày:** 2026-11-11 · **Sản phẩm:** `docs/00_nguyen_ly_deception_telemetry.md` tại nhánh `tv4` @ `9c75ec0` (cùng nội dung với `origin/main` @ `1d115d3`)
**Kết luận:** **Đạt có lưu ý.** Mọi trích dẫn `json:<dòng>` và `cfg:<dòng>` đúng loại sự kiện, đúng giá trị (1 trích dẫn lệch dòng nhỏ). Có 4 câu khẳng định rộng hơn căn cứ và 3 chỗ nên nói rõ mức căn cứ (mục 4). Không có lỗi mức chặn.

**Phạm vi:** đây là review **ghi chú và quan sát điểm lộ ban đầu**, không phải bảng điểm lộ O7 chính thức từ RUN (`results/RUN-xx/diem_lo.md` chưa có). TV4 chỉ kiểm trên tài liệu, log smoke test và cấu hình trong repo; **chưa** kiểm trên VM-H đang chạy. Phần cấu hình (mục 4 của ghi chú) vẫn chờ TV1 kiểm theo phân công.

## 1. Cách kiểm

Chạy trên máy host của TV4, gốc repo; nhật ký lệnh ở `evidence/van_hanh_TV4/2026-11-11.md`.

| Việc | Lệnh | Kết quả |
| --- | --- | --- |
| Đọc từng dòng log được trích, kèm các sự kiện cùng phiên | `python -I` in gọn 58 dòng `evidence/smoke_test/cowrie.json` (giờ, `session`, `src_ip`, `protocol`, `dst_port`, `eventid`, trường riêng) | Xem mục 2 |
| Kiểm dòng cấu hình được trích | `sed -n '<n>p' Implement/lab/cowrie/cowrie.cfg` cho dòng 29, 63, 124, 364, 525, 611, 617, 738, 808, 813, 873 | Xem mục 2, 3 |
| Giải mã TTY | `python -I review/tai_hien/doc_tty.py evidence/smoke_test/tty/317e…b964` | Lời chào "Debian GNU/Linux", dấu nhắc `labuser@svr04:~$`, `whoami` → `labuser` |
| Kiểm `cowrie.log` cho `json:3` | `grep -n "Bad protocol" evidence/smoke_test/cowrie.log` | Dòng 18, `2026-11-10T14:47:23.185254Z`: `Bad protocol version identification: b''` |
| **Tự đối chiếu bản cấu hình mặc định chính thức** | `git ls-remote --tags https://github.com/cowrie/cowrie.git` → tag `v3.1.6` = commit `ea9513eda9ea0dac05f6ace7db84ca95e0571501`; tải `https://raw.githubusercontent.com/cowrie/cowrie/v3.1.6/src/cowrie/data/etc/cowrie.cfg.dist` (SHA-256 `c9021cef…5e31`) và `…/v3.1.6/src/cowrie/data/etc/userdb.example`; `diff --strip-trailing-cr <cfg.dist> Implement/lab/cowrie/cowrie.cfg` | Chỉ khác **dòng 813** (`forwarding = true` → `false`) và **dòng 873** (`enabled = false` → `true`, mục `[telnet]`). Khớp kết luận của TV3. `userdb.example` có `*:x:*` ở cuối, khớp câu "mặc định chấp nhận gần như mọi cặp" |

TV3 so bằng gói `pip download cowrie==3.1.6`; TV4 so bằng mã nguồn ở tag `v3.1.6` trên GitHub. Hai cách độc lập cho cùng kết quả.

## 2. Kiểm từng trích dẫn telemetry (mục 3 của ghi chú)

| Dòng ghi chú | Trích dẫn | Log thật | Kết quả |
| --- | --- | --- | --- |
| 33 | `json:1` SSH, `json:2` Telnet | `json:1` `session.connect` `protocol=ssh` `dst_port=2222`; `json:2` `session.connect` `protocol=telnet` `dst_port=2223` (cùng `.10`) | ✅ |
| 34 | `json:4` 16 ms (chỉ dò cổng), `json:21` 287 ms | `json:4` `session.closed` `duration_ms=16` (phiên `3f8ff8b71f88` chỉ có 3 sự kiện); `json:21` `duration_ms=287` | ✅ |
| 35 | `json:7` có `version`; `json:3` `version` rỗng | `json:7` `SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13.20`; `json:3` `version=""`; `cowrie.log:18` `Bad protocol version identification: b''` | ✅ |
| 36 | `json:8`, `json:13` cùng HASSH | Cả hai `hassh=aae6b960…f657`, đi cùng `json:7`, `json:12` cùng chuỗi phiên bản client | ✅ (xem lưu ý V7) |
| 37 | `json:23` `telnet.option` | `json:23` `WONT NAWS` | ✅ |
| 38 | `json:9` sai, `json:14` đúng | `json:9` `login.failed` (`labuser`, mật khẩu giả sai); `json:14` `login.success` (`labuser`, `LabOnly-2026`) | ✅ |
| 39 | `json:15–17` môi trường phiên | `client.size` (`width=0, height=0`), `client.var` (`LANG`), `session.params` (`arch=linux-x64-lsb`) | ✅. `width/height = 0` có thể do client chạy bằng script; không phải điểm lộ |
| 40 | `json:18` `whoami`, `json:19` `exit` | Đúng, cùng phiên `17f75198febf` | ✅ |
| 41 | `command.failed`: dự kiến | Không có trong 58 dòng | ✅ ghi đúng là dự kiến |
| 42 | `file_download*`: dự kiến | Không có trong 58 dòng | ✅ ghi đúng là dự kiến |
| 43 | `json:20` → file TTY | `json:20` `log.closed`, `ttylog=var/lib/cowrie/tty/317e…b964`; file có trong `evidence/smoke_test/tty/`, giải mã được | ✅ |
| 47 | `cowrie.log` giải thích `json:3` | Như dòng 35 | ✅ |

Ghi thêm khi đọc cả phiên: 4 sự kiện `log.closed` (`json:20, 31, 46, 57`) trỏ cùng một file TTY, gồm cả 2 phiên Telnet. Điều này khớp giải thích của TV1 (TTY đặt tên theo hash nội dung).

## 3. Phân loại căn cứ của yếu tố mồi và L1–L8

Loại căn cứ: **CH** = cấu hình (TV4 đã đọc dòng cfg và so với bản mặc định 3.1.6) · **LOG** = sự kiện trong `cowrie.json` · **TTY** = file TTY giải mã · **QS** = người khác quan sát, chưa có log trong repo · **DK** = còn dự kiến.

| Mục | Khẳng định | Căn cứ TV4 xác nhận được | Loại | Ghi chú |
| --- | --- | --- | --- | --- |
| Mồi: shell, tên máy, banner, `ssh -V`, nhân | Giá trị mặc định | `cfg:124, 29, 738, 617, 611–614`; trùng `cowrie.cfg.dist` v3.1.6 | CH | Là cấu hình **trong repo**; chưa so với file đang chạy trên VM-H |
| Mồi: kiến trúc `linux-x64-lsb` | Mặc định | `json:17`; `cfg:542` | LOG + CH | |
| Mồi: lời chào Debian | Mặc định | TTY | TTY | |
| Mồi: hệ thống file giả | Mặc định | `cfg:63`, `cfg:525` là dòng chú thích | CH | |
| Mồi: tài khoản | Đã đổi | `json:9`, `json:14` | LOG | Chỉ 1 cặp sai đã thấy bị từ chối |
| Mồi: SFTP | Bật, chưa thử | `cfg:808` | CH | |
| **L1** Cấu hình trùng bản mặc định công khai | | diff với `cowrie.cfg.dist` tag `v3.1.6` | CH | Đúng; TV3 và TV4 kiểm độc lập |
| **L2** `svr04` là mặc định "nổi tiếng" | | `cfg:29`, TTY | CH + TTY | Phần "mặc định" đã kiểm; phần "nổi tiếng" chưa có nguồn (V5) |
| **L3** Banner 9.2p1 khác `ssh -V` 7.9p1 | | `cfg:738`, `cfg:617`; TV1 thấy cả hai | CH + QS | Phần log: DK (V6) |
| **L4** `wget` in "connected." rồi treo | | `evidence/kiem_tra_cach_ly_TV1.md` | QS | Log không có trong repo; phần "máy thật báo lỗi ngay" cần điều kiện (V4) |
| **L5** `curl -m` không được hỗ trợ | | Như L4 | QS | |
| **L6** Cổng 2222/2223 | | `json:1–2` | LOG | Đúng là lựa chọn của lab |
| **L7** Phản hồi khác máy thật | | – | DK | Chờ transcript KB-03 và bản chạy trên VM-A |
| **L8** Lệnh không được hỗ trợ | | – | DK | Chờ RUN có KB-03 |

## 4. Vấn đề

| # | Câu gốc | Vị trí | Căn cứ | Ảnh hưởng | Đề nghị sửa |
| --- | --- | --- | --- | --- | --- |
| V1 | "mọi tương tác với tài nguyên giả đều đáng ngờ" | `docs/00_nguyen_ly_deception_telemetry.md` dòng 9; lặp ở `report/TV3_review_deception.md` dòng 34 | Kế hoạch mục A dùng "đáng quan sát". Có tương tác không mang ý đồ: quét nghiên cứu, cấu hình nhầm, và trong lab là chính thành viên nhóm | Người nghe có thể hiểu mọi dữ liệu lab là hành vi độc hại | "Mọi tương tác đều **đáng quan sát** và thường đáng ngờ, vì không có lý do sử dụng hợp lệ; dữ liệu lab của nhóm là tương tác mô phỏng" |
| V2 | "Phát hiện với tỉ lệ báo động giả thấp … vì tài nguyên giả vốn không có lưu lượng tốt" | dòng 11; `report/TV3_…` dòng 36 | Đây là đặc tính thường được nêu của deception, không phải điều nhóm đo được. Honeypot đặt ngoài Internet nhận nhiều lưu lượng quét tự động | Dễ bị hỏi "đo bằng gì" | Ghi là **cơ chế/giả định thường nêu**, kèm điều kiện (tài nguyên không ai dùng hợp lệ); nói rõ nhóm không đo tỉ lệ báo động giả |
| V3 | "Mồi càng giống thật, kẻ tấn công càng ở lâu và telemetry càng nhiều; mồi lộ thì kẻ tấn công rời đi sớm hoặc cố tình cho dữ liệu giả" | dòng 15 (và câu "làm chậm kẻ tấn công" dòng 12) | Là **giả thuyết**. Dữ liệu lab do thành viên nhóm tạo theo kịch bản, không kiểm chứng được thời gian ở lại hay ý định của kẻ tấn công | Trộn giả thuyết với kết quả | Thêm chữ "giả thuyết" và câu "lab của nhóm không kiểm chứng được điều này"; tách khỏi phần kết quả |
| V4 | "`wget` in 'connected.' rồi treo, máy thật báo lỗi ngay" | L4, dòng 76 | Theo bảng của TV1: với `wget http://example.com` shell giả báo lỗi phân giải tên; chỉ với URL là **địa chỉ IP** mới in "connected." rồi treo. "Báo lỗi ngay" đúng khi máy không có tuyến (như VM-H), không đúng khi tường lửa chỉ thả gói | So sánh thiếu điều kiện | Ghi rõ "với URL dạng IP, trên máy không có tuyến ra ngoài"; giữ mức QS cho tới khi tái hiện bằng log |
| V5 | "`svr04` là giá trị mặc định nổi tiếng của Cowrie" | L2, dòng 74 (và `Implement/lab/cowrie/README.md` mục điểm lộ 5: "công cụ dò honeypot thường kiểm tra tên này") | Phần "mặc định" đã kiểm (`cfg:29`, `cowrie.cfg.dist`). Phần "nổi tiếng", "công cụ dò thường kiểm tra" chưa có nguồn trong repo | Khẳng định không có trích dẫn | Bỏ chữ "nổi tiếng", hoặc thêm nguồn cụ thể |
| V6 | L3 "**dự kiến** ghi vào log ở KB-03 nếu thêm `ssh -V`" | dòng 75 | `cowrie.json` chỉ ghi **lệnh gõ vào** (`command.input`), không ghi đầu ra. Chuỗi 7.9p1 sẽ nằm ở file TTY/transcript KB-03; banner 9.2p1 nằm ở transcript phía client (`ssh -v`, KB-01), không nằm trong `cowrie.json` | Có thể đi tìm sai chỗ khi lập O7 | Sửa căn cứ dự kiến thành "transcript KB-01 (`ssh -v`) + TTY/transcript KB-03"; `docs/03_kich_ban_thu_nghiem.md` đã thêm `-v` ở KB-01 và `ssh -V` ở KB-03 |
| V7 | "Rủi ro trung bình: chỉ lỗi trong chính Cowrie mới chạm được máy thật" | bảng mục 2, dòng 22 | Chính ghi chú (dòng 25) và `evidence/kiem_tra_cach_ly_TV1.md` cho thấy Cowrie **tải tệp thật** khi gặp `wget`/`curl`; `forwarding` mặc định là `true` (`cowrie.cfg.dist` dòng 813) | Mâu thuẫn trong cùng file | "Rủi ro: lỗi trong Cowrie; tính năng tải tệp thật; chuyển tiếp cổng (mặc định bật, lab đã tắt)" |
| V8 | "rủi ro vẫn kiểm soát được bằng cách ly mức VM" | dòng 25 | Căn cứ hiện có là tự kiểm của TV1; biên bản cách ly độc lập của TV3 chưa chạy (`review/kiem_tra_cach_ly.md`) | Nâng mức căn cứ | Thêm "theo tự kiểm của TV1; kiểm độc lập: dự kiến" |
| V9 | "`[proxy]`, `cfg:364`" | dòng 23 | Tiêu đề `[proxy]` ở `cfg:359`; dòng 364 là `backend = pool` | Thấp | Sửa thành `cfg:359` |

Lưu ý nhỏ, không bắt buộc sửa: dòng 36 "cùng HASSH vì cùng một client" nên ghi "cùng HASSH và cùng chuỗi phiên bản client (`json:7`, `json:12`), cùng nguồn `.10`", vì HASSH giống nhau không tự chứng minh là cùng một máy.

## 5. Kết luận

- **Đạt có lưu ý**, trong phạm vi: trích dẫn log smoke test, trích dẫn cấu hình trong repo, so cấu hình với bản mặc định chính thức v3.1.6, giải mã TTY.
- **Chưa kiểm:** cấu hình đang chạy trên VM-H có trùng file trong repo không; L3–L5, L7, L8 trên log thật; mức tương tác của OpenCanary (ghi chú dựa vào `docs/01_quyet_dinh_pham_vi_cong_cu.md` của TV1).
- Các vấn đề V1–V9 do TV3 quyết định sửa. TV4 không sửa `docs/00_nguyen_ly_deception_telemetry.md`. Khi ghép báo cáo tiến độ, TV4 dùng cách diễn đạt ở cột "Đề nghị sửa" cho các câu V1–V3 và ghi rõ nguồn.
