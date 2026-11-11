# Prompt cho Claude thực thi công việc TV4

Tôi là **TV4 – Thực nghiệm, diễn giải, tổng hợp** của nhóm đồ án NT140.R13.ANTT, đề tài 13: Honeypot thu thập và phân tích hành vi tấn công. Bạn có quyền đọc và chỉnh sửa repo được mở trong phiên này, chạy các kiểm tra cần thiết và vận hành lab sẵn có trong phạm vi nêu dưới đây. Hãy **trực tiếp thực hiện công việc**, tạo sản phẩm, chạy kiểm chứng và lưu minh chứng; tiếp tục qua các bước đủ điều kiện, không chỉ đưa kế hoạch rồi dừng.

## 1. Phạm vi thực hiện và chỉ dẫn ưu tiên

- Repo dự kiến: `D:\Study\HK5\ATM\NT140.R13.ANTT`. Kiểm tra thư mục làm việc thực tế trước khi thao tác. Tôi đã xác nhận là TV4, không hỏi lại vai trò.
- Thực hiện WP-01 phần TV4, WP-04, review ghi chú deception, lặp một phép đối chiếu smoke test, thực nghiệm WP-06, diễn giải WP-08 và ghép **báo cáo Markdown** WP-10. Phần behavior/IOC/ATT&CK chỉ thực hiện tới mức dữ liệu cho phép.
- **Phần cần lab trên máy TV1: chủ động tìm và bật VM-H, VM-A rồi làm luôn**, nếu các VM và quyền truy cập có sẵn trên máy đang điều khiển. Việc bật hai VM hiện có và chạy các tương tác lab được mô tả ở đây đã được tôi yêu cầu; không dừng chỉ để hỏi lại việc này.
- **Bỏ phần tạo slide và thủ tục bàn giao trong lượt này.** Không tạo/sửa slide, không cập nhật `BAN_GIAO.md`, không đổi trạng thái BG, không soạn/gửi yêu cầu bàn giao, không tạo Issue/PR hoặc nhắn thành viên. Không tự `git pull`, commit, push hay merge. Chỉ dẫn này ghi đè các bước thủ tục bàn giao tương ứng trong hướng dẫn repo cho phạm vi lượt này.
- Vẫn viết báo cáo công việc theo `docs/bao_cao_cong_viec/README.md`. Giữ những quy định còn lại của repo, đặc biệt cách ly và tính trung thực của kết quả.
- Không ghi nhận đã có xác nhận/review của TV1, TV2, TV3 nếu thực tế chưa có. Công việc bạn làm trong phiên này được ghi là TV4 thực hiện với hỗ trợ AI.
- Không làm lại hệ thống từ đầu, dựng honeypot thứ hai, thay kiến trúc, nâng phiên bản Cowrie hoặc mở rộng phạm vi ngoài các việc đã nêu.
- Không ghi đè thay đổi đang có của người dùng. Không sửa lịch sử báo cáo cũ hoặc phần do thành viên khác viết chỉ để đồng nhất trạng thái. Nếu cần hiệu chỉnh, ưu tiên ghi nhận trong sản phẩm mới và chỉ sửa phần liên quan trực tiếp tới TV4.
- Gặp trở ngại ở một bước: lưu nguyên nhân và bằng chứng, tiếp tục các bước độc lập. Chỉ hỏi thông tin không thể tự tìm, chẳng hạn vị trí VM hoặc quyền đăng nhập thực sự còn thiếu. Không giả định có quyền điều khiển máy khác chỉ vì repo gọi đó là “máy TV1”.

## 2. Đọc nguồn và xác minh hiện trạng

Trước khi sửa, đọc `AGENTS.md`, `CLAUDE.md`, trạng thái Git và các nguồn sau:

1. `Project.md`, `Plan/TOM_TAT_KE_HOACH.md`.
2. `Plan/KE_HOACH_BAO_CAO_TIEN_DO_HONEYPOT.md`: mục A, E.4, F.4, F.6, H.1–H.9, I.1 và G.4.
3. `docs/01_quyet_dinh_pham_vi_cong_cu.md`, `docs/02_so_do_lab.md`, `docs/04_hop_dong_du_lieu.md`.
4. `docs/00_nguyen_ly_deception_telemetry.md`.
5. `Implement/lab/README_chay_lab.md`, `Implement/lab/cowrie/README.md`, `Implement/lab/cowrie/cowrie.cfg`.
6. `evidence/smoke_test/README.md`, các log và `SHA256SUMS`; `evidence/kiem_tra_cach_ly_TV1.md`, `review/kiem_tra_cach_ly.md`.
7. `analysis/README.md`, `analysis/process_run.py`, các test/fixture cần đối chiếu.
8. `review/issues.md`, hai bản review TV1/TV2 của TV3 và các script trong `review/tai_hien/`.
9. `report/TV1_lab.md`, `report/TV3_review_deception.md`, phần viết TV2 nếu hiện đã có.
10. `docs/bao_cao_cong_viec/README.md` và các báo cáo mới liên quan.

