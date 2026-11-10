# Hợp đồng dữ liệu A → B (TV1 → TV2)

**Trạng thái:** BẢN NHÁP – chờ log smoke test thật (BG-02)  
**Người soạn:** TV2  
**Ngày:** 2026-11-10

Quy ước: `[XM]` nghĩa là tên trường, giá trị hoặc hành vi lấy từ tài liệu Cowrie nhưng **chưa xác minh trên log smoke test thật**. Không có trường Cowrie nào trong tài liệu này được xem là đã xác minh.

## 1. Phạm vi và nguyên tắc

- TV1 bàn giao log gốc theo từng lượt; TV2 không sửa `data/raw/`. Luồng dữ liệu là `raw` → `processed` → `results`.
- Trước xử lý, kiểm tra `SHA256SUMS`. Ghi `events.csv`, `sessions.csv` và `bao_cao_chat_luong.txt` vào `data/processed/RUN-xx/`; chỉ bảng/biểu đồ O1–O7 vào `results/RUN-xx/`.
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

`run_note.txt` là **đề xuất của TV2, cần TV1 đồng ý** (README lab Bước 15 hiện chưa tạo file này; theo F.3 của kế hoạch chỉ yêu cầu "một dòng ghi chú"). File là một dòng ghi đủ: thời điểm bắt đầu và kết thúc UTC, độ lệch giờ đo (δ), phiên bản Cowrie và mã/phiên bản cấu hình đã dùng; không ghi bí mật. Ví dụ định dạng:

```text
start_utc=<ISO-8601 UTC>; end_utc=<ISO-8601 UTC>; clock_offset_s=<δ giây, số thực, có dấu: giờ VM-A trừ giờ VM-H>; cowrie_version=<version>; config_version=<revision>
```

Log smoke test thật để xác minh schema được đặt trong `evidence/smoke_test/`, kèm phiên bản Cowrie và cách cài; không trộn với log lượt chạy trong `data/raw/RUN-xx/`.

## 3. Log xoay vòng

TV2 đọc mọi file khớp `cowrie.json*` trong thư mục lượt chạy, không chỉ file có tên chính xác `cowrie.json`. Tên file sau khi Cowrie xoay vòng là `[XM]`. Để tránh phải xác định quan hệ giữa các file qua ranh giới ngày, TV1 bố trí lượt thử không chạy qua nửa đêm UTC; nếu không tránh được, vẫn bàn giao và giữ nguyên tất cả file khớp mẫu.

## 4. Từ điển dữ liệu

### `events.csv`

Mỗi dòng tương ứng một sự kiện hợp lệ sau chuẩn hóa; trường không có trong sự kiện được để rỗng, không tự điền giá trị suy đoán. Bảng dưới gồm **24 trường H.3** và ba cột kỹ thuật đề xuất (`protocol_inferred`, `duplicate_count`, `known_event_type`). Mọi nguồn Cowrie mang `[XM]`.

