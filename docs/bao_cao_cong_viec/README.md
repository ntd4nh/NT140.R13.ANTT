# Báo cáo công việc

Mỗi lần làm xong một việc, người làm (hoặc AI agent của họ) viết một báo cáo ngắn ở thư mục này, để các thành viên khác đọc trong khoảng 2 phút là nắm được.

## Đặt tên file

```text
YYYY-MM-DD_TVx_WP-xx_ten-ngan.md
```

Ví dụ: `2026-11-10_TV1_WP-03_cai-cowrie.md`. Ngày đặt đầu tên để các file tự xếp theo thứ tự thời gian. Việc không thuộc gói việc nào thì thay `WP-xx` bằng `KHAC`.

## Cách viết

- **Ngắn:** tối đa khoảng 1 trang.
- **Viết cho người không làm phần này:** câu ngắn, giải thích thuật ngữ nếu cần.
- **Kết quả trước:** câu đầu tiên nói việc đã xong chưa và được gì.
- **Chỉ ghi việc đã làm thật, có minh chứng.** Việc chưa làm thì ghi "dự kiến".
- **Không dán log dài:** trỏ tới file trong repo.
- **Không ghi** mật khẩu thật, khóa SSH hay thông tin máy cá nhân.

## Mẫu

Sao chép khung dưới đây vào file mới rồi điền.

```markdown
# WP-xx – <tên việc> (TVx)

**Ngày:** YYYY-MM-DD · **Người làm:** TVx (<tên>) · **Trạng thái:** Xong / Xong một phần / Bị chặn

<Một câu tóm tắt: đã xong chưa, được gì.>

## Đã làm gì
- <2–4 ý ngắn>

## Kết quả
- Sản phẩm: <đường dẫn file trong repo, mã commit>
- Đã kiểm tra bằng cách: <lệnh / thao tác> → <kết quả>

## Còn thiếu / vướng mắc
- <nếu không có, ghi "Không">

## Liên quan tới người khác
- Bàn giao: <BG-xx → TVy: đã gửi / chưa đủ điều kiện vì ...>
- Cần review: <TVy>

## Các thành viên khác cần biết
- <1–2 điều quan trọng nhất>
```