Các thông tin dưới đây chỉ là điểm xuất phát, phải đối chiếu lại với repo và máy thực tế:

| Thành phần | Thông số đã ghi nhận |
| --- | --- |
| VM-H | `192.168.239.20`, Cowrie 3.1.6, SSH giả 2222, Telnet giả 2223 |
| VM-A | `192.168.239.10`, nguồn thử nghiệm thứ nhất và máy đối chứng |
| Windows host | `192.168.239.1`, nguồn thứ hai và máy quản trị |
| Mạng | VMware host-only VMnet1, subnet `192.168.239.0/24` |
| SSH quản trị thật | Cổng 22, chỉ từ host; tách với SSH honeypot 2222 |
| Backend | `shell`, user chạy Cowrie không phải root; forwarding tắt |

Không suy luận “mọi người đã xong” từ bản tóm tắt cũ. Một số tài liệu kế hoạch vẫn có chỗ trống và trạng thái lịch sử. Nếu có mâu thuẫn, ghi rõ nguồn, thời điểm và mức xác minh; không tự biến “đã gửi” thành “đã review”, “tự kiểm” thành “kiểm độc lập”. Không tuyên bố đã đọc PDF slide khi chỉ có bản tổng hợp.

## 3. WP-01: chốt câu hỏi và phạm vi TV4

Điền mục 1 của `docs/01_quyet_dinh_pham_vi_cong_cu.md`, khoảng nửa trang, gồm:

- **Q1:** Với kết nối, đăng nhập, lệnh và tải tệp có kiểm soát, Cowrie ghi nhận được những gì? Thao tác/phản hồi nào cho thấy giới hạn hoặc điểm lộ của shell giả?
- **Q2:** Có dựng lại và đối chiếu được diễn biến từng phiên với nhật ký thực nghiệm về nguồn, dịch vụ, thứ tự thao tác và thời gian không?
- **Q3:** Từ dữ liệu đã thu, có thể mô tả những nhóm hành vi và observable nào; tới đâu thì đủ căn cứ để đề xuất mapping ATT&CK?
- Trong phạm vi: một Cowrie ở chế độ shell, SSH/Telnet, hai nguồn lab, tương tác có kiểm soát, log gốc bảo toàn, xử lý và báo cáo có thể kiểm tra lại.
- Ngoài phạm vi: Internet/public deployment, malware thật, SIEM, cloud trả phí, AI/ML, proxy tới hệ điều hành thật.
- Tách phạm vi báo cáo tiến độ và đích đến toàn đề tài. Không gọi việc điền văn bản là đã có thực nghiệm hoặc cả nhóm đã phê duyệt.

Có thể chỉnh câu chữ cho đo lường được, nhưng giữ đúng mục tiêu đề tài. Chỉ cập nhật mô tả trạng thái liên quan tới phần TV4 vừa thực hiện, giữ nguyên nội dung kỹ thuật của các thành viên khác nếu không cần sửa.

## 4. WP-04: kịch bản, credential giả và mẫu nhật ký

Tạo hoặc hoàn thiện:

- `docs/03_kich_ban_thu_nghiem.md`.
- `experiments/mau_nhat_ky.csv`.
- `experiments/quy_uoc_nhat_ky.md` nếu cần giải thích cách ghi thời gian và xử lý ISS-01.

Mỗi kịch bản phải có: mục tiêu, nguồn/đích, tiền điều kiện, bước thao tác và lệnh cụ thể theo đúng môi trường, sự kiện mong đợi cho từng bước, trường cần đối chiếu, đơn vị đếm, minh chứng cần lưu và tiêu chí đạt/không đạt. “Mong đợi” phải tách khỏi “thực tế”. Bước không sinh sự kiện riêng thì ghi rõ cách kiểm chứng khác; không tự bịa event.

### Credential

Chọn danh sách hoàn toàn giả, cụ thể và nhất quán, có thể giữ tài khoản tạm `labuser` / `LabOnly-2026` để giảm thay đổi:

- KB-02: cùng username `labuser`, năm mật khẩu sai phân biệt `LabWrong-01` tới `LabWrong-05`, rồi mật khẩu đúng `LabOnly-2026`.
- KB-05: cùng username, hai mật khẩu sai `TelnetWrong-01`, `TelnetWrong-02`, rồi mật khẩu đúng như trên.
- Dòng chấp nhận dự kiến: `labuser:x:LabOnly-2026`.

Ghi đầy đủ từng cặp sai/đúng trong kịch bản, cùng nội dung `userdb` cần có. Kiểm tra auth backend, file và quy tắc thực tế để xác nhận các cặp còn lại bị từ chối; không suy diễn chỉ từ việc một cặp vắng mặt trong tài liệu. Không dùng wildcard chấp nhận tất cả. Khi vận hành lab, lưu bản cấu hình cũ rồi áp dụng danh sách giả này nếu cần, kiểm tra bằng một phiên chuẩn bị riêng trước RUN; không tính các lần thử chuẩn bị vào RUN-01. Không đọc/lưu mật khẩu thật của thành viên vào sản phẩm.

### Kịch bản cơ bản

1. **KB-01, VM-A → VM-H/2222:** mở SSH, tới bước hỏi mật khẩu thì hủy, không gửi credential. Kiểm `session.connect`, sự kiện bắt tay SSH thực sự có và `session.closed`; đối chiếu không có login. Sau đó lặp cùng kịch bản từ Windows host, ghi rõ nguồn thứ hai.
2. **KB-02, VM-A → VM-H/2222:** buộc password bằng `-o PubkeyAuthentication=no -o PreferredAuthentications=password`; kiểm soát `NumberOfPasswordPrompts` phù hợp. Kết nối thứ nhất thử sai 3 lần; kết nối thứ hai thử sai 2 lần rồi đúng 1 lần và `exit`. Tổng mục tiêu là 5 login failed và 1 login success trong **hai phiên**, không phải một phiên. Xác minh số lần thử bằng log thật, không chỉ theo số lần gọi client. Nếu giới hạn client/server khác dự kiến, điều chỉnh cách chạy có ghi nhận trước lượt đo chính thức.
3. **KB-03, VM-A → VM-H/2222:** dùng kết nối riêng, đăng nhập đúng và chạy lần lượt: `whoami`, `id`, `uname -a`, `pwd`, `ls -la`, `cat /etc/passwd`, `ps aux`, `ifconfig`, `ssh -V`, `nt140_cmd_khong_ton_tai`, `exit`. Nếu buộc thay `ifconfig` bằng lệnh khác thì chốt và dùng cùng danh sách cho cả honeypot lẫn VM-A đối chứng. Đối chiếu mỗi `command.input`, sự kiện `command.failed` nếu thực sự phát sinh, TTY và đóng phiên. Không coi không có `command.failed` là bằng chứng lệnh đã được thực thi thành công trên hệ điều hành thật.
4. **KB-05, Windows host → VM-H/2223:** Telnet, hai credential sai rồi một credential đúng, sau đó `whoami`, `uname -a`, `exit`. Dùng Telnet client hiện có hoặc công cụ tương đương có ghi transcript; không tự giả định Python hiện tại còn `telnetlib`. Kiểm protocol, nguồn, login, lệnh và đóng phiên. Lượt lặp KB-01 qua SSH từ host là phiên riêng.

`ssh -V` ở KB-03 phải được gõ **bên trong shell Cowrie**. Đầu ra thường ở stderr nên transcript phải giữ cả stdout/stderr. Phiên bản **server banner** phải lấy từ bắt tay/cấu hình server có căn cứ; `cowrie.client.version` là phiên bản client, không dùng nó thay server banner. Nếu kiểm được L3, đối chiếu banner 9.2p1 và output 7.9p1 bằng bằng chứng thực tế, không chỉ chép giá trị dự kiến.

### KB-04 nâng cao

Chỉ sau khi kịch bản cơ bản và kiểm tra cách ly đạt: tạo một tệp văn bản vô hại trên VM-A, tính SHA-256 trước, phục vụ nội bộ ở cổng 8000 rồi tải từ shell Cowrie. Tuyệt đối không dùng mẫu malware hoặc URL Internet.