| Tên trường | Ý nghĩa | Nguồn (trường Cowrie) | Loại | Bắt buộc | Xử lý khi thiếu | Trạng thái xác minh |
|---|---|---|---|---|---|---|
| `event_time_utc` | Thời điểm sự kiện UTC | `timestamp` [XM] | Công cụ cấp | Có | Không parse được: loại khỏi dữ liệu chuẩn hóa, ghi file:dòng và báo cáo chất lượng | [XM] |
| `event_type` | Loại sự kiện | `eventid` [XM] | Công cụ cấp | Có | Loại khỏi dữ liệu chuẩn hóa; ghi file:dòng và báo lỗi | [XM] |
| `session_id` | Định danh phiên | `session` [XM] | Công cụ cấp | Có với sự kiện thuộc phiên | Để rỗng, không ghép phiên, đánh dấu review | [XM] |
| `src_ip` | IP nguồn | `src_ip` [XM] | Công cụ cấp | Có | Để rỗng; báo trường thiếu | [XM] |
| `src_port` | Cổng nguồn | `src_port` [XM] | Công cụ cấp | Không | Để rỗng | [XM] |
| `dst_ip` | IP đích | `dst_ip` [XM] | Công cụ cấp | Không | Để rỗng | [XM] |
| `dst_port` | Cổng đích | `dst_port` [XM] | Công cụ cấp | Không | Để rỗng | [XM] |
| `protocol` | Giao thức ssh/telnet | `protocol` [XM] ở sự kiện connect; có thể lan truyền theo phiên | Công cụ cấp / suy ra | Không | Ưu tiên lan truyền trong phiên; nếu suy từ cổng, bật `protocol_inferred` | [XM] |
| `sensor` | Tên sensor | `sensor` [XM] | Công cụ cấp | Không | Để rỗng | [XM] |
| `client_version` | Phiên bản client | `version` [XM] ở `cowrie.client.version` [XM] | Công cụ cấp | Không | Để rỗng | [XM] |
| `client_hassh` | Fingerprint HASSH client | `hassh` [XM] ở `cowrie.client.kex` [XM] | Công cụ cấp | Không | Để rỗng | [XM] |
| `username` | Username thử đăng nhập | `username` [XM] ở sự kiện login [XM] | Công cụ cấp | Với sự kiện login | Để rỗng, đếm trường thiếu | [XM] |
| `password` | Password thử đăng nhập | `password` [XM] ở sự kiện login [XM] | Công cụ cấp | Với sự kiện login nếu log có trường này | Để rỗng; không suy ra từ xác thực public key | [XM] |
| `login_result` | Kết quả login: `success` hoặc `failed` | Suy từ `eventid` [XM] tương ứng [XM] | Suy ra | Với sự kiện login | Không xác định được thì để rỗng và báo | [XM] |
| `command` | Nội dung lệnh | `input` [XM] ở `cowrie.command.input` [XM] | Công cụ cấp | Với sự kiện lệnh | Để rỗng | [XM] |
| `command_supported` | Trạng thái hỗ trợ lệnh | Đối chiếu `input` [XM] giữa `cowrie.command.input` và `cowrie.command.failed` [XM] cùng phiên | Suy ra | Không | Chỉ nhận `unsupported` hoặc `unknown`; không suy thành `supported` | [XM] |
| `download_url` | URL tải | `url` [XM] ở `cowrie.session.file_download` [XM] | Công cụ cấp | Không | Để rỗng | [XM] |
| `file_sha256` | SHA-256 tệp tải | `shasum` [XM] ở `cowrie.session.file_download` [XM] | Công cụ cấp | Không | Để rỗng | [XM] |
| `duration_ms` | Thời lượng phiên, mili giây | `duration_ms` [XM] ở `cowrie.session.closed` [XM]; chỉ lấy từ log, không tự tính ở bảng này (thời lượng tự tính nằm ở `sessions.csv`) | Công cụ cấp | Không | Để rỗng | [XM] |
| `message` | Thông điệp gốc | `message` [XM] | Công cụ cấp | Không | Để rỗng | [XM] |
| `scenario_id` | Kịch bản khớp nhật ký | Nhật ký thử nghiệm; quy tắc tại mục 6 | Nhóm gán / suy ra | Với dữ liệu lab | Không khớp hoặc khớp nhiều: ghi trạng thái, chuyển TV3 review | Chưa áp dụng – chờ dữ liệu |
| `run_id` | Mã lượt chạy | Tên thư mục `RUN-xx` | Nhóm gán | Có | Thiếu thì không nhận lượt vào xử lý | Chưa áp dụng – do nhóm gán |
| `data_origin` | Nguồn dữ liệu: `lab`, `tham_khao`, `minh_hoa` | Nhóm gán | Nhóm gán | Có | Không được thiếu | Chưa áp dụng – do nhóm gán |
| `raw_ref` | File và số dòng gốc | Bộ xử lý ghi, dạng `tên_file:dòng` | Nhóm gán | Có | Không được thiếu; nếu không xác định được thì báo lỗi xử lý | Chưa áp dụng – do bộ xử lý ghi |
| `protocol_inferred` | Cờ cho biết protocol được suy ra từ cổng, không phải đọc từ sự kiện | Bộ xử lý | Kỹ thuật (nhóm đề xuất) | Có, boolean | `false` nếu protocol được cung cấp/lan truyền; `true` nếu suy từ cổng; không suy được thì `protocol` rỗng | Chờ TV3 review |
| `duplicate_count` | Số bản sao dư của sự kiện trùng bị loại | Bộ xử lý, trước bước khử trùng | Kỹ thuật (nhóm đề xuất) | Không | Ghi tổng bản sao dư trong `bao_cao_chat_luong.txt`; không nhân bản dòng chuẩn hóa | Chờ TV3 review |
| `known_event_type` | `true` nếu `event_type` thuộc danh sách đã biết trong `docs/01` mục 3.1; `false` nếu là eventid chưa biết (dòng vẫn được giữ) | Bộ xử lý | Kỹ thuật (nhóm đề xuất) | Có, boolean | Không áp dụng | Chờ TV3 review |

