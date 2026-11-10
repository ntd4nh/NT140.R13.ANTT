# Bộ xử lý log Cowrie

## Cài đặt

Từ thư mục gốc repo:

```bash
python -m pip install -r analysis/requirements.txt
```

## Chạy một lượt

Mỗi lượt chạy bằng một lệnh:

```bash
python -m analysis.process_run --run-dir data/raw/RUN-01
```

Có thể thêm nhật ký thử nghiệm H.2 để gắn kịch bản:

```bash
python -m analysis.process_run --run-dir data/raw/RUN-01 --logbook experiments/nhat_ky_thu_nghiem.csv
```

Có thể ghi đè độ lệch giờ từ `run_note.txt` khi cần:

```bash
python -m analysis.process_run --run-dir data/raw/RUN-01 --logbook experiments/nhat_ky_thu_nghiem.csv --delta-seconds 1.0
```

Các tùy chọn `--data-origin`, `--out-processed` và `--out-results` dùng để
khai báo nguồn dữ liệu hoặc đổi thư mục đầu ra. Mặc định, cả `events.csv`,
`sessions.csv` và `bao_cao_chat_luong.txt` nằm trong
`data/processed/RUN-xx/`, theo quy ước tại Plan mục E.5/C4. Nếu chỉ định
`--out-results`, riêng báo cáo chất lượng được ghi vào thư mục đó. Ngoài
`data/raw/RUN-xx`, phải chỉ rõ `--data-origin`. Thư mục `minh_hoa_*` luôn bị
ép thành `minh_hoa`, không thể khai báo là `lab`.

## Đầu vào và đầu ra

- Đầu vào bắt buộc: `SHA256SUMS` và ít nhất một file `cowrie.json*`. Hash của
  mọi file được kê trong manifest, gồm cả file trong `tty/`, phải khớp trước
  khi xử lý.
- Bộ xử lý đọc các file log theo thứ tự xác định: file xoay vòng đứng trước
  `cowrie.json` hiện tại; các file xoay vòng xếp theo tên. Quy tắc hậu tố ngày
  là `[XM]` vì smoke test chưa chạy qua nửa đêm UTC.
- Đầu ra mặc định:
  - `data/processed/RUN-xx/events.csv`
  - `data/processed/RUN-xx/sessions.csv`
  - `data/processed/RUN-xx/bao_cao_chat_luong.txt`
- `events.csv` có 24 trường H.3 và các cột kỹ thuật `protocol_inferred`,
  `duration_computed`, `duplicate_count`.
- Báo cáo chất lượng không ghi thời điểm xử lý; cùng đầu vào và tùy chọn tạo
  nội dung giống hệt nhau từng byte.
- Trong `sessions.csv`, cột `commands` là mảng JSON được mã hóa thành chuỗi
  trong một ô CSV, UTF-8 và không mất thứ tự.
- Nếu không có `--logbook`, kịch bản để trống, trạng thái là `unmatched` và
  báo cáo nêu rõ chưa đối chiếu nhật ký. Nếu có nhật ký nhưng thiếu
  `clock_offset(_s)` trong `run_note.txt`, các phiên cần ghép được đánh dấu
  `needs_review`; bộ xử lý không tự giả định độ lệch bằng 0. Có thể chỉ định
  `--delta-seconds` để ghi đè offset thiếu hoặc đã ghi; giá trị ghi đè xuất
  hiện trong Mục 6 của báo cáo chất lượng.

## Bảo vệ log gốc

Bộ xử lý chỉ đọc `data/raw/`. Kiểm tra đầu ra bằng đường dẫn tuyệt đối sau khi
resolve; nếu đầu ra trỏ vào `data/raw/` hoặc thư mục đầu vào, chương trình dừng
với mã thoát khác 0. Hash sai, thiếu manifest hoặc thiếu file log cũng làm
chương trình dừng trước khi tạo đầu ra. Không sửa log gốc để xử lý lỗi.

## Kiểm thử

```bash
python -m pytest analysis/tests -q
```

Test dùng fixture minh họa và bản sao của `evidence/smoke_test/` trong thư mục
tạm. Không có đầu ra test nào được ghi vào `data/processed/` hoặc `results/`
trong repo, và dữ liệu smoke test trong `evidence/` chỉ được đọc.

## Giới hạn đã biết

- Tên file Cowrie sau xoay vòng là `[XM]`; tiếp tục đọc glob `cowrie.json*` và
  sắp file xoay vòng trước file `cowrie.json`.
- Chưa chạy trên log `data/raw/RUN-xx/` thật. Smoke test chỉ dùng để xác nhận
  schema và kiểm thử tích hợp trên bản sao tạm.
- Event tải file và `cowrie.command.failed` không có trong smoke test; các
  trường liên quan cần xác minh thêm trên lượt chạy thật.
- Fixture trong `analysis/tests/fixtures/` là dữ liệu tự soạn, KHÔNG phải log
  thật, chưa đối chiếu Cowrie thật và không dùng trong kết quả.