Firewall hiện có thể chặn cả kết nối tới VM-A. Nếu cần, chỉ thêm ngoại lệ tối thiểu tới **VM-A:8000** cho thử nghiệm này, ghi lại và hoàn nguyên sau đó; không tắt firewall hay mở chiều ra toàn subnet/Internet. Không thực hiện nếu không xác minh được ngoại lệ vẫn bảo toàn cách ly. Tách riêng lượt nâng cao, không trộn vào RUN cơ bản. Đối chiếu `file_download`/`file_download.failed`, URL, SHA-256 thật và access log của server; thất bại cũng là kết quả cần ghi đúng.

### Nhật ký H.2 và ISS-01

Giữ **đúng 11 tên cột**, không thêm khoảng trắng vào tên cột hoặc tự đổi schema:

```csv
run_id,scenario_id,step_no,time_utc_client,may_nguon,ip_nguon,dich_vu_cong,thao_tac,ket_qua_phia_client,nguoi_thuc_hien,ghi_chu
```

- Mẫu CSV có thể chỉ có header; không đặt thời gian/kết quả giả vào nhật ký thật. Ví dụ nếu có phải để file riêng ghi nhãn `minh_hoa`.
- Mỗi lần thực hiện kịch bản/nguồn phải có dòng bắt đầu **trước khi kết nối**, dòng cho từng thao tác và dòng kết thúc **sau khi đóng phiên**; dùng UTC có độ chính xác phù hợp. Kịch bản KB-02 bao quát cả hai kết nối.
- `run_id` phải trùng tên thư mục lượt chạy; `dich_vu_cong` dùng `ssh/2222` hoặc `telnet/2223`; xử lý CSV bằng thư viện để quote dấu phẩy đúng.
- Kiểm tra code hiện tại trước khi chốt cách ghi: `_attach_scenarios` đang dùng `abs(clock_offset)` mở rộng khoảng min/max thời gian nhật ký và kiểm giao khoảng với phiên; nó **không dịch đồng hồ theo dấu offset**. Không đánh đồng offset đồng hồ, sai số đo và độ trễ thao tác.
- Đo độ lệch cho **cả VM-A và Windows host** so với VM-H. Nếu hợp đồng/code chỉ có một offset cho cả lượt, ghi riêng phép đo từng nguồn và nêu giới hạn; không tự nhét một giá trị có ý nghĩa khác vào `clock_offset_s`.
- Không tăng `--delta-seconds` tùy tiện chỉ để mọi phiên thành `matched`; không tự đặt offset bằng 0 khi chưa đo. Nhật ký có đầu/cuối giải quyết cửa sổ quá hẹp nhưng không bảo đảm mọi ca đều khớp.
- Ghi giải pháp quy ước phía TV4, kiểm bằng dữ liệu có thật; không tự ghi TV2 đã đồng ý và không đóng ISS-01 thay người review. Không sửa thuật toán TV2 trong lượt này; nếu cần sửa, ghi rõ vấn đề và căn cứ trong báo cáo kỹ thuật.

## 5. Tìm, bật và kiểm tra lab thực tế

Chủ động thực hiện phần này bằng các công cụ thật có trong phiên, thay vì mặc định đợi TV1:

1. Kiểm tra VMware/`vmrun`, danh sách VM đang chạy, inventory/cấu hình VM đã đăng ký và vị trí `.vmx`. Tìm có giới hạn theo hướng dẫn lab và thư mục VM hợp lý; không quét nội dung bí mật hay toàn bộ đĩa vô mục đích. Xác định đúng VM-H và VM-A, không bật nhầm VM chỉ vì tên tương tự.
2. Trước khi bật VM-H, kiểm tra cấu hình mạng VM không gắn NAT/Bridged và khớp thiết kế host-only. Nếu cấu hình sai, sửa tối thiểu trên đúng VM trong trạng thái thích hợp, giữ bản cấu hình trước thay đổi. Không thay toàn bộ mạng của host. Không nối Internet để tiện cài gói.
3. Bật VM-H, VM-A nếu đang tắt; nếu đã chạy thì dùng trạng thái hiện có. Dùng CLI/native app được hỗ trợ, đợi có kiểm tra trạng thái và giới hạn thời gian. Nếu dùng helper nền thì chạy ẩn trừ khi cần người dùng thao tác trực tiếp.
4. Xác nhận IP thật, tuyến mạng, trạng thái firewall, user chạy Cowrie, backend shell, forwarding tắt, output ngoài tắt, cổng quản trị tách khỏi honeypot và các tính năng chia sẻ host đã tắt. Đọc trạng thái hiện tại, không dùng biên bản ngày trước thay kiểm tra mới.
5. Chạy kiểm tra cách ly theo các phép thử trong `review/kiem_tra_cach_ly.md`, có timeout và lưu lệnh, output, exit code, giờ UTC. Kiểm từ VM-H và shell giả; dùng log thật để đánh giá tải tệp, không tin riêng chuỗi “connected” giả. Không thực thi nội dung tệp tải về.
6. Kết quả an toàn phải có căn cứ về **mạng + firewall + phép thử kết nối**, không chỉ ping thất bại. Nếu có đường Internet hoặc phạm vi chặn không bảo đảm: dừng tương tác, dừng Cowrie/VM-H theo cách phù hợp, giữ minh chứng, ghi lỗi và chỉ tiếp tục phần repo độc lập.

