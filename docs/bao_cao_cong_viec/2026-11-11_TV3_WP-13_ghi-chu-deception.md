# WP-13 – Ghi chú deception, yếu tố mồi, điểm lộ ban đầu (TV3)

**Ngày:** 2026-11-11 · **Người làm:** TV3 · **Trạng thái:** Xong một phần

Đã có ghi chú nguyên lý deception và telemetry; mỗi loại telemetry trỏ tới dòng log thật của smoke test. Bảng điểm lộ đầy đủ (O7) còn chờ RUN-01 và transcript KB-03.

## Đã làm gì
- Viết `docs/00_nguyen_ly_deception_telemetry.md`: deception là gì, ba mức tương tác và đánh đổi, bảng "tương tác → sự kiện Cowrie → dòng log thật".
- Nhận BG-08 và kiểm lại danh sách yếu tố mồi của TV1: so `cowrie.cfg` với file mặc định trong gói Cowrie 3.1.6 chính thức, giải mã file TTY của smoke test.
- Lập bảng điểm lộ ban đầu (8 dòng), ghi rõ dòng nào đã kiểm, dòng nào chỉ là quan sát của TV1, dòng nào dự kiến.

## Kết quả
- Sản phẩm: `docs/00_nguyen_ly_deception_telemetry.md`
- Đã kiểm tra bằng cách: `pip download cowrie==3.1.6 --no-deps` rồi `diff` file `cowrie.cfg.dist` với `Implement/lab/cowrie/cowrie.cfg` → chỉ khác dòng 813 (`forwarding`) và 873 (Telnet). Giải mã `evidence/smoke_test/tty/317e…b964` → thấy lời chào Debian, dấu nhắc `labuser@svr04:~$`.

## Còn thiếu / vướng mắc
- `cowrie.command.failed` và `cowrie.session.file_download*` chưa có trong log của repo; ghi "dự kiến", kiểm ở KB-03/KB-04.
- Bảng điểm lộ từ dữ liệu thật (`results/RUN-xx/diem_lo.md`) chờ RUN-01 và BG-07 (transcript KB-03 + kết quả chạy cùng lệnh trên VM-A).

## Liên quan tới người khác
- Bàn giao: nhận BG-08 (TV1 → TV3): đã nhận.
- Cần review: TV4 review ghi chú; TV1 kiểm tra mục 4 (yếu tố mồi).

## Các thành viên khác cần biết
- Cấu hình honeypot đang **trùng hoàn toàn bản mặc định công khai** (trừ `userdb`), nên tên máy `svr04`, banner và kernel đều đoán trước được. Đây là điểm lộ lớn nhất; nếu nhóm đổi mồi thì phải ghi `config_version` mới trong `run_note.txt`.
- TV4: khi chạy KB-03 nên thêm `ssh -V` vào danh sách lệnh để ghi được điểm lộ L3 vào log.
