# Quy ước ghi nhật ký thử nghiệm H.2 (WP-04)

**Người viết:** TV4 (có AI hỗ trợ) · **Ngày:** 2026-11-11 · **Trạng thái:** bản đề xuất, chờ TV3 review; TV2 **chưa** xem và **chưa** đồng ý

Áp dụng cho `experiments/nhat_ky_thu_nghiem.csv`. Mẫu trống: `experiments/mau_nhat_ky.csv`. Kịch bản: `docs/03_kich_ban_thu_nghiem.md`.

Các quy tắc dưới đây dựa trên mã bộ xử lý của TV2, `analysis/process_run.py` tại commit `9c75ec0` (viết tắt `pr:<dòng>`). Mã đổi thì phải đọc lại quy ước này.

## 1. Cột

Đúng 11 cột, đúng thứ tự, không thêm khoảng trắng:

```csv
run_id,scenario_id,step_no,time_utc_client,may_nguon,ip_nguon,dich_vu_cong,thao_tac,ket_qua_phia_client,nguoi_thuc_hien,ghi_chu
```

Thiếu một cột thì bộ xử lý dừng với lỗi "Nhật ký thiếu cột H.2" (`pr:105–117`, `pr:554–558`).

| Cột | Cách ghi | Ví dụ |
| --- | --- | --- |
| `run_id` | Trùng **đúng** tên thư mục `data/raw/RUN-xx`. Dòng có `run_id` khác bị bỏ qua (`pr:561–562`) | `RUN-01` |
| `scenario_id` | `KB-01`, `KB-02`, `KB-03`, `KB-04`, `KB-05`. Lượt lặp KB-01 từ Host vẫn ghi `KB-01` | `KB-01` |
| `step_no` | Số nguyên: `0` là dòng bắt đầu; `1..n` theo bảng bước trong `docs/03_kich_ban_thu_nghiem.md`; dòng kết thúc là số cuối của bảng | `0` |
| `time_utc_client` | ISO 8601 UTC có `Z`, tới mili giây, lấy bằng đồng hồ máy nguồn **ngay lúc gửi** | `2026-11-11T08:15:02.123Z` |
| `may_nguon` | `VM-A` hoặc `Host` | `VM-A` |
| `ip_nguon` | IP nguồn trong lab | `192.168.239.10` |
| `dich_vu_cong` | `ssh/2222` hoặc `telnet/2223`. Bộ xử lý lấy số cổng ở cuối chuỗi (`pr:542–544`) | `ssh/2222` |
| `thao_tac` | Một nhãn ở bảng dưới, sau dấu `:` là chi tiết (lệnh, mật khẩu giả đã gửi) | `GUI_MAT_KHAU: LabWrong-01` |
| `ket_qua_phia_client` | Điều client thấy, chép ngắn từ transcript | `Permission denied, please try again.` |
| `nguoi_thuc_hien` | `TV4 (AI hỗ trợ)` | `TV4 (AI hỗ trợ)` |
| `ghi_chu` | Tùy chọn; ghi "mật khẩu giả của lab" ở dòng có mật khẩu | |

**Nhãn `thao_tac`** (để bảng đối chiếu đọc được bằng script `experiments/scripts/doi_chieu.py`):

| Nhãn | Dùng khi | Ví dụ |
| --- | --- | --- |
| `BAT_DAU` | Dòng bắt đầu một kịch bản từ một nguồn | `BAT_DAU` |
| `MO_KET_NOI` | Mở kết nối TCP (chạy `ssh`, mở socket Telnet) | `MO_KET_NOI: ssh -v -p 2222 … labuser@192.168.239.20` |
| `GUI_USERNAME` | Gửi username ở `login:` (Telnet) | `GUI_USERNAME: labuser` |
| `GUI_MAT_KHAU` | Gửi một mật khẩu (giả) | `GUI_MAT_KHAU: LabWrong-01` |
| `GO_LENH` | Gõ một lệnh trong shell | `GO_LENH: uname -a` |
| `HUY_DAU_NHAC` | Hủy ở dấu nhắc mật khẩu, không gửi gì (KB-01) | `HUY_DAU_NHAC: Ctrl+C` |
| `CLIENT_TU_NGAT` | Client tự thoát (KB-02 sau 3 lần sai) | `CLIENT_TU_NGAT: sau 3 lần sai` |
| `KET_THUC` | Dòng kết thúc, sau khi phiên đã đóng | `KET_THUC` |

## 2. Định dạng thời gian

- Bộ xử lý đọc giờ bằng `pd.to_datetime(..., utc=True)` (`pr:305–314`). Giờ **không đọc được** thì dòng đó bị **bỏ qua mà không báo** (`pr:563–565`). Vì vậy script tự ghi giờ bằng `datetime.now(timezone.utc)`, không gõ tay.
- Không đổi giờ hệ thống của máy nào.

## 3. Dòng bắt đầu, dòng thao tác, dòng kết thúc

Mỗi lần chạy **một kịch bản từ một nguồn**:

1. Một dòng **bắt đầu** (`step_no=0`, `thao_tac=BAT_DAU`), ghi **trước** khi mở kết nối.
2. Một dòng cho **mỗi thao tác** (mở kết nối, mỗi lần gửi mật khẩu, mỗi lệnh, hủy), ghi **ngay lúc gửi**.
3. Một dòng **kết thúc** (`thao_tac=KET_THUC`), ghi **sau** khi phiên đã đóng (client đã thoát).

KB-02 có hai kết nối nhưng chỉ **một** cặp bắt đầu/kết thúc bao cả hai.

Lý do: bộ xử lý dựng **một cửa sổ** cho mỗi bộ `(scenario_id, ip_nguon, cổng)` từ dòng sớm nhất tới dòng muộn nhất, nới mỗi đầu `|clock_offset_s|` (`pr:595–602`, `pr:616–617`), rồi gán phiên nào **giao** cửa sổ (`pr:618`). Có dòng bắt đầu và kết thúc thì cửa sổ luôn bao trọn phiên, không còn phụ thuộc vào việc phiên mở trễ hơn giờ ghi bao lâu (ISS-01).

Khớp đúng một kịch bản → `matched`; không khớp → `unmatched`; khớp từ hai kịch bản → `ambiguous` (`pr:620–632`). Không có `--logbook` → mọi phiên `unmatched` (`pr:579–585`); có nhật ký nhưng `run_note.txt` thiếu `clock_offset_s` → mọi phiên `needs_review` (`pr:586–593`).

## 4. Khoảng nghỉ giữa hai kịch bản

Bộ xử lý **không** dịch đồng hồ theo dấu của offset, chỉ dùng trị tuyệt đối `|δ|` làm dung sai hai phía (`pr:602`). Phiên của kịch bản trước có thể lệch tới `|δ|` sau dòng kết thúc của nó; cửa sổ kịch bản sau bắt đầu sớm hơn dòng bắt đầu `|δ|`. Để hai cửa sổ cùng nguồn, cùng cổng không chạm phiên của nhau:

```text
nghỉ giữa dòng KET_THUC của kịch bản trước và dòng BAT_DAU của kịch bản sau ≥ max(10 s, 2×|δ| + 2 s)
```

Cặp cần chú ý trong một RUN: KB-01 → KB-02 → KB-03 (cùng VM-A, cùng `ssh/2222`). KB-05 (`telnet/2223`) và KB-01 lặp từ Host (`.1`, `ssh/2222`) khác bộ khóa với nhau và với VM-A, nhưng vẫn giữ khoảng nghỉ cho dễ đọc.

## 5. Độ lệch giờ (`clock_offset_s`)

- `run_note.txt` ghi `clock_offset_s` = δ(VM-A − VM-H), giây, có dấu (`docs/04_hop_dong_du_lieu.md` mục 2). Bộ xử lý tìm chuỗi này bằng regex **không xét ranh giới từ** (`pr:535–537`), nên không thêm khóa nào khác chứa chữ `clock_offset`.
- Bộ xử lý dùng **một** δ cho cả hai nguồn. Lệch của Host so với VM-H ghi riêng trong `experiments/<RUN>/do_lech_gio.md`. Có thể chạy thêm một lần **kiểm độ nhạy** với `--delta-seconds <max |lệch| của hai nguồn>` ra thư mục khác; ghi rõ là bản phụ.
- Nhờ có dòng bắt đầu/kết thúc, phiên vẫn giao cửa sổ nếu thời lượng phiên lớn hơn chênh lệch đồng hồ của nguồn đó. Vì vậy KB-01 nên chờ khoảng 1–2 s ở dấu nhắc mật khẩu trước khi hủy, để phiên không quá ngắn.

## 6. Ghi file

- Ghi bằng module `csv` của Python (quote đúng ô có dấu phẩy), UTF-8, không BOM (bộ xử lý đọc `utf-8-sig` nên có BOM cũng được, `pr:552`).
- `experiments/nhat_ky_thu_nghiem.csv` đã có thì **thêm dòng**, không ghi đè. Không sửa dòng đã ghi để khớp kịch bản; ghi sai thì thêm dòng mới và giải thích ở `ghi_chu`.
- Không ghi bước đối chứng KB-03 trên VM-A thật, phiên chuẩn bị, hay lệnh quản trị vào nhật ký H.2.

## 7. Giới hạn đã biết (ISS-01 chưa đóng)

`review/issues.md` ISS-01 vẫn **Mở**. Dòng bắt đầu/kết thúc giải quyết trường hợp cửa sổ quá hẹp, nhưng **không bảo đảm** mọi ca đều khớp:

- Một δ chung cho hai nguồn: nếu Host lệch VM-H nhiều hơn `|δ|` và phiên rất ngắn, phiên có thể không giao cửa sổ.
- Hai kịch bản cùng `(scenario_id, ip_nguon, cổng)` chạy hai lần trong một RUN sẽ gộp thành một cửa sổ (vì vậy không chạy lại kịch bản trong cùng RUN).
- Khoảng nghỉ quá ngắn giữa hai kịch bản cùng nguồn, cùng cổng sẽ cho `ambiguous`.

Đây là quy ước phía nhật ký của TV4. TV2 chưa xem, chưa đồng ý; quy ước này không sửa thuật toán và không đóng ISS-01.