Lưu phép kiểm do mình thực hiện ở `evidence/kiem_tra_cach_ly_TV4/` và ghi nhận riêng, **không điền vào biên bản mang tên TV3 hoặc tự ký xác nhận TV1**. Tôi yêu cầu bỏ thủ tục bàn giao và chủ động vận hành lab: nếu kiểm tra kỹ thuật hiện tại đạt, tiếp tục thực nghiệm trong phạm vi lab đã cho phép; vẫn ghi rõ kiểm độc lập/tiêu chí nghiệm thu của TV3 chưa được hoàn tất nếu thực tế chưa có. Không vì đã chạy thử mà tuyên bố WP-03/WP-09 đã nghiệm thu đầy đủ.

Nếu không tìm thấy VM hoặc không thể truy cập máy TV1 từ phiên hiện tại, nêu đúng lỗi/khả năng thiếu và thông tin tối thiểu cần người dùng cung cấp. Không tự mở đường truy cập từ Internet, đổi sang Bridged hay cài dịch vụ điều khiển từ xa. Vẫn hoàn thành toàn bộ sản phẩm không phụ thuộc lab.

## 6. Review deception và lặp phép đối chiếu smoke test

### Review ghi chú TV3

Tạo `review/review_TV4_WP-13_deception.md`:

- Kiểm từng loại telemetry và tham chiếu `file:dòng` với log thật, đọc cả ngữ cảnh phiên.
- Kiểm các điểm lộ L1–L8: căn cứ cấu hình, log/TTY, quan sát được người khác ghi lại hay còn dự kiến. Không nâng mức bằng chứng nếu chưa tái hiện.
- Kiểm các khẳng định quá rộng, chẳng hạn mọi tương tác đều độc hại, luôn ít báo động giả, hoặc mồi giống thật chắc chắn làm attacker ở lại lâu. Tách cơ chế/giả thuyết với kết quả đã đo; dữ liệu lab không chứng minh ý định attacker.
- Chỉ ra câu sai, căn cứ, ảnh hưởng và đề nghị sửa; kết luận đạt/đạt có lưu ý/chưa đạt theo phần thực sự đã kiểm. Không tự nhận đã diff gói Cowrie chính thức nếu chỉ đọc báo cáo TV3.
- Đây là review ghi chú và quan sát ban đầu; không đồng nhất với việc đã có O7 đối chứng từ RUN-01.

### Lặp phép đếm độc lập

1. Tạo bản sao `evidence/smoke_test/` trong thư mục tạm riêng, không sửa bản gốc hoặc tạo RUN-01 bằng log cũ.
2. Kiểm manifest và hash; chạy CLI hiện có của TV2 trên bản sao, chỉ rõ `--data-origin lab` nếu nằm ngoài quy ước `data/raw/`, chỉ định đầu ra tạm ngoài thư mục đầu vào.
3. Chạy:

```text
python -I review/tai_hien/dem_doc_lap.py <thu_muc_ban_sao_smoke> <thu_muc_dau_ra_bo_xu_ly>
```

4. Đối chiếu kết quả thật với mốc tham chiếu: 58 sự kiện, 8 phiên, 4 lần đăng nhập sai, 4 lần đúng, 8 `command.input`; công cụ in `KHỚP` và trả mã 0 khi khớp. Nếu lệch, lưu kết quả và tìm nguyên nhân, không sửa log hoặc công cụ chỉ để đạt mốc.
5. Lưu lệnh, phiên bản môi trường cần thiết, output và nhận xét vào `review/review_TV4_doi_chieu_smoke.md`; minh chứng máy đọc được có thể để `evidence/doi_chieu_smoke_TV4/`.

Kết luận phải gọi đúng là **TV4 lặp phép đối chiếu trên smoke test**. Không gọi đây là RUN-TEST độc lập mới hoặc toàn bộ WP-09 đã hoàn thành. Các số tham chiếu trên không phải mục tiêu ép cho RUN-01.

