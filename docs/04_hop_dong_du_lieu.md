# Hợp đồng dữ liệu A → B (TV1 → TV2)

**Trạng thái:** BẢN CHỐT ĐỀ XUẤT – đã đối chiếu log smoke test; chờ TV3 review (BG-05 chưa gửi)
**Người soạn:** TV2  
**Ngày:** 2026-11-10

Quy ước: `[XM]` chỉ phần chưa xác minh được trên log smoke test. Hiện còn `[XM]` cho tên file Cowrie sau xoay vòng (smoke test chỉ có `cowrie.json`) và trường `url` của `cowrie.session.file_download.failed` (event này không có trong smoke test). Các trường đã quan sát đều ghi căn cứ câu hỏi hoặc file:dòng.

## 1. Phạm vi và nguyên tắc

- TV1 bàn giao log gốc theo từng lượt; TV2 không sửa `data/raw/`. Luồng dữ liệu là `raw` → `processed` → `results`.
- Trước xử lý, kiểm tra `SHA256SUMS`. Mặc định ghi `events.csv`, `sessions.csv` và `bao_cao_chat_luong.txt` vào `data/processed/RUN-xx/`; chỉ bảng/biểu đồ O1–O7 vào `results/RUN-xx/`. Có thể đổi riêng thư mục báo cáo chất lượng bằng tùy chọn `--out-results`.
- Mọi thời gian lưu trong các file phân tích dùng UTC. Nhật ký thử nghiệm cũng ghi UTC.
- Ba đơn vị đếm theo H.4:
  - **Sự kiện:** một dòng log.
  - **Lần đăng nhập:** một sự kiện đăng nhập thành công hoặc thất bại.
  - **Phiên:** một định danh phiên, tương ứng một kết nối. Một phiên có thể có nhiều sự kiện, lần đăng nhập và lệnh.

## 2. Nơi chuyển và cấu trúc lượt chạy

TV1 sao chép mỗi lượt thử vào `data/raw/RUN-xx/`; giữ nguyên log JSON gốc và kèm thư mục TTY nếu có KB-03. `RUN-xx` dùng tiền tố `RUN-` và số thứ tự hai chữ số tăng dần (`RUN-01`, `RUN-02`, ...), không tái sử dụng một mã cho lượt khác.

```text
data/raw/RUN-xx/
├── cowrie.json*
├── tty/                  # nếu có bản ghi TTY
├── SHA256SUMS
└── run_note.txt
```

`SHA256SUMS` chứa một dòng theo định dạng chuẩn `sha256sum`: hash, hai khoảng trắng, đường dẫn tương đối bắt đầu `./`. Trong Git Bash, tại thư mục lượt chạy, tạo và kiểm tra manifest đúng như README lab, Bước 15.3:

```bash
cd data/raw/RUN-xx
find . -type f ! -name SHA256SUMS -exec sha256sum {} + > SHA256SUMS
sha256sum -c SHA256SUMS
```

`run_note.txt` là một dòng ghi đủ: thời điểm bắt đầu và kết thúc UTC, độ lệch đồng hồ đo (δ), phiên bản Cowrie và mã/phiên bản cấu hình đã dùng; không ghi bí mật. TV1 đã đồng ý định dạng một dòng này và sẽ ghi cho RUN-01:

```text
start_utc=<ISO-8601 UTC>; end_utc=<ISO-8601 UTC>; clock_offset_s=<δ giây, số thực có dấu: giờ VM-A trừ giờ VM-H>; cowrie_version=<version>; config_version=<revision>
```

Log smoke test thật để xác minh schema được đặt trong `evidence/smoke_test/`, kèm phiên bản Cowrie và cách cài; không trộn với log lượt chạy trong `data/raw/RUN-xx/`.

## 3. Log xoay vòng

TV2 đọc mọi file khớp `cowrie.json*` trong thư mục lượt chạy, không chỉ file có tên chính xác `cowrie.json`. Tên file sau khi Cowrie xoay vòng là `[XM]`: smoke test không chạy qua nửa đêm UTC nên chưa quan sát được tên này (câu f). TV1 bố trí lượt thử không chạy qua nửa đêm UTC; nếu không tránh được, vẫn bàn giao và giữ nguyên tất cả file khớp mẫu.

## 4. Từ điển dữ liệu

### `events.csv`

