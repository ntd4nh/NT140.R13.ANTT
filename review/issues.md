# Danh sách lỗi (TV3)

Mức độ: **Chặn** (không dùng được kết quả) · **Trung bình** (kết quả dùng được nhưng tốn công sửa tay hoặc dễ hiểu sai) · **Thấp** (tài liệu, trình bày).
Trạng thái: `Mở` → người xây sửa → `Chờ kiểm lại` → TV3 kiểm lại → `Đóng`.

Thư mục tái hiện dùng chung: `review/tai_hien/`. Bản sao smoke test tạo như sau (chạy ở gốc repo, Git Bash):

```bash
mkdir -p /tmp/tv3/RUN-SMOKE
cp -r evidence/smoke_test/{cowrie.json,cowrie.log,tty,SHA256SUMS} /tmp/tv3/RUN-SMOKE/
```

| Mã | Mức | Người sửa | Sản phẩm | Tóm tắt | Trạng thái |
| --- | --- | --- | --- | --- | --- |
| ISS-01 | Trung bình | TV2 (+ TV4 cho nhật ký) | `analysis/process_run.py` | Kịch bản chỉ có một dòng nhật ký không khớp được phiên khi δ nhỏ | Mở |
| ISS-02 | Thấp | TV2 | `analysis/process_run.py` | Báo cáo chất lượng tính phiên chỉ dò cổng là "thiếu trường bắt buộc" | Mở |
| ISS-03 | Thấp | TV2 | `docs/04_hop_dong_du_lieu.md` | Trạng thái BG-05 trong hợp đồng lỗi thời | Mở |
| ISS-04 | Thấp | TV1 | `docs/02_so_do_lab.md`, `docs/01_quyet_dinh_pham_vi_cong_cu.md` | Còn chỗ trống và ghi chú "[cần xem trên máy thật]" đã có câu trả lời | TV1 đã sửa, chờ TV3 kiểm lại |

---

## ISS-01 – Kịch bản một dòng nhật ký không khớp được phiên

- **Mức:** Trung bình. Lỗi an toàn (không gán sai kịch bản), nhưng sẽ đẩy nhiều phiên RUN-01 sang review tay.
- **Vị trí:** `analysis/process_run.py`, hàm `_attach_scenarios` (khoảng dòng 595–619).
- **Bước tái hiện:**
  ```bash
  python -m analysis.process_run --run-dir /tmp/tv3/RUN-SMOKE --data-origin lab \
    --out-processed /tmp/tv3/outL --logbook review/tai_hien/nhat_ky_smoke_tv3.csv --delta-seconds 0.5
  cut -d, -f1,3,4,6,7,9 /tmp/tv3/outL/sessions.csv
  ```
  `nhat_ky_smoke_tv3.csv` ghi đúng 6 thao tác và giờ trong bảng "Đã làm gì" của `evidence/smoke_test/README.md` (giờ đến giây, mỗi thao tác một dòng). δ = 0,5 s phù hợp với "lệch dưới 1 giây" trong README đó.
- **Mong đợi:** 6 phiên đăng nhập đều `matched` đúng kịch bản; 2 phiên chỉ dò cổng (`3f8ff8b71f88`, `0722a6a2bff3`) `unmatched` vì nhật ký không có dòng cho chúng.
- **Thực tế:** 2 phiên Telnet `e02625c405d3` (bắt đầu 14:47:49.819) và `d976c4e34a27` (14:48:13.604) bị `unmatched`. Với `--delta-seconds 1.0` thì cả 6 phiên khớp.
- **Nguyên nhân:** cửa sổ khớp là `[giờ dòng đầu − δ, giờ dòng cuối + δ]`. Kịch bản chỉ có một dòng thì cửa sổ rộng 2δ quanh một thời điểm. Giờ client ghi đến giây và kết nối luôn mở **sau** thời điểm ghi, nên phiên bắt đầu trễ hơn δ là trượt. δ là độ lệch đồng hồ, không bao gồm độ trễ thao tác.
- **Gợi ý (người xây quyết định):** thêm một khoảng dung sai thao tác riêng, ghi vào báo cáo chất lượng; hoặc thống nhất với TV4 là nhật ký H.2 phải có dòng bắt đầu và dòng kết thúc cho mỗi kịch bản. Sau khi sửa cần thêm test cho trường hợp này.

## ISS-02 – Phiên chỉ dò cổng bị tính là thiếu trường bắt buộc

- **Mức:** Thấp.
- **Bước tái hiện:**
  ```bash
  python -m analysis.process_run --run-dir /tmp/tv3/RUN-SMOKE --data-origin lab --out-processed /tmp/tv3/out1
  sed -n '/^4\./,/^5\./p' /tmp/tv3/out1/bao_cao_chat_luong.txt
  ```
- **Mong đợi:** người đọc báo cáo biết đây là hệ quả bình thường của thao tác dò cổng (KB-01), không phải mất dữ liệu.
- **Thực tế:** mục 4 ghi `cowrie.client.version.version: 1`. Đó là `json:3` của phiên `3f8ff8b71f88`: client mở cổng 2222 rồi đóng, không gửi chuỗi phiên bản; `cowrie.log` ghi `Bad protocol version identification: b''`. Hành vi đúng theo hợp đồng mục 7 (chuỗi rỗng là thiếu), nhưng báo cáo không phân biệt với trường hợp mất dữ liệu thật.
- **Gợi ý:** tách dòng riêng trong báo cáo, ví dụ "client.version rỗng ở phiên không bắt tay SSH (n_events ≤ 3, không có kex)", hoặc ghi chú trong hợp đồng mục 7.

## ISS-03 – Trạng thái BG-05 trong hợp đồng lỗi thời

- **Mức:** Thấp.
- **Bước tái hiện:** mở `docs/04_hop_dong_du_lieu.md`, dòng 3 và mục 11.
- **Mong đợi:** khớp `BAN_GIAO.md` (BG-05 `Đã gửi`, TV3 đã review: `review/review_TV2_WP-05_WP-07.md`).
- **Thực tế:** dòng 3 ghi "BG-05 chưa gửi"; mục 11 ghi trạng thái "Chưa – chờ TV3 review" và điều kiện "TV3 đã review", trong khi bảng A của `BAN_GIAO.md` đã tách review khỏi điều kiện bàn giao.

## ISS-04 – Tài liệu lab còn chỗ trống đã có câu trả lời

- **Mức:** Thấp.
- **Thực tế và mong đợi:**
  - `docs/02_so_do_lab.md` mục 1 còn `VMware Workstation <phiên bản>`; mục 8 đã ghi 25H2.
  - `docs/01_quyet_dinh_pham_vi_cong_cu.md` mục 3.5 còn hai ghi chú "[cần xem trên máy thật]". Cả hai đã có câu trả lời: chỉ `[output_jsonlog]` được bật trong `cowrie.cfg` (các mục `enabled = true` duy nhất là `[ssh]`, `[telnet]`, `[output_jsonlog]`), và `[ssh] forwarding = false` (`cowrie.cfg:813`).