## 7. WP-06: chạy thực nghiệm và bảo toàn dữ liệu

Sau khi chuẩn bị và kiểm tra kỹ thuật ở trên đạt, chạy thực nghiệm thật:

1. Xác nhận thư mục RUN dự kiến chưa có dữ liệu. Nếu RUN-01 đã tồn tại, không ghi đè; chọn mã mới theo quy ước, dùng nhất quán trong mọi file.
2. Tách log kiểm cổng, preflight, kiểm credential và kiểm cách ly khỏi lượt thực nghiệm. Dùng cơ chế lưu/rotate log có kiểm soát, giữ nguyên log cũ; **không xóa/truncate log để làm đẹp số liệu**. Nếu có log ngoài kịch bản trong tập thu được, giữ bản gốc và giải thích trong dữ liệu dẫn xuất.
3. Ghi giờ UTC của VM-A, VM-H và Windows host trước/sau lượt, phép đo offset có dấu, sai số/độ phân giải và cách đo. Dùng `date -u` trên Linux, UTC tương ứng trên Windows. Không thay đổi thời gian máy để ép log khớp.
4. Chạy tuần tự KB-01 → KB-02 → KB-03 từ VM-A; KB-05 rồi lặp KB-01 từ host. Tách các cửa sổ kịch bản, lưu transcript client gồm output lỗi, điền nhật ký **ngay khi chạy**. Nếu tự động hóa, bảo đảm đúng số lần nhập/số kết nối; dùng công cụ có sẵn, không mở NAT để cài thêm.
5. Chạy đối chứng KB-03 trên VM-A thật: cùng danh sách và thứ tự lệnh, trong terminal/subshell dành riêng để `exit` không kết thúc phiên điều khiển ngoài ý muốn. Lưu hai transcript ở `experiments/transcript/<RUN>/`, ghi rõ đâu là honeypot, đâu là máy thật, cùng ngữ cảnh môi trường. Không chỉnh transcript để hai bản giống nhau.
6. Xuất log nguyên vẹn từ VM-H qua đường quản trị được phép vào `data/raw/<RUN>/`: mọi `cowrie.json*` thuộc lượt, các TTY liên quan và tệp vô hại cần đối chiếu nếu có. Không lọc/sửa nội dung raw. File nào chỉ là bản trích thì phải ghi là bản trích và giữ nguồn nguyên vẹn.
7. Tạo `run_note.txt` theo hợp đồng hiện có, tối thiểu `start_utc`, `end_utc`, `clock_offset_s`, `cowrie_version`, `config_version`; bổ sung nguồn đo offset từng máy trong ghi chú/phụ lục riêng khi cần. Cấu hình chưa commit thì dùng định danh/hash có thật, không bịa mã commit.
8. Tạo `SHA256SUMS` sau khi hoàn tất bộ file, gồm các file cần bảo toàn trừ chính manifest; kiểm lại hash sau sao chép. Không sửa raw sau khi chốt manifest.
9. Lưu nhật ký ở `experiments/nhat_ky_thu_nghiem.csv` theo H.2. Tạo `experiments/doi_chieu_<RUN>.csv`: mỗi dòng liên hệ bước nhật ký với session, thời gian, loại sự kiện và `raw_ref=file:dòng`, trạng thái đối chiếu, lý do nếu không có sự kiện, bằng chứng transcript nếu cần. Một bước có thể tương ứng nhiều sự kiện; không ép quan hệ một-một.
10. Mọi thao tác có sự kiện phải khớp nguồn, cổng, phiên và khoảng thời gian có căn cứ. Giữ nguyên các trường hợp không khớp/mơ hồ để review; giải thích thao tác không được log hỗ trợ. Thu thập thành công không đồng nghĩa “tấn công thành công”.

Nếu một lượt chạy sai thao tác, giữ bằng chứng, ghi là lượt thử chưa đạt và dùng lượt tiếp theo; không sửa nhật ký/log để biến nó thành đúng kịch bản. Kết thúc thì đóng client và server HTTP tạm, hoàn nguyên ngoại lệ firewall nâng cao, đưa Cowrie/lab về trạng thái kiểm soát được và ghi trạng thái cuối.

## 8. WP-08: xử lý và diễn giải bằng số liệu thật

Đọc lại CLI và hợp đồng trước khi chạy. Lệnh cơ sở, thay `<RUN>` bằng mã thật:

```text
python -m analysis.process_run --run-dir data/raw/<RUN> --logbook experiments/nhat_ky_thu_nghiem.csv
```

- Kiểm hash trước/sau, báo cáo chất lượng, số dòng, trường thiếu, sự kiện lạ, bản trùng và trạng thái `matched/unmatched/ambiguous/needs_review`. Không coi CSV có dữ liệu là đã đối chiếu đầy đủ.
- Đầu ra hiện có là `events.csv`, `sessions.csv`, `bao_cao_chat_luong.txt`; không mặc định CLI đã sinh O1–O7/biểu đồ. Không lấy hash TTY làm hash tệp tải, không lấy `log.closed.duration_ms` thay thời lượng phiên.
- Dùng bảng thật TV2 đã có nếu sẵn. Nếu O1/O4/O6 chưa có, có thể tạo **bảng dẫn xuất phục vụ phần đối chiếu/diễn giải của TV4** bằng đoạn xử lý riêng, đọc từ CSV hiện có; ghi người tạo, công thức và nguồn rõ ràng, không nhận đó là sản phẩm TV2 đã nộp. Không sửa bộ xử lý lõi TV2. Nếu thêm script, đặt tên thể hiện phạm vi TV4 và giữ chạy lại được.
- O1: một dòng/phiên, nguồn/dịch vụ/kịch bản, bắt đầu/kết thúc, thời lượng, số login sai/đúng, số lệnh.
- O4: timeline một phiên KB-03 thực tế, thứ tự sự kiện, `raw_ref`, thời gian UTC và tương đối từ kết nối. Quy tắc xử lý thời điểm bằng nhau phải xác định được.
- O6: ma trận nguồn × dịch vụ, tách số phiên và số lần đăng nhập, không cộng hai đơn vị thành một chỉ số.
- Kiểm ít nhất các tổng và một phiên tiêu biểu bằng phép tính độc lập, lưu chênh lệch nếu có. Không ép công cụ đếm smoke vốn đơn giản phải tương đương mọi quy tắc khử trùng của pipeline trên RUN mới.

Viết `results/<RUN>/nhan_xet.md`, gồm 3–5 nhận xét. Mỗi nhận xét theo cấu trúc: **quan sát → số liệu/sự kiện và đường dẫn → ý nghĩa trong phạm vi câu hỏi → giới hạn/giải thích khác**. Nêu cỡ mẫu, tương tác do nhóm tạo, shell giả lập, nguồn thời gian, trạng thái gắn kịch bản và phần chưa quan sát được. Không gọi IP lab là IOC độc hại, không suy rộng thành xu hướng attacker Internet, không dùng số liệu fixture minh họa làm kết quả.

Nếu lab chưa chạy được hoặc dữ liệu không đủ, không tạo nhận xét thực nghiệm giả. Chỉ tạo khung có nhãn dự kiến và ghi rõ bằng chứng còn thiếu.

## 9. WP-10: ghép báo cáo tiến độ Markdown

Tạo/hoàn thiện `report/bao_cao_tien_do.md`, dựa trên sản phẩm hiện có và kết quả thật vừa làm. Dùng 7 phần của I.1, nhưng viết thành báo cáo, **không làm slide**:

1. Đề tài, deception, Q1–Q3 và phạm vi.
2. Nhóm đã làm được tới đâu: bảng theo mẫu B.3 và đóng góp thực tế theo B.5.
3. Thiết kế và lựa chọn công cụ; trạng thái cách ly/tái lập.
4. Thu thập và xử lý: nhật ký → log → CSV → kiểm chứng.
5. Kết quả sơ bộ và giới hạn; phân biệt smoke test với RUN mới.
6. Còn thiếu, lỗi, ảnh hưởng và hướng xử lý.
7. Dự định tiếp theo và phân công.

- Phần tiến độ luôn trước dự định tiếp theo. Đặt các bảng B.3/B.5 cập nhật trong báo cáo mới; không viết lại bảng lịch sử trong bản kế hoạch để tạo cảm giác nhóm đã đạt từ trước.
- Đọc kỹ 5 lưu ý ghép báo cáo của TV3. Nếu lượt này có kiểm tra TV4 và RUN mới, cập nhật trung thực, vẫn tách kiểm độc lập TV3/dựng lại lab chưa làm. Không gắn nhãn lab đạt đầy đủ tiêu chí cơ bản nếu chưa đủ nghiệm thu của kế hoạch.
- Tổng hợp phần TV1, TV3 và TV2 nếu có. Thiếu phần TV2 thì dùng nguồn code/minh chứng đã kiểm với ghi chú nguồn, không viết thay dưới danh nghĩa TV2 hoặc bịa đóng góp/nhận xét đã được TV2 xác nhận.
- Mọi khẳng định “đã làm” phải có đường dẫn minh chứng. Không tự tính phần trăm hoàn thành, gán lịch ngày/tuần hoặc tự thêm deadline.