Mỗi dòng tương ứng một sự kiện thuộc một trong hai lớp được giữ lại ở bảng phân loại dưới đây; trường không có trong sự kiện được để rỗng, không tự điền giá trị suy đoán. Bộ xử lý phân loại theo bảng eventid nhưng không xuất cột phân loại riêng. Bảng dưới gồm **24 trường H.3** và ba cột kỹ thuật (`protocol_inferred`, `duration_computed`, `duplicate_count`).

| Tên trường | Ý nghĩa | Nguồn (trường Cowrie) | Loại | Bắt buộc | Xử lý khi thiếu | Trạng thái xác minh |
|---|---|---|---|---|---|---|
| `event_time_utc` | Thời điểm sự kiện UTC | `timestamp` | Công cụ cấp | Có | Không parse được: loại khỏi dữ liệu chuẩn hóa, ghi file:dòng và báo cáo chất lượng | Xác minh smoke test, câu j; `cowrie.json:1` |
| `event_type` | Loại sự kiện | `eventid` | Công cụ cấp | Có | Thiếu thì loại khỏi dữ liệu chuẩn hóa; ghi file:dòng và báo lỗi | `cowrie.json:1–58` |
| `session_id` | Định danh phiên | `session` | Công cụ cấp | Có với sự kiện thuộc phiên | Để rỗng, không ghép phiên, đánh dấu review | `cowrie.json:1–58` |
| `src_ip` | IP nguồn | `src_ip` | Công cụ cấp | Có | Để rỗng; báo trường thiếu | `cowrie.json:1–58` |
| `src_port` | Cổng nguồn | `src_port` | Công cụ cấp | Không | Để rỗng | `cowrie.json:1–58` |
| `dst_ip` | IP đích | `dst_ip` | Công cụ cấp | Không | Để rỗng | Xác minh smoke test, câu c; `cowrie.json:1–58` |
| `dst_port` | Cổng đích | `dst_port` | Công cụ cấp | Không | Để rỗng | Xác minh smoke test, câu c; `cowrie.json:1–58` |
| `protocol` | Giao thức (`ssh`/`telnet`) | `protocol` ở các sự kiện, không chỉ connect | Công cụ cấp; dự phòng suy ra khi thiếu | Không | Lấy trực tiếp; chỉ dùng cổng dự phòng nếu thiếu, bật `protocol_inferred` | Xác minh smoke test, câu a/c; `cowrie.json:1–58` |
| `sensor` | Tên sensor | `sensor` | Công cụ cấp | Không | Để rỗng | Xác minh smoke test, câu e; `cowrie.json:1` |
| `client_version` | Phiên bản client SSH | `version` ở `cowrie.client.version` | Công cụ cấp | Với sự kiện `cowrie.client.version` | Rỗng hoặc chuỗi `""` đều coi là thiếu; phiên Telnet không có sự kiện này nên không tính là lỗi thiếu trường | Xác minh smoke test, câu b; `cowrie.json:3,7` |
| `client_hassh` | Fingerprint HASSH client SSH | `hassh` ở `cowrie.client.kex` | Công cụ cấp | Không | Để rỗng; với phiên Telnet rỗng là bình thường | `cowrie.json:8` |
| `username` | Username thử đăng nhập | `username` ở sự kiện login | Công cụ cấp | Với sự kiện login | Để rỗng, đếm trường thiếu | `cowrie.json:9,14` |
| `password` | Password thử đăng nhập | `password` ở sự kiện login | Công cụ cấp | Với sự kiện login khi có password | Để rỗng; không suy ra từ xác thực public key | Xác minh smoke test, câu d; `cowrie.json:9,14` |
| `login_result` | Kết quả login: `success` hoặc `failed` | Suy từ `eventid` | Suy ra | Với sự kiện login | Không xác định được thì để rỗng và báo | Xác minh smoke test, câu d; `cowrie.json:9,14` |
| `command` | Nội dung lệnh | `input` ở `cowrie.command.input` | Công cụ cấp | Với sự kiện lệnh | Để rỗng | `cowrie.json:18` |
| `command_supported` | Trạng thái hỗ trợ lệnh | Đối chiếu `input` của `cowrie.command.input` và `cowrie.command.failed` cùng phiên | Suy ra | Không | Chỉ nhận `unsupported` hoặc `unknown`; không suy thành `supported` | Câu h: chỉ quan sát ở lần TV1 gõ thêm ngoài smoke test, dòng 116–117 |
| `download_url` | URL tải | `url` ở `cowrie.session.file_download` | Công cụ cấp | Không | Để rỗng | Theo schema Cowrie; chưa có event này trong smoke test |
| `file_sha256` | SHA-256 tệp tải | `shasum` ở `cowrie.session.file_download` | Công cụ cấp | Không | Để rỗng; chỉ đọc trong đúng event, không nhầm hash TTY | Theo schema Cowrie; chưa có event này trong smoke test |
| `duration_ms` | Thời lượng phiên, mili giây | `duration_ms` chỉ ở `cowrie.session.closed`; không lấy từ `cowrie.log.closed` | Công cụ cấp hoặc suy ra | Không | Với sự kiện khác để rỗng; nếu thiếu ở `session.closed` nhưng có mốc connect và close, tính `close - connect` (mili giây) cho event đóng (`duration_computed=true`) và phiên (`duration_source=computed`) | Xác minh smoke test, câu g; `cowrie.json:4,20` |
| `message` | Thông điệp gốc | `message` | Công cụ cấp | Không | Để rỗng | `cowrie.json:1–58` |
| `scenario_id` | Kịch bản khớp nhật ký | Nhật ký thử nghiệm; quy tắc tại mục 6 | Nhóm gán / suy ra | Với dữ liệu lab | Không khớp hoặc khớp nhiều: ghi trạng thái, chuyển TV3 review | Chưa áp dụng – chờ dữ liệu |
| `run_id` | Mã lượt chạy | Tên thư mục `RUN-xx` | Nhóm gán | Có | Thiếu thì không nhận lượt vào xử lý | Chưa áp dụng – do nhóm gán |
| `data_origin` | Nguồn dữ liệu: `lab`, `tham_khao`, `minh_hoa` | Nhóm gán | Nhóm gán | Có | Không được thiếu | Chưa áp dụng – do nhóm gán |
| `raw_ref` | File và số dòng gốc | Bộ xử lý ghi, dạng `tên_file:dòng` | Nhóm gán | Có | Không được thiếu; nếu không xác định được thì báo lỗi xử lý | Chưa áp dụng – do bộ xử lý ghi |
| `protocol_inferred` | Cờ cho biết protocol được suy ra từ cổng, không phải đọc từ sự kiện | Bộ xử lý | Kỹ thuật | Có, boolean | `false` nếu protocol được cung cấp/lan truyền; `true` nếu suy từ cổng; không suy được thì `protocol` rỗng | Quy ước nhóm |
| `duration_computed` | Cờ cho biết `duration_ms` tại event đóng phiên được tính thay vì lấy từ Cowrie | Bộ xử lý | Kỹ thuật | Có, boolean | `true` chỉ khi thiếu `duration_ms` tại `cowrie.session.closed` và tính được từ connect đến close; ngược lại `false` | Quy ước nhóm |
| `duplicate_count` | Số bản sao dư giống hệt event này đã loại | Bộ xử lý, trước bước khử trùng | Kỹ thuật | Có, số nguyên | `0` nếu không trùng; số lần lặp bị bỏ được gắn vào bản đầu được giữ; đồng thời báo nguồn các dòng trùng trong báo cáo chất lượng | Quy ước nhóm |

