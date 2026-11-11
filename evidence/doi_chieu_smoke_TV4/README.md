# TV4 lặp phép đối chiếu trên log smoke test

**Người chạy:** TV4, có AI hỗ trợ · **Ngày:** 2026-11-11, 11:00:10–11:00:11 UTC · **Máy:** máy host của TV4 (Windows 11, Git Bash)

Đây **không phải** RUN-TEST và **không phải** hoàn thành WP-09. Chỉ là lặp lại phép đối chiếu của TV3 trên bản sao log smoke test, theo kế hoạch E.4 (WP-09: "TV4 lặp lại một phép đối chiếu"). Kết quả và nhận xét: `review/review_TV4_doi_chieu_smoke.md`.

## Môi trường

| Thành phần | Phiên bản |
| --- | --- |
| Bộ xử lý `analysis.process_run` | `.venv` ở gốc repo: Python 3.11.9, pandas 3.1.1, numpy 2.4.6 (cài từ `analysis/requirements.txt`) |
| Phép đếm độc lập `review/tai_hien/dem_doc_lap.py` | Python 3.11.9 của hệ thống, chạy `python -I` (chỉ thư viện chuẩn) |
| Mã nguồn | nhánh `tv4` @ `9c75ec0` |

## File trong thư mục

| File | Nội dung |
| --- | --- |
| `output_lenh.txt` | Lệnh và output nguyên văn, có mã thoát. Đường dẫn thư mục tạm (ngoài repo, có tên user máy) đã thay bằng `<TMP>`; không đổi gì khác |
| `bao_cao_chat_luong.txt` | Báo cáo chất lượng do bộ xử lý sinh ra, chép nguyên từ `<TMP>/out-smoke/` |
| `sessions.csv` | `sessions.csv` do bộ xử lý sinh ra, chép nguyên từ `<TMP>/out-smoke/` |

SHA-256 của đầu ra trong thư mục tạm: `events.csv` `2ee65aa0…ca0b`, `sessions.csv` `a7ba3574…9915` (đầy đủ trong nhật ký vận hành).

## Lệnh (Git Bash, gốc repo)

```bash
mkdir -p <TMP>/RUN-SMOKE
# Chỉ chép 4 mục có trong manifest; không chép README.md (file ngoài manifest làm bộ xử lý dừng)
cp -r evidence/smoke_test/{cowrie.json,cowrie.log,tty,SHA256SUMS} <TMP>/RUN-SMOKE/
(cd <TMP>/RUN-SMOKE && sha256sum -c SHA256SUMS)
.venv/Scripts/python.exe -m analysis.process_run --run-dir <TMP>/RUN-SMOKE --data-origin lab --out-processed <TMP>/out-smoke
python -I review/tai_hien/dem_doc_lap.py <TMP>/RUN-SMOKE <TMP>/out-smoke; echo "exit=$?"
(cd evidence/smoke_test && sha256sum -c SHA256SUMS); git status --short evidence/
```