`protocol_inferred` giúp phân biệt dữ liệu công cụ ghi với dữ liệu suy ra, tránh trình bày suy luận như sự kiện gốc. `duplicate_count` giúp truy vết số bản sao đã loại theo H.4. `known_event_type` giữ lại mọi sự kiện hợp lệ (kể cả eventid lạ) để số dòng `events.csv` khớp phép đếm độc lập của TV3 ở WP-09, đồng thời vẫn lọc được các sự kiện chưa biết.

### `sessions.csv`

Một dòng cho mỗi `session_id` xác định được trong một `run_id`. Các nguồn Cowrie trong bảng đều `[XM]`.

| Tên trường | Ý nghĩa / nguồn hoặc cách tính | Trạng thái xác minh |
|---|---|---|
| `session_id` | ID phiên từ `session` [XM] | [XM] |
| `run_id` | Tên thư mục `RUN-xx` | Do nhóm gán |
| `scenario_id` | Kịch bản gắn theo mục 6 | Chờ nhật ký |
| `scenario_match_status` | `matched` (đúng một kịch bản), `unmatched` (không khớp kịch bản nào), `ambiguous` (khớp từ hai kịch bản trở lên), `no_notebook` (không có nhật ký thử nghiệm để đối chiếu) | Quy ước nhóm |
| `scenario_candidates` | Danh sách `scenario_id` ứng viên khi `ambiguous`; rỗng với các trạng thái khác | Quy ước nhóm |
| `src_ip` | IP nguồn từ `src_ip` [XM] | [XM] |
| `protocol` | Giao thức từ `protocol` [XM], lan truyền hoặc suy theo mục 5 | [XM] |
| `dst_port` | Cổng đích từ `dst_port` [XM] (thường lấy từ connect nếu sự kiện khác không có) | [XM] |
| `start_utc` | Thời điểm sớm nhất của phiên sau parse từ `timestamp` [XM] | [XM] |
| `end_utc` | Thời điểm muộn nhất của phiên sau parse từ `timestamp` [XM] | [XM] |
| `duration_ms` | Từ `duration_ms` [XM] ở `session.closed` [XM], nếu có; nếu thiếu, tính `end_utc - start_utc` | [XM] |
| `duration_source` | `tool` nếu lấy từ log; `computed` nếu tự tính (cờ "tự tính" của H.3 nằm ở đây); rỗng nếu không xác định | Quy ước nhóm |
| `n_events` | Số sự kiện của phiên sau khử trùng | Bộ xử lý |
| `n_login_failed` | Số sự kiện `cowrie.login.failed` [XM] | [XM] |
| `n_login_success` | Số sự kiện `cowrie.login.success` [XM] | [XM] |
| `n_commands` | Số sự kiện `cowrie.command.input` [XM] | [XM] |
| `commands` | Danh sách `input` [XM] của `cowrie.command.input` [XM], theo timestamp tăng dần; nếu bằng nhau giữ thứ tự file:dòng | [XM] |
| `has_download` | Có sự kiện `cowrie.session.file_download` [XM] hay không | [XM] |
| `closed_properly` | Có sự kiện `cowrie.session.closed` [XM] hay không | [XM] |
| `client_version` | Giá trị `version` [XM] ở `cowrie.client.version` [XM], nếu có | [XM] |
| `data_origin` | Nguồn dữ liệu của lượt | Nhóm gán |

