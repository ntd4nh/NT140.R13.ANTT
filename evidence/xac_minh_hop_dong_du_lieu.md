# Trả lời mục 10 của hợp đồng dữ liệu (TV1 → TV2)

**Người làm:** TV1 · **Ngày:** 2026-11-10 · **Dữ liệu:** `evidence/smoke_test/cowrie.json` (58 dòng, Cowrie 3.1.6, `sha256sum -c` OK)

Các câu a–j được chạy **đúng lệnh `jq` ghi trong `docs/04_hop_dong_du_lieu.md` mục 10**, bằng jq 1.7 trên VM-A, với bản sao của log smoke test. Một số lệnh có thêm `| sort | uniq -c` để gộp các dòng giống nhau. Câu h phải dùng thêm log ngoài smoke test (xem câu h).

TV2 dựa vào đây để cập nhật nhãn `[XM]`. TV1 không sửa `docs/04`.

## Trả lời

| # | Câu hỏi | Kết quả trên log thật | Ảnh hưởng tới hợp đồng |
| --- | --- | --- | --- |
| a | Connect của Telnet có `protocol` không? | **Có**, giá trị `"telnet"`; cả 3 phiên Telnet đều có. SSH là `"ssh"` | Xác minh được `protocol` |
| b | Phiên Telnet có `client.version` / `client.kex` không? | **Không**. Lệnh không trả dòng nào | `client_version`, `client_hassh` luôn rỗng với Telnet. Đây là bình thường, không phải lỗi thiếu trường |
| c | Event sau connect có `dst_port`, `dst_ip`, `protocol` không? | **Có ở mọi loại event**, cả 11 loại | Không cần lan truyền hay suy `protocol` từ cổng trên log này. Vẫn giữ phương án dự phòng, nhưng `protocol_inferred` sẽ luôn `false` |
| d | Login có `password` không, kiểu gì? | **Có** ở cả 4 `login.failed` và 4 `login.success`, kiểu `string` | Xác minh được `username`, `password` |
| e | Giá trị `sensor`? | Chỉ một giá trị: `vm-h` (58/58 dòng). Đây là tên **máy thật**, khác tên máy giả `svr04` mà kẻ tấn công thấy | Xác minh được `sensor`. Không lấy `sensor` làm tên máy honeypot trong báo cáo |
| f | Tên file sau xoay vòng? | **Chưa thấy**. Chỉ có `cowrie.json`, vì lượt thử không chạy qua nửa đêm | Giữ `[XM]` |
| g | `session.closed` có `duration_ms`, kiểu số nguyên? | **Có** ở cả 8 phiên, kiểu `number`, giá trị nguyên: `16 15 1043 287 3194 1070 337 3091` | Xác minh được. **Chú ý:** `cowrie.log.closed` **cũng có** `duration_ms` (xem lưu ý 2) |
| h | `command.failed` cùng `input` và đứng ngay sau `command.input`? | Log smoke test **không có** `command.failed` nào. TV1 gõ thêm một lệnh không tồn tại (15:07 UTC, ngoài smoke test): `command.failed` nằm **ngay dòng sau** `command.input` (dòng 116 → 117), **cùng `session`, cùng `input`** (`lenhkhongcothat --abc`) | Quy tắc `command_supported = unsupported` đúng. **Nhưng:** lệnh có thật mà dùng tùy chọn shell giả không hiểu (ví dụ `curl -m 5 ...` báo `option -m not recognized`) thì **không** sinh `command.failed`. Vì vậy `unknown` vẫn có thể là lệnh bị lỗi |
| i | `ttylog` ở event nào, có phải đường dẫn tương đối không? | Chỉ ở `cowrie.log.closed`. Giá trị dạng `var/lib/cowrie/tty/<hash>`, tính từ thư mục Cowrie chứ **không** tính từ thư mục lượt chạy. 4 phiên trỏ cùng **một** file | Muốn ghép thì lấy tên file (phần sau dấu `/` cuối) rồi tìm trong `tty/` của lượt chạy |
| j | Định dạng timestamp? | Cả 58/58 dòng cùng một dạng: `YYYY-MM-DDTHH:MM:SS.ffffffZ` (hậu tố `Z`, 6 chữ số micro giây). Không có dòng nào thiếu `timestamp` | Xác minh được `timestamp`; parse bằng `pd.to_datetime(..., utc=True)` |