`protocol_inferred` phân biệt protocol ghi trong log với giá trị dự phòng suy ra; `duration_computed` phân biệt duration công cụ ghi với duration tự tính; `duplicate_count` giúp truy vết bản trùng bị loại. Phân loại eventid ở bảng dưới là logic nội bộ của bộ xử lý, không phải cột xuất.

### Phân loại eventid dùng chung khi xử lý

| Lớp nội bộ | `eventid` | Trường riêng đọc / cách xử lý | Ghi chú xác minh |
|---|---|---|---|
| Sự kiện phân tích | `cowrie.session.connect` | Không cần trường riêng ngoài các trường chung | Đã thấy, `cowrie.json:1` |
| Sự kiện phân tích | `cowrie.session.closed` | `duration_ms` | Đã thấy, `cowrie.json:4` |
| Sự kiện phân tích | `cowrie.client.version` | `version` | Đã thấy, `cowrie.json:3` |
| Sự kiện phân tích | `cowrie.client.kex` | `hassh` (có thêm thông tin KEX ở log) | Đã thấy, `cowrie.json:8` |
| Sự kiện phân tích | `cowrie.login.failed`, `cowrie.login.success` | `username`, `password` | Đã thấy, `cowrie.json:9,14` |
| Sự kiện phân tích | `cowrie.command.input` | `input` → `command` | Đã thấy, `cowrie.json:18` |
| Sự kiện phân tích | `cowrie.command.failed` | `input`; chỉ đánh dấu lệnh tương ứng là `unsupported` | Không có trong smoke test; chỉ thấy ở lần TV1 gõ thêm, câu h, dòng 116–117 |
| Sự kiện phân tích | `cowrie.session.file_download` | `url`, `shasum`, `outfile` | Theo schema Cowrie; không có event trong smoke test |
| Sự kiện phân tích | `cowrie.session.file_download.failed` | `url` | Trường `url` [XM], chưa có trong smoke test |
| Sự kiện phân tích | `cowrie.log.closed` | `ttylog`, `size`, `shasum`, `duplicate`; không dùng `duration_ms` làm thời lượng phiên | Đã thấy, `cowrie.json:20` |
| Sự kiện phụ đã biết | `cowrie.telnet.option`, `cowrie.client.size`, `cowrie.client.var`, `cowrie.session.params` | Giữ trong `events.csv` với `event_type` và trường chung; không đọc trường riêng để phân tích | Đã thấy lần lượt tại `cowrie.json:23`, `15`, `16`, `17` |
| Event lạ thật sự | Mọi `eventid` không thuộc hai lớp trên | Không ánh xạ, ghi file:dòng, loại khỏi `events.csv` cho tới TV3 review | Phát hiện theo allowlist này |