## 5. Quy tắc suy ra

- **`login_result`:** `success` chỉ từ `cowrie.login.success` [XM], `failed` chỉ từ `cowrie.login.failed` [XM]. Không suy kết quả từ trường khác.
- **`command_supported`:** gán `unsupported` khi có `cowrie.command.failed` [XM] cùng `session_id` và cùng `input` [XM] với lệnh; trường hợp còn lại là `unknown`. Không gán `supported`: không có dấu hiệu thất bại không chứng minh shell đã thực thi/hỗ trợ lệnh, và log có thể thiếu hoặc không ghi sự kiện tương ứng.
- **`protocol`:** lấy protocol từ sự kiện connect [XM], rồi lan truyền cho sự kiện khác trong cùng phiên. Nếu thiếu, có thể dự phòng suy theo `dst_port`: 2222 → `ssh`, 2223 → `telnet`; đặt `protocol_inferred=true`. Đây là quy ước cổng dự kiến của lab, phải xác minh khi nhận log thật. Không đủ căn cứ thì để rỗng.
- **`duration_ms`:** ưu tiên số nguyên `duration_ms` [XM] của sự kiện đóng phiên [XM]. Nếu thiếu nhưng có mốc mở và đóng, tính `end_utc - start_utc` theo mili giây ở `sessions.csv`, đặt `duration_source=computed` (`events.csv` không tự tính thời lượng). Không có đủ mốc thì để rỗng; không dùng trường cũ `duration` [XM] thay thế nếu chưa xác minh.

## 6. Gắn kịch bản (`scenario_id`)

Khớp một phiên với nhật ký thử nghiệm theo cả ba điều kiện:

1. `src_ip` của phiên bằng `ip_nguon` của nhật ký.
2. `dst_port` của phiên bằng cổng suy từ `dich_vu_cong` (ví dụ `ssh/2222` → 2222, `telnet/2223` → 2223).
3. Thời gian phiên giao với khoảng nhật ký `[bắt đầu − δ, kết thúc + δ]`, trong đó δ là độ lệch giờ đo trước lượt chạy.

Chỉ một kịch bản phù hợp thì gán `scenario_id` và `scenario_match_status=matched`. Không có kết quả thì `scenario_id` để rỗng, trạng thái `unmatched`; có nhiều hơn một kết quả thì không tự chọn, ghi `ambiguous` và liệt kê ứng viên ở `scenario_candidates`. Hai trường hợp này phải được báo TV3 review. Không có file nhật ký thì trạng thái `no_notebook`, không bịa kịch bản. Một kịch bản được phép khớp nhiều phiên (ví dụ KB-02 gồm hai kết nối).

Không ghép theo IP đơn thuần: KB-02 có thể có nhiều kết nối từ cùng nguồn; KB-05 và lượt SSH lặp KB-01 dùng chung nguồn 2. Ghép IP đơn thuần có thể gán nhầm phiên và làm sai số liệu theo kịch bản.

## 7. Xử lý lỗi và báo cáo chất lượng

