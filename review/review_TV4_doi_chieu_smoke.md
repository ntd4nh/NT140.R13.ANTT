# TV4 lặp phép đối chiếu trên log smoke test

**Người làm:** TV4, có AI hỗ trợ · **Ngày:** 2026-11-11 · **Đối tượng:** phép đối chiếu của TV3 trong `review/review_TV2_WP-05_WP-07.md` mục 1 và `report/TV3_review_deception.md` phần 4
**Kết luận:** **Khớp.** Trên máy khác (máy TV4), với pandas 3.1.1, bộ xử lý và phép đếm độc lập cho đúng các số TV3 báo cáo. Đây không phải RUN-TEST và không phải hoàn thành WP-09.

Minh chứng: `evidence/doi_chieu_smoke_TV4/` (lệnh, output, báo cáo chất lượng, `sessions.csv`).

## 1. Kết quả

| Chỉ số | Mốc tham chiếu (TV3) | Phép đếm độc lập (`dem_doc_lap.py`) | Bộ xử lý (`events.csv`, `sessions.csv`, báo cáo chất lượng) | Khớp |
| --- | --- | --- | --- | --- |
| Sự kiện | 58 | 58 | 58 dòng `events.csv`; "Sự kiện giữ: 58" | ✅ |
| Phiên | 8 | 8 | 8 dòng `sessions.csv` | ✅ |
| Lần đăng nhập thất bại / thành công | 4 / 4 | 4 / 4 | "Lần đăng nhập giữ: 8" | ✅ |
| `command.input` | 8 | 8 | – | ✅ |
| `command.failed` | – | 0 | – | – |
| So từng `raw_ref` và từng phiên (số sự kiện, đăng nhập, danh sách lệnh, `duration_ms`, IP, giao thức) | KHỚP | `KHỚP`, mã thoát 0 | | ✅ |
| Hash log gốc trước và sau | OK | Bản sao: 3/3 OK trước khi chạy; `evidence/smoke_test`: 3/3 OK sau khi chạy; `git status --short evidence/` không có thay đổi ở `evidence/smoke_test/` | | ✅ |

Báo cáo chất lượng (`evidence/doi_chieu_smoke_TV4/bao_cao_chat_luong.txt`): 58 dòng vật lý, 58 JSON hợp lệ, 0 hỏng, 0 trùng, 0 event lạ; 45 sự kiện phân tích + 13 sự kiện phụ; mục 4 có `cowrie.client.version.version: 1` (đúng ISS-02 của TV3: phiên chỉ dò cổng `json:3`); 8 phiên `unmatched` vì không truyền `--logbook`.

## 2. Ghi chú phát sinh

1. **pytest trên máy TV4: 13 passed, 2 failed.** Hai test lỗi (`test_processor_fixture_and_does_not_change_raw`, `test_outputs_are_reproducible`) dừng vì `SHA256SUMS` của fixture minh họa `analysis/tests/fixtures/minh_hoa_RUN-TEST/` không khớp.
   - Nguyên nhân đã kiểm: fixture trên cây làm việc là LF (`git ls-files --eol`: `i/lf w/lf`), không có thuộc tính `-text`; manifest fixture trùng đúng hash của bản **CRLF** (đổi `\n` → `\r\n` rồi băm thì ra đúng `5874a14c…f007` và `854b23a9…9353`).
   - Xuất `git archive HEAD` ra thư mục tạm (Git đổi fixture sang CRLF theo `core.autocrlf=true`) rồi chạy lại: **15 passed**.
   - Kết luận: test phụ thuộc kiểu xuống dòng của máy checkout, không phải lỗi của bộ xử lý. Phép đối chiếu trên smoke test không bị ảnh hưởng vì `evidence/**` có `-text`.
   - Đề nghị (TV2 quyết định, TV4 không sửa): thêm `analysis/tests/fixtures/** -text` vào `.gitattributes`, hoặc để test tự sinh manifest cho fixture như đã làm với bản sao smoke test.
2. **Phiên bản pandas.** `analysis/requirements.txt` chỉ ghi `pandas>=2.0.0`; máy TV4 cài được pandas 3.1.1 (bản chính mới). Kết quả trên smoke test vẫn khớp. TV3 không ghi phiên bản pandas đã dùng, nên chưa so được byte giữa hai máy.
3. **Mẫu nhật ký WP-04 được bộ xử lý chấp nhận.** Chạy thêm với `--logbook experiments/mau_nhat_ky.csv` (chỉ có header) ra thư mục tạm khác: mã thoát 0, không báo thiếu cột; 8 phiên `needs_review` vì bản sao smoke test không có `run_note.txt` (đúng `analysis/process_run.py` dòng 586–593). Lần chạy này chỉ để kiểm header, không phải kết quả.

## 3. Giới hạn

- Chỉ lặp trên log smoke test (58 dòng, không theo kịch bản). Chưa kiểm phần gắn kịch bản trên log thật.
- Phép đếm độc lập là script của TV3; TV4 chạy lại, không viết script đếm riêng.