`uuid` có ở 58/58 sự kiện (`cowrie.json:1–58`), nhưng là định danh cài đặt Cowrie, không phải định danh sự kiện/phiên. Bỏ qua có chủ đích; không dùng làm khóa hoặc trường xuất.

### `sessions.csv`

Một dòng cho mỗi `session_id` xác định được trong một `run_id`.

| Tên trường | Ý nghĩa / nguồn hoặc cách tính | Trạng thái xác minh |
|---|---|---|
| `session_id` | ID phiên từ `session` | `cowrie.json:1–58` |
| `run_id` | Tên thư mục `RUN-xx` | Do nhóm gán |
| `scenario_id` | Kịch bản gắn theo mục 6 | Chờ nhật ký |
| `scenario_match_status` | `matched` (đúng một kịch bản), `unmatched` (không khớp hoặc không có nhật ký), `ambiguous` (khớp từ hai kịch bản trở lên), `needs_review` (có nhật ký nhưng thiếu δ hoặc dữ liệu phiên để so khớp) | Quy ước nhóm |
| `scenario_candidates` | Danh sách `scenario_id` ứng viên khi `ambiguous`; rỗng với các trạng thái khác | Quy ước nhóm |
| `src_ip` | IP nguồn từ `src_ip` | `cowrie.json:1–58` |
| `protocol` | Giao thức từ `protocol`; hiện diện trên mọi event smoke test | Xác minh câu a/c; `cowrie.json:1–58` |
| `dst_port` | Cổng đích từ `dst_port` | Xác minh câu c; `cowrie.json:1–58` |
| `start_utc` | Thời điểm sớm nhất của phiên sau parse từ `timestamp` | Xác minh câu j; `cowrie.json:1–58` |
| `end_utc` | Thời điểm muộn nhất của phiên sau parse từ `timestamp` | Xác minh câu j; `cowrie.json:1–58` |
| `duration_ms` | Chỉ lấy từ `duration_ms` ở `cowrie.session.closed`; nếu thiếu nhưng có mốc connect và close, tính `close - connect` (mili giây), đồng thời đặt `duration_computed=true` ở event đóng và `duration_source=computed` ở phiên | Xác minh câu g; `cowrie.json:4,20` (`log.closed` cũng có nhưng không dùng) |
| `duration_source` | `tool` nếu lấy từ log; `computed` nếu tự tính; rỗng nếu không xác định | Quy ước nhóm; tương ứng `duration_computed` trong `events.csv` |
| `n_events` | Số sự kiện của phiên sau khử trùng | Bộ xử lý |
| `n_login_failed` | Số sự kiện `cowrie.login.failed` | `cowrie.json:9,25,36,51` |
| `n_login_success` | Số sự kiện `cowrie.login.success` | `cowrie.json:14,26,41,52` |
| `n_commands` | Số sự kiện `cowrie.command.input` | `cowrie.json:18` |
| `commands` | Danh sách `input` của `cowrie.command.input`, theo timestamp tăng dần; nếu bằng nhau giữ thứ tự file:dòng | `cowrie.json:18` |
| `has_download` | Có sự kiện `cowrie.session.file_download` hay không | Theo allowlist; chưa có event trong smoke test |
| `closed_properly` | Có sự kiện `cowrie.session.closed` hay không | `cowrie.json:4,5` |
| `client_version` | Giá trị `version` ở `cowrie.client.version`; chuỗi rỗng coi là thiếu | Xác minh câu b; `cowrie.json:3,7` |
| `data_origin` | Nguồn dữ liệu của lượt | Nhóm gán |

## 5. Quy tắc suy ra

- **`login_result`:** `success` chỉ từ `cowrie.login.success`, `failed` chỉ từ `cowrie.login.failed`. Không suy kết quả từ trường khác. Hai event có mặt ở `cowrie.json:9,14`.
- **`command_supported`:** gán `unsupported` khi có `cowrie.command.failed` cùng `session_id` và cùng `input` với lệnh; trường hợp còn lại là `unknown`. Không gán `supported`: không có dấu hiệu thất bại không chứng minh shell đã thực thi/hỗ trợ lệnh, và log có thể thiếu sự kiện. `unknown` cũng bao gồm trường hợp shell giả báo lỗi tùy chọn/đối số nhưng không phát `command.failed`. Smoke test không có event `command.failed`; cặp khớp ngay sau `command.input` chỉ được thấy trong lần TV1 gõ thêm ngoài smoke test (câu h, dòng 116–117).
- **`protocol`:** log smoke test có `protocol` ở mọi event, không cần lan truyền cho log này (câu c). Với log khác, lấy giá trị hiện diện; nếu thiếu ở một event thì lan truyền theo phiên từ connect. Chỉ khi không có protocol trong phiên mới dự phòng suy từ `dst_port`: 2222 → `ssh`, 2223 → `telnet`; đặt `protocol_inferred=true`. Cổng là quy ước lab, không đủ căn cứ thì để rỗng.
- **`duration_ms`:** chỉ lấy số nguyên `duration_ms` của `cowrie.session.closed`; không lấy từ `cowrie.log.closed` dù event này cũng có trường cùng tên (câu g; `cowrie.json:4,20`). Nếu thiếu ở `session.closed` nhưng có connect và close, tính từ close − connect theo mili giây cho cả event đóng và `sessions.csv`; đặt `duration_computed=true` ở event đóng và `duration_source=computed` ở phiên. Không có đủ mốc thì để rỗng; không dùng trường cũ `duration`.
- **`client_version` và `client_hassh`:** chuỗi `""` coi như thiếu. Với sự kiện/phiên Telnet, `client_version` và `client_hassh` rỗng là bình thường, không báo lỗi chất lượng (câu b).

## 6. Gắn kịch bản (`scenario_id`)

Khớp một phiên với nhật ký thử nghiệm theo cả ba điều kiện:

1. `src_ip` của phiên bằng `ip_nguon` của nhật ký.
2. `dst_port` của phiên bằng cổng suy từ `dich_vu_cong` (ví dụ `ssh/2222` → 2222, `telnet/2223` → 2223).
3. Thời gian phiên giao với khoảng nhật ký mở rộng mỗi đầu bởi `|δ| + 1 giây`, trong đó δ là độ lệch giờ đo trước lượt chạy; 1 giây là dung sai thao tác riêng cho độ chính xác đến giây của nhật ký và độ trễ bắt đầu kết nối, không thay thế hay làm thay đổi δ.

Chỉ một kịch bản phù hợp thì gán `scenario_id` và `scenario_match_status=matched`. Không có kết quả hoặc không có file nhật ký thì `scenario_id` để rỗng, trạng thái `unmatched`; có nhiều hơn một kết quả thì không tự chọn, ghi `ambiguous` và liệt kê ứng viên ở `scenario_candidates`. Nếu có nhật ký nhưng thiếu δ hoặc dữ liệu cần để so khớp thì ghi `needs_review`; không tự giả định δ=0. Báo cáo chất lượng ghi riêng dung sai thao tác 1 giây khi áp dụng. Các phiên unmatched/ambiguous/needs_review được báo để TV3 review. Một kịch bản được phép khớp nhiều phiên (ví dụ KB-02 gồm hai kết nối).