- **JSON hỏng:** giữ nguyên file raw; bỏ qua dòng không đọc được, ghi `file:dòng` và thông báo lỗi parse vào `bao_cao_chat_luong.txt`; báo TV1 qua `review/issues.md`.
- **Event lạ** (eventid không thuộc danh sách đã biết): **giữ** dòng trong `events.csv` với `known_event_type=false`, không ánh xạ thành event đã biết và không đoán trường; ghi `eventid` và `file:dòng` vào báo cáo chất lượng; báo TV1 qua `review/issues.md`. Không loại, vì sẽ làm số sự kiện lệch với phép đếm độc lập.
- **Thiếu trường bắt buộc:** không tự điền. Giữ rỗng và đếm theo event type [XM] trong báo cáo chất lượng. Nếu thiếu `event_type` hoặc thời điểm không thể chuẩn hóa thì không đưa dòng vào `events.csv`; thiếu `session_id` thì không nhóm vào `sessions.csv`; các trường thiếu khác được giữ rỗng để không mất phần còn dùng được.
- **Trùng:** theo H.4, trùng hoàn toàn là cùng loại sự kiện, phiên, thời điểm và nội dung. Chỉ giữ một bản, đếm bản dư và ghi nguồn các dòng trùng vào báo cáo chất lượng.
- **Timestamp không parse được:** không thể sắp xếp hoặc so UTC đáng tin cậy; loại khỏi dữ liệu chuẩn hóa và ghi `file:dòng` vào báo cáo.
- **Báo lỗi:** mỗi lỗi cần tái hiện được; tạo/cập nhật `review/issues.md` với file:dòng, loại/mức độ lỗi, kết quả mong đợi, kết quả thực tế và ảnh hưởng. Không sửa file raw để “chữa” lỗi.

`bao_cao_chat_luong.txt` tối thiểu liệt kê:

1. `run_id`, các file đầu vào, kết quả kiểm tra SHA-256.
2. Số dòng đọc, JSON hợp lệ, JSON hỏng, dòng trống, bản trùng bị loại.
3. Số event lạ theo event type và vị trí file:dòng.
4. Trường bắt buộc bị thiếu theo event type.
5. Timestamp không parse được, vị trí và số dòng bị loại.
6. Số phiên không khớp/khớp nhiều kịch bản; số protocol/duration được suy ra.
7. Đường dẫn `review/issues.md` nếu có issue. Không ghi thời điểm chạy, để hai lần chạy cho kết quả giống hệt nhau.

## 8. Múi giờ

`events.csv`, `sessions.csv`, báo cáo chất lượng và mọi đầu ra khác lưu thời gian UTC. Nhật ký thử nghiệm ghi UTC. δ (đơn vị giây) lấy từ độ lệch đồng hồ đo trước lượt chạy, lưu ở `clock_offset_s` trong `run_note.txt`; đây là nguồn duy nhất. Tham số dòng lệnh `--delta-seconds` chỉ dùng để ghi đè khi cần và phải được ghi vào báo cáo chất lượng. Không tự giả định δ bằng 0. Chỉ đổi sang giờ Việt Nam khi hiển thị, không thay giá trị lưu trữ.

## 9. Dữ liệu minh họa

Dữ liệu minh họa được dùng để viết và kiểm thử mã trước khi có log thật; đặt `data_origin=minh_hoa`. Không đưa dữ liệu minh họa vào bảng, biểu đồ, nhận xét hay kết quả nghiên cứu.

## 10. Câu hỏi cho TV1 – xác minh trên log smoke test thật

Chạy trên VM-H (nơi đã cài `jq`, theo README lab Bước 13.5) tại thư mục chứa các file `cowrie.json*`, hoặc sau này dùng `analysis/tools/inspect_log.py` trên log đã chép về `evidence/smoke_test/`; Git Bash trên Windows có thể chưa có `jq`. Các lệnh dưới đây chỉ đọc log. Trước khi dùng mẫu glob, xác nhận thư mục có đúng các file `cowrie.json*`.

