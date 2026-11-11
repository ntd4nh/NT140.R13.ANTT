# KHAC – Soạn prompt Claude thực thi công việc TV4

**Ngày:** 2026-11-11 · **Người làm:** TV4 · **Trạng thái:** Xong

Đã soạn prompt chi tiết để Claude thực hiện các việc TV4, gồm chủ động bật lab có sẵn; bỏ tạo slide và thủ tục bàn giao theo yêu cầu trực tiếp của người dùng.

## Đã làm gì

- Đối chiếu phần việc với kế hoạch, tài liệu lab, hợp đồng dữ liệu, code gắn kịch bản và công cụ đếm độc lập.
- Viết quy trình tạo sản phẩm, kiểm chứng và lưu minh chứng cho WP-01, WP-04, WP-06, WP-08, WP-10 và các review TV4; phần WP-11 có điều kiện dữ liệu.
- Bổ sung xử lý đồng hồ của hai nguồn, giới hạn ISS-01, phân biệt banner server/client, tách preflight khỏi RUN và phân biệt kiểm TV4 với kiểm độc lập TV3.

## Kết quả

- Sản phẩm: `Prompt/PROMPT_CLAUDE_THUC_THI_CONG_VIEC_TV4.md`.
- Đã rà soát tính nhất quán bằng đọc nguồn cục bộ và một lượt đọc chéo độc lập; kiểm tra định dạng/diff sau khi tạo.
- Đây là sản phẩm prompt, chưa triển khai các WP hoặc bật/chạy lab trong lượt soạn này. Các thao tác đó là yêu cầu dành cho Claude khi dùng prompt.

## Còn thiếu / vướng mắc

- Khả năng thực thi trên VM còn phụ thuộc công cụ, vị trí VM và quyền của phiên Claude; prompt yêu cầu xác minh thật trước thao tác.

## Liên quan tới người khác

- Bàn giao: bỏ thủ tục theo yêu cầu trực tiếp; không sửa `BAN_GIAO.md`, không gửi yêu cầu, không pull/commit/push.
- Cần review: đây là việc KHAC soạn prompt; không tự ghi các WP hay review thành viên đã hoàn tất.

## Các thành viên khác cần biết

- Prompt cho phép chạy thử nghiệm sau kiểm tra kỹ thuật thực tế đạt trong phạm vi người dùng yêu cầu; không thay xác nhận kiểm độc lập TV3 hoặc nghiệm thu đầy đủ của kế hoạch.