Không ghép theo IP đơn thuần: KB-02 có thể có nhiều kết nối từ cùng nguồn; KB-05 và lượt SSH lặp KB-01 dùng chung nguồn 2. Ghép IP đơn thuần có thể gán nhầm phiên và làm sai số liệu theo kịch bản.

## 7. Xử lý lỗi và báo cáo chất lượng

- **JSON hỏng:** giữ nguyên file raw; bỏ qua dòng không đọc được, ghi `file:dòng` và thông báo lỗi parse vào `bao_cao_chat_luong.txt`; báo TV1 qua `review/issues.md`.
- **Phân loại eventid:** dùng đúng allowlist ở mục 4. Sự kiện phân tích đọc trường riêng đã quy định; sự kiện phụ đã biết vẫn giữ trong `events.csv` với `event_type` và trường chung, không đọc trường riêng; eventid ngoài hai nhóm là event lạ thật sự.
- **Event lạ thật sự:** ghi eventid và `file:dòng` vào báo cáo chất lượng, không ánh xạ, loại khỏi `events.csv` cho tới TV3 review; báo TV1 qua `review/issues.md`. Không coi event phụ đã biết là event lạ.
- **Thiếu trường bắt buộc:** không tự điền. Giữ rỗng và đếm theo event type trong báo cáo chất lượng. Nếu thiếu `event_type` hoặc thời điểm không thể chuẩn hóa thì không đưa dòng vào `events.csv`; thiếu `session_id` thì không nhóm vào `sessions.csv`; các trường thiếu khác được giữ rỗng để không mất phần còn dùng được. `client_version`/`client_hassh` rỗng trong phiên Telnet không tính là lỗi.
- `client.version` rỗng ở phiên chỉ dò cổng (tối đa 3 event trong phiên, không có `client.kex`) được ghi chú riêng trong báo cáo là trường hợp bình thường, không phải mất dữ liệu; bộ đếm trường thiếu vẫn giữ nguyên để phản ánh log nguồn.
- **Trùng:** theo H.4, trùng hoàn toàn là cùng loại sự kiện, phiên, thời điểm và nội dung. Chỉ giữ một bản, đếm bản dư và ghi nguồn các dòng trùng vào báo cáo chất lượng.
- **Timestamp không parse được:** không thể sắp xếp hoặc so UTC đáng tin cậy; loại khỏi dữ liệu chuẩn hóa và ghi `file:dòng` vào báo cáo.
- **Báo lỗi:** mỗi lỗi cần tái hiện được; tạo/cập nhật `review/issues.md` với file:dòng, loại/mức độ lỗi, kết quả mong đợi, kết quả thực tế và ảnh hưởng. Không sửa file raw để “chữa” lỗi.

`bao_cao_chat_luong.txt` được lưu mặc định tại
`data/processed/RUN-xx/bao_cao_chat_luong.txt` theo quy ước Plan mục E.5/C4;
có thể đổi riêng thư mục báo cáo bằng tùy chọn `--out-results`. Báo cáo tối thiểu liệt kê:

1. `run_id`, các file đầu vào, kết quả kiểm tra SHA-256.
2. Số dòng đọc, JSON hợp lệ, JSON hỏng, dòng trống, bản trùng bị loại.
3. Số event lạ thật sự theo event type và vị trí file:dòng; tách riêng số sự kiện phụ đã biết.
4. Trường bắt buộc bị thiếu theo event type.
5. Timestamp không parse được, vị trí và số dòng bị loại.
6. Số phiên không khớp/khớp nhiều kịch bản; số protocol/duration được suy ra.
7. Đường dẫn `review/issues.md` nếu có issue. Không ghi thời điểm chạy, để hai lần chạy cho kết quả giống hệt nhau.

## 8. Múi giờ

`events.csv`, `sessions.csv`, báo cáo chất lượng và mọi đầu ra khác lưu thời gian UTC. Nhật ký thử nghiệm ghi UTC. δ (đơn vị giây) lấy từ độ lệch đồng hồ đo trước lượt chạy, lưu ở `clock_offset_s` trong `run_note.txt`; đây là nguồn duy nhất. Tham số dòng lệnh `--delta-seconds` chỉ dùng để ghi đè khi cần và phải được ghi vào báo cáo chất lượng. Không tự giả định δ bằng 0. Chỉ đổi sang giờ Việt Nam khi hiển thị, không thay giá trị lưu trữ.

## 9. Dữ liệu minh họa

Dữ liệu minh họa được dùng để viết và kiểm thử mã trước khi có log thật; đặt `data_origin=minh_hoa`. Không đưa dữ liệu minh họa vào bảng, biểu đồ, nhận xét hay kết quả nghiên cứu.

## 10. Kết quả xác minh trên smoke test (câu a–j)

Đối chiếu với `evidence/xac_minh_hop_dong_du_lieu.md`; TV2 cũng tự đọc và kiểm tra `evidence/smoke_test/cowrie.json` (58 dòng) sau khi xác minh SHA-256. Kết quả:

| # | Kết quả | Căn cứ |
|---|---|---|
| a | Connect Telnet có `protocol="telnet"`; SSH có `"ssh"` | Câu a; `cowrie.json:1,2,22,33,48` |
| b | Phiên Telnet không có `cowrie.client.version`/`cowrie.client.kex`; client version và HASSH rỗng là bình thường | Câu b; không có event đó trong phiên Telnet |
| c | Cả 58/58 event đều có `dst_port`, `dst_ip`, `protocol`; protocol không cần lan truyền hay suy ra cho log này | Câu c; `cowrie.json:1–58` |
| d | Cả 4 `login.failed` và 4 `login.success` đều có `password` kiểu chuỗi | Câu d; ví dụ `cowrie.json:9,14` |
| e | `sensor` là `vm-h` ở 58/58 event; đây là tên sensor/máy, không phải tên máy giả kẻ tấn công nhìn thấy | Câu e; `cowrie.json:1` |
| f | Chỉ có `cowrie.json`; không chạy qua nửa đêm nên chưa xác định được tên file xoay vòng: `[XM]` | Câu f; `evidence/smoke_test/` |
| g | 8/8 `session.closed` có `duration_ms` kiểu số nguyên. `log.closed` cũng có trường này nhưng không dùng để tính duration phiên | Câu g; `cowrie.json:4,20` |
| h | Smoke test không có `command.failed`. Ở lượt TV1 gõ thêm ngoài smoke test, event này đứng ngay sau `command.input`, cùng session và input (dòng 116–117) | Câu h; không tính là event của smoke test |
| i | `ttylog` nằm ở `cowrie.log.closed`, giá trị dạng `var/lib/cowrie/tty/<hash>`; tên file đối chiếu với bản được chép vào `tty/` | Câu i; `cowrie.json:20` |
| j | 58/58 timestamp dạng `YYYY-MM-DDTHH:MM:SS.ffffffZ`; không có `+00:00`, đủ sáu chữ số phần thập phân | Câu j; ví dụ `cowrie.json:1` |

Các trường chung `dst_ip`, `dst_port`, `eventid`, `message`, `protocol`, `sensor`, `session`, `src_ip`, `src_port`, `timestamp`, `uuid` đều có ở 58/58 dòng. `uuid` được bỏ qua có chủ đích (mục 4). Cách cài và phiên bản Cowrie được ghi trong `evidence/smoke_test/README.md`: Cowrie 3.1.6, cài bằng pip trong venv.

## 11. Điều kiện sẵn sàng BG-05

| Mã | Từ → Đến | Kích hoạt khi | Bàn giao gì | Vị trí | Điều kiện sẵn sàng (phải kiểm tra được) | Mở khóa việc | Trạng thái |
|---|---|---|---|---|---|---|---|
| **BG-05** | TV2 → TV1 | WP-05 chốt | Hợp đồng dữ liệu A→B | `docs/04_hop_dong_du_lieu.md` | Tên trường đã đối chiếu với log smoke test thật; có quy định nơi chuyển log, cách giữ log gốc, múi giờ UTC, xử lý trường thiếu; TV3 đã review | TV1 xuất log đúng quy định | Chưa – chờ TV3 review |

*Ghi chú BG-05:* đã nhận BG-02 và ghi kết quả đối chiếu vào mục 10; trạng thái vẫn "Chưa" cho tới khi TV3 review. Các trường/tên file không xuất hiện trong smoke test được nêu rõ ở mục 4; chưa coi hợp đồng đã được review hoặc bàn giao.