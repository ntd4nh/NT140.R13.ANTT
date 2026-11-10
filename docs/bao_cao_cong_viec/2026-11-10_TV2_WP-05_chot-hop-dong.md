# WP-05 – Chốt đề xuất hợp đồng dữ liệu (TV2)

**Ngày:** 2026-11-10 · **Người làm:** TV2 · **Trạng thái:** Xong một phần

Đã tự kiểm và nhận BG-02; hợp đồng dữ liệu đã đối chiếu smoke test, hiện là bản chốt đề xuất chờ TV3 review.

## Đã làm gì
- Tạo branch `tv2-wp05-contract-close`; nhận BG-02 trong commit riêng `edfdc71` (`ban-giao: nhận BG-02`).
- Đối chiếu 58 dòng `cowrie.json`: 58 JSON hợp lệ, 0 dòng hỏng; `sha256sum -c SHA256SUMS` trả `OK` cho `cowrie.json`, `cowrie.log` và file trong `tty/`.
- Kiểm tra phiên connect/closed ghép theo session:

  | Nguồn | SSH | Telnet |
  |---|---:|---:|
  | `192.168.239.10` | 3/3 phiên đóng | 2/2 phiên đóng |
  | `192.168.239.1` | 2/2 phiên đóng | 1/1 phiên đóng |

- Cập nhật hợp đồng từ bằng chứng trong `evidence/xac_minh_hop_dong_du_lieu.md` và tự kiểm log; không sửa bất kỳ file nào trong `evidence/`.

## Kết quả và lý do thay đổi

| Thay đổi | Lý do |
|---|---|
| Đổi trạng thái đầu tài liệu sang “BẢN CHỐT ĐỀ XUẤT”, chờ TV3 review; cập nhật BG-05 nhưng giữ trạng thái “Chưa” | Đã nhận BG-02 và đối chiếu log; chưa có review TV3 |
| Ghi kết quả các câu a–j và căn cứ file:dòng; chỉ giữ `[XM]` cho tên file xoay vòng và `url` của `file_download.failed` | Smoke test xác nhận các trường chung, giao thức, kiểu password/duration và timestamp; không chạy qua nửa đêm, không có event `file_download.failed` |
| Thêm bảng phân loại event: 11 event phân tích, 4 event phụ đã biết, còn lại là event lạ; event phụ được giữ với trường chung, event lạ ghi lỗi và loại đến khi review | Tránh nhầm event phụ Cowrie thành event lạ; thống nhất allowlist cho bộ xử lý |
| Bổ sung `uuid` vào trường bỏ qua; duration phiên chỉ lấy từ `session.closed`; ghi quy tắc `command_supported=unknown` cả khi shell giả báo lỗi tùy chọn; chuỗi rỗng `client_version` là thiếu | Theo bằng chứng smoke test và các đề xuất TV1 |
| Xác nhận `run_note.txt` một dòng, gồm UTC, offset có dấu, phiên bản Cowrie/cấu hình | TV1 đã đồng ý định dạng này |
| Giữ nguyên `docs/01_quyet_dinh_pham_vi_cong_cu.md` | Phần “trường dữ liệu chờ TV2 xác nhận” còn treo; đề nghị TV1 cập nhật sau khi TV3 review hợp đồng |

## Điều kiện BG-05
- **Đạt:** quy định nơi nhận log `data/raw/RUN-xx/`, bảo toàn raw, kiểm hash, múi giờ UTC và cách xử lý trường thiếu đã có trong hợp đồng.
- **Đạt một phần:** các trường chung và trường của event xuất hiện trong smoke test đã được kiểm trực tiếp; file `cowrie.json*` sau xoay vòng và `url` của `cowrie.session.file_download.failed` chưa xác minh. Các event tải file không xuất hiện trong smoke test.
- **Chưa đạt:** TV3 chưa review hợp đồng theo checklist. Vì vậy BG-05 vẫn **Chưa**, chưa gửi bàn giao cho TV1.

## [REVIEW] soạn sẵn – chưa gửi

```text
[REVIEW] Hợp đồng dữ liệu A→B (WP-05)
Người làm: TV2 → Người review: TV3
Vị trí: docs/04_hop_dong_du_lieu.md @ branch tv2-wp05-contract-close (phần hợp đồng chưa commit)
Cần kiểm tra theo checklist RV-MÃ-XỬ-LÝ và RV-CẤU-HÌNH (kế hoạch mục F.6)

RV-MÃ-XỬ-LÝ:
- Có thể chạy lại trên máy khác cho cùng kết quả.
- Không ghi vào raw; múi giờ UTC đúng; trường thiếu xử lý theo hợp đồng; số dòng khớp.

RV-CẤU-HÌNH:
- Thay đổi so với mặc định được liệt kê và có lý do.
- Bản đưa lên kho chung đã bỏ thông tin nhạy cảm; README làm lại được.
```

## Còn thiếu / liên quan tới người khác
- TV3 review để hoàn thành BG-05; yêu cầu review ở trên chỉ được soạn, chưa gửi.
- Đề nghị TV1 cập nhật trạng thái “trường dữ liệu chờ TV2 xác nhận” trong `docs/01_quyet_dinh_pham_vi_cong_cu.md` sau review.
- Hợp đồng chưa commit; commit riêng duy nhất trong lượt này là nhận BG-02 (`edfdc71`). Không chạy quy trình kết thúc Prompt 8.