| # | Câu hỏi cần xác minh | Lệnh kiểm tra |
|---|---|---|
| a | Sự kiện connect của Telnet có trường `protocol` không; giá trị chính xác là gì? | `jq -c 'select(.eventid=="cowrie.session.connect" and (.protocol=="telnet" or .dst_port==2223)) \| {eventid,session,has_protocol:has("protocol"),protocol,dst_port}' cowrie.json*` |
| b | Phiên Telnet có sinh `client.version` hoặc `client.kex` không? | `jq -s -c '[.[] \| select(.eventid=="cowrie.session.connect" and (.protocol=="telnet" or .dst_port==2223)) \| .session] as $s \| .[] \| select(.session as $id \| $s \| index($id)) \| select(.eventid=="cowrie.client.version" or .eventid=="cowrie.client.kex") \| {eventid,session}' cowrie.json*` (không có dòng kết quả nghĩa là không thấy hai event đó trong phiên Telnet) |
| c | Các event sau connect có mang `dst_port`, `dst_ip`, `protocol` không? | `jq -c 'select(.eventid!="cowrie.session.connect") \| {eventid,session,has_dst_port:has("dst_port"),has_dst_ip:has("dst_ip"),has_protocol:has("protocol")}' cowrie.json*` |
| d | Event login.failed/success có trường `password` không; kiểu dữ liệu là gì? | `jq -c 'select(.eventid=="cowrie.login.failed" or .eventid=="cowrie.login.success") \| {eventid,session,has_password:has("password"),password_type:(.password\|type)}' cowrie.json*` (không in giá trị credential) |
| e | Các giá trị `sensor` thực tế là gì? | `jq -r 'select(has("sensor")) \| .sensor' cowrie.json* \| sort -u` |
| f | Tên file sau xoay vòng là gì? | `find . -maxdepth 1 -type f -name 'cowrie.json*' -printf '%f\n'` |
| g | `session.closed` có `duration_ms` không và có phải số nguyên không? | `jq -c 'select(.eventid=="cowrie.session.closed") \| {session,has_duration_ms:has("duration_ms"),duration_ms,duration_type:(.duration_ms\|type)}' cowrie.json*` |
| h | `command.failed` có cùng `input` với `command.input` và đứng ngay sau trong thứ tự file không? | `jq -s -c 'to_entries[] \| select(.value.eventid=="cowrie.command.input" or .value.eventid=="cowrie.command.failed") \| {line_index:.key,eventid:.value.eventid,session:.value.session,input:.value.input}' cowrie.json*` (đối chiếu chỉ số liền kề, session và input) |
| i | `ttylog` nằm ở event nào; giá trị có chỉ đường dẫn tương đối tới file trong `tty/` không? | `jq -c 'select(has("ttylog")) \| {eventid,session,ttylog}' cowrie.json*; find tty -type f -print` |
| j | Timestamp dùng hậu tố `Z` hay `+00:00`; có phần thập phân/micro giây không? | `jq -r 'select(has("timestamp")) \| .timestamp' cowrie.json* \| grep -E 'Z$|\+00:00$|\.[0-9]+'` (lưu mẫu giá trị và đếm từng dạng; grep không thay cho kiểm tra toàn bộ timestamp) |

Lưu output lệnh, phiên bản Cowrie và cách cài cùng smoke test; TV2 cập nhật nhãn `[XM]` chỉ sau khi đối chiếu được bằng chứng file:dòng. Nếu cấu trúc hoặc giá trị khác dự kiến, TV1 và TV2 thống nhất cập nhật hợp đồng trước khi xuất log lượt chạy.

## 11. Điều kiện sẵn sàng BG-05

| Mã | Từ → Đến | Kích hoạt khi | Bàn giao gì | Vị trí | Điều kiện sẵn sàng (phải kiểm tra được) | Mở khóa việc | Trạng thái |
|---|---|---|---|---|---|---|---|
| **BG-05** | TV2 → TV1 | WP-05 chốt | Hợp đồng dữ liệu A→B | `docs/04_hop_dong_du_lieu.md` | Tên trường đã đối chiếu với log smoke test thật; có quy định nơi chuyển log, cách giữ log gốc, múi giờ UTC, xử lý trường thiếu; TV3 đã review | TV1 xuất log đúng quy định | Chưa |

*Ghi chú BG-05:* các điều kiện "đối chiếu với log smoke test thật" và "TV3 đã review" chưa đạt; chưa tích. Chờ BG-02 và review.