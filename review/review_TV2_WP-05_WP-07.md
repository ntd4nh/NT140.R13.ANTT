# Review sản phẩm của TV2: WP-05 (hợp đồng dữ liệu), WP-07 (bộ xử lý)

**Người review:** TV3 · **Ngày:** 2026-11-11 · **Commit được review:** `cec6308`
**Máy chạy lại:** máy TV3, Windows 11, Python 3.11.9, pandas cài từ `analysis/requirements.txt` (TV2 dùng máy khác)
**Kết luận:** **Đạt, không có lỗi mức chặn.** 1 lỗi mức trung bình (ISS-01), 2 lỗi mức thấp (ISS-02, ISS-03). Chưa có log RUN thật nên chưa kiểm được phần gắn kịch bản trên dữ liệu thật.

## 1. RV-MÃ-XỬ-LÝ

| Mục kiểm | Kết quả | Căn cứ |
| --- | --- | --- |
| Test của TV2 chạy được trên máy khác | ✅ | `python -m pytest analysis/tests -q` → `15 passed` |
| Chạy một lệnh mỗi lượt | ✅ | `python -m analysis.process_run --run-dir <bản sao smoke test> --data-origin lab --out-processed <thư mục tạm>` → mã thoát 0, sinh 3 file |
| Chạy lại cho cùng kết quả | ✅ | Chạy 2 lần vào 2 thư mục: `diff -r` không khác byte nào |
| Số dòng khớp, khớp phép đếm độc lập | ✅ | `review/tai_hien/dem_doc_lap.py` (chỉ dùng thư viện chuẩn, không dùng mã `analysis/`): 58 sự kiện, 8 phiên, 4 đăng nhập thất bại, 4 thành công, 8 lệnh. So từng `raw_ref` trong `events.csv` và từng phiên trong `sessions.csv` (số sự kiện, đăng nhập, danh sách lệnh theo thứ tự, `duration_ms`, IP, giao thức): **KHỚP** |
| Không ghi vào `raw/` | ✅ | Trỏ `--out-processed` vào thư mục lượt chạy → dừng, mã thoát 2. `git status` sạch sau mọi lần chạy; `sha256sum -c` của bản sao vẫn OK |
| Kiểm tra hash trước khi xử lý | ✅ | Thiếu một file trong manifest, hoặc sửa một byte của `cowrie.json` → dừng, mã thoát 2, không tạo đầu ra |
| Múi giờ đúng | ✅ | `event_time_utc` giữ nguyên giá trị `Z` của Cowrie (ví dụ `2026-11-10T14:47:23.158579Z`); parse bằng `pd.to_datetime(..., utc=True)` |
| Xử lý trường thiếu, lỗi theo hợp đồng | ✅ | Bộ dữ liệu biên tự tạo (nhãn minh họa, không lưu vào repo): tách smoke test thành `cowrie.json.2026-11-09` + `cowrie.json`, thêm 1 dòng JSON hỏng, 1 dòng trùng, 1 eventid lạ. Báo cáo chất lượng ghi đúng `file:dòng` cho cả ba; file xoay vòng được đọc trước; bản trùng và event lạ bị loại khỏi `events.csv` |
| Gắn kịch bản theo nhật ký | ⚠️ | Thử với nhật ký dựng từ bảng giờ trong `evidence/smoke_test/README.md`: δ=0,5 s → 2 phiên Telnet `unmatched`; δ=1,0 s → khớp đủ. Xem **ISS-01** |
| Báo cáo chất lượng dễ hiểu đúng | ⚠️ | Phiên chỉ dò cổng bị tính là thiếu trường. Xem **ISS-02** |

## 2. Review hợp đồng dữ liệu (WP-05)

| Mục kiểm | Kết quả | Căn cứ |
| --- | --- | --- |
| Tên trường đối chiếu với log thật | ✅ | TV3 kiểm lại trên `evidence/smoke_test/cowrie.json`: các trích dẫn `json:3,4,7,8,9,14,15,16,17,18,20,23` đúng loại sự kiện ghi trong hợp đồng |
| Quy định nơi chuyển log, giữ log gốc | ✅ | Mục 2 (cấu trúc `data/raw/RUN-xx/`, `SHA256SUMS`, `run_note.txt`) |
| Múi giờ UTC | ✅ | Mục 8 |
| Xử lý trường thiếu, lỗi | ✅ | Mục 7, đã kiểm bằng chạy thật ở trên |
| Phần chưa xác minh được đánh dấu | ✅ | `[XM]` cho tên file xoay vòng và `url` của `file_download.failed` |
| Phân biệt đơn vị đếm sự kiện / đăng nhập / phiên | ✅ | Mục 1; báo cáo chất lượng in cả ba |
| Trạng thái trong tài liệu khớp `BAN_GIAO.md` | ⚠️ | Xem **ISS-03** |

## 3. Việc TV3 còn làm với phần của TV2

- WP-09: khi có lab, tự chạy `RUN-TEST` và lặp lại toàn bộ bảng 1 trên log thật, kèm nhật ký thật.
- Kiểm lại ISS-01 đến ISS-03 sau khi TV2 sửa.