## Trường có ở mọi sự kiện (Cowrie 3.1.6)

`dst_ip`, `dst_port`, `eventid`, `message`, `protocol`, `sensor`, `session`, `src_ip`, `src_port`, `timestamp`, `uuid`

Giá trị mẫu: `dst_ip` = `192.168.239.20`; `dst_port` = `2222` hoặc `2223`; `src_port` là cổng tạm phía client.

## Trường riêng theo loại sự kiện

| `eventid` | Trường riêng |
| --- | --- |
| `cowrie.session.connect` | (không có trường riêng) |
| `cowrie.client.version` | `version` |
| `cowrie.client.kex` | `hassh`, `hasshAlgorithms`, `kexAlgs`, `keyAlgs`, `encCS`, `macCS`, `compCS`, `langCS` |
| `cowrie.client.size` | `width`, `height` |
| `cowrie.client.var` | `name`, `value` |
| `cowrie.session.params` | `arch` |
| `cowrie.telnet.option` | `command`, `option_byte`, `option_name` |
| `cowrie.login.failed` / `cowrie.login.success` | `username`, `password` |
| `cowrie.command.input` | `input` |
| `cowrie.command.failed` | `input` (thấy ở lần thử thêm, câu h) |
| `cowrie.log.closed` | `ttylog`, `size`, `shasum`, `duplicate`, `duration_ms` |
| `cowrie.session.closed` | `duration_ms` |
| `cowrie.session.file_download.failed` | `url` (thấy khi kiểm tra cách ly, không có trong smoke test) |

## Lưu ý cho script xử lý

1. **`uuid`** có ở mọi sự kiện nhưng chưa có trong từ điển dữ liệu. Đó là định danh của cài đặt Cowrie, không phải của sự kiện. Không dùng làm khóa.
2. **Trường cùng tên ở nhiều event:**
   - `duration_ms` có ở cả `session.closed` lẫn `log.closed`; cột `duration_ms` của phiên phải **lấy từ `session.closed`**.
   - `shasum` có ở `log.closed` (hash của file TTY); `file_sha256` chỉ lấy từ `session.file_download`.

   Phải lọc theo `eventid` trước khi lấy các trường này.
3. **`client.version` có thể là chuỗi rỗng `""`.** Gặp ở phiên kiểm tra cổng: kết nối rồi đóng ngay, không gửi phiên bản. Nên coi `""` như thiếu.
4. **`cowrie.client.var`** ghi biến môi trường client gửi lên (`name`, `value`); ở smoke test là biến ngôn ngữ của OpenSSH client trên VM-A. Không chứa bí mật, nhưng nên giữ ngoài bảng tóm tắt.
5. Trong log smoke test, 2 phiên đầu (14:47:23, từ `192.168.239.10`) là **phiên kiểm tra cổng**: chỉ có connect và closed, không đăng nhập. Ở lượt chạy thật, TV1 sẽ ghi các thao tác tương tự vào nhật ký để không bị tính thành `unmatched`.

## Đề xuất sửa hợp đồng (TV2 quyết định)

- Thêm `uuid` vào danh sách "trường bỏ qua có chủ đích".
- Mục 5, `duration_ms`: ghi rõ "lấy từ `cowrie.session.closed`, không lấy từ `cowrie.log.closed`".
- Mục 5, `command_supported`: thêm ghi chú rằng `unknown` gồm cả lệnh bị shell giả báo lỗi tùy chọn.
- `client_version`: chuỗi rỗng coi như thiếu.
- `run_note.txt`: TV1 đồng ý định dạng một dòng như mục 2 và sẽ ghi theo đúng định dạng đó cho RUN-01.