## 10. Behavior, observable và ATT&CK: chỉ tới mức đã có căn cứ

Sau phần cơ bản, kiểm dữ liệu có cho phép làm thêm WP-11 không. Nếu có, tạo bảng quy tắc B1–B5, `results/<RUN>/behavior.csv`, bảng observable/IOC có ngữ cảnh và `results/attack_mapping.md` hoặc đường dẫn đúng quy ước hiện có:

- Nhãn theo phiên có thể nhiều nhãn; định nghĩa ngưỡng và bằng chứng. Phiên không đăng nhập chỉ được gắn nhãn phù hợp khi có đủ dữ liệu mở/đóng, không suy từ log bị thiếu.
- So nhãn với kịch bản chỉ là kiểm tra trên các tình huống đã biết; không gọi đó là đánh giá độc lập hay hiệu quả phát hiện ngoài thực tế. Không tự tạo lượt hỗn hợp rồi nói TV3 đã thực hiện.
- Observable lab như IP, credential giả, URL/hash tệp vô hại phải ghi đúng tính chất; không đánh giá độc hại khi thiếu căn cứ.
- Mỗi mapping ghi hành vi, `raw_ref`, technique/sub-technique, tactic, phiên bản ATT&CK, nguồn chính thức và giới hạn. Năm mật khẩu sai cùng username có thể là căn cứ mô phỏng password guessing; không từ một kết nối đơn lẻ kết luận quét mạng.
- Kiểm phiên bản/ID/tactic trên nguồn MITRE chính thức khi cần dùng; repo dự kiến v20 nhưng không sao chép máy móc một tên tactic hoặc thông tin phiên bản chưa xác minh. Nếu không truy cập được, ghi “ứng viên/chưa xác minh”, không công bố mapping đã kiểm.
- Tra cứu ngoài chỉ trên môi trường quản trị được phép, **không bật Internet cho VM lab**. WP-12/báo cáo cuối kỳ hoặc mở rộng chưa có điều kiện thì ghi dự kiến, không tuyên bố hoàn thành đồ án.

## 11. Kiểm chứng, báo cáo công việc và trả kết quả

- Sau mỗi gói việc thực sự hoàn thành, ghi báo cáo ngắn theo mẫu repo: `YYYY-MM-DD_TV4_WP-xx_ten-ngan.md`; dùng ngày thực tế, không ghi đè báo cáo cũ. Việc ngoài WP dùng `KHAC`.
- Giữ thông tin đã chạy trong lượt này tách với kết quả người khác từng ghi. Lưu lệnh, exit code và output cần thiết để kiểm tra lại; không ghi bí mật quản trị.
- Kiểm tên cột CSV, UTF-8, đường dẫn tham chiếu, hash raw, số liệu tổng/đơn vị đếm, cách chạy lại và diff cuối. Chạy các kiểm tra hiện có phù hợp; nếu có sửa logic xử lý phụ trợ thì kiểm các trường hợp ảnh hưởng. Không chạy thử hàng loạt không liên quan chỉ để tăng số kiểm tra.
- Thực hiện các bước kiểm chứng bằng công cụ thật; không viết “đã kiểm” cho lệnh mới chỉ đề xuất. Không xóa dữ liệu để làm sạch Git. Không commit/push hoặc thực hiện thủ tục bàn giao.
- Kết thúc trả lời ngắn gọn bằng bảng: **hạng mục | trạng thái thực tế | sản phẩm/minh chứng | giới hạn/bước còn lại**. Liệt kê file tạo/sửa, lệnh kiểm tra chính và kết quả; cho biết VM nào đã được bật, có chạy RUN thật không, mã RUN, số liệu thật và trạng thái lab cuối phiên.
- Nếu chưa thể hoàn tất vì thiếu môi trường/quyền/dữ liệu, nêu đúng điểm dừng và thông tin tối thiểu cần bổ sung. Không dùng các từ “xong toàn bộ”, “an toàn”, “đạt nghiệm thu” vượt quá bằng chứng.

**Bắt đầu bằng kiểm tra repo và công cụ hiện có, sau đó thực thi liên tục các phần đủ điều kiện theo thứ tự trên.**
