# Hướng dẫn dựng lab Honeypot từ con số 0 (WP-03)

Hướng dẫn này viết cho người **chưa từng dựng máy ảo hay server**. Làm đúng thứ tự từ Bước 1 tới Bước 16, không nhảy bước. Mỗi bước có ba phần: **Làm**, **Bạn sẽ thấy** (để biết mình làm đúng), **Nếu lỗi**.

Thiết kế lab xem `docs/02_so_do_lab.md`. Gặp lỗi không có trong hướng dẫn: chụp màn hình hoặc copy nguyên văn thông báo lỗi, gửi cho nhóm hoặc hỏi AI agent.

---

## Phần A – Hiểu nhanh trước khi làm

### Mình sắp dựng cái gì?

Trên máy Windows của bạn, ta tạo **2 máy ảo** chạy Linux:

| Tên | Vai trò | Địa chỉ IP |
| --- | --- | --- |
| **VM-H** | Máy honeypot: chạy Cowrie, giả làm server SSH/Telnet để ghi lại mọi thứ người khác làm với nó | `<SUBNET>.20` |
| **VM-A** | Máy "người thử" số 1: dùng để kết nối vào honeypot | `<SUBNET>.10` |
| **Máy Windows của bạn** | Máy "người thử" số 2, đồng thời là máy quản trị | `<SUBNET>.1` |

Ba máy nối với nhau bằng một mạng ảo riêng tên **VMnet1**. Mạng này **không ra được Internet**, nên honeypot không thể gây hại ra bên ngoài.

### Giải thích từ ngữ

| Từ | Nghĩa |
| --- | --- |
| **Máy ảo (VM)** | Một "máy tính giả" chạy bên trong máy thật, do VMware tạo ra |
| **Host** | Máy thật của bạn (Windows) |
| **File ISO** | File chứa bộ cài hệ điều hành, giống đĩa cài |
| **Terminal** | Cửa sổ gõ lệnh bằng chữ |
| **PowerShell** | Terminal của Windows. Mở: bấm phím Windows, gõ `PowerShell`, Enter |
| **SSH** | Cách điều khiển một máy khác qua mạng bằng terminal |
| **IP** | Địa chỉ của máy trong mạng, dạng `192.168.150.20` |
| **Cổng (port)** | "Cửa" của một dịch vụ trên máy. SSH thật dùng cổng 22; honeypot dùng 2222 (SSH giả) và 2223 (Telnet giả) |
| **sudo** | Chạy lệnh với quyền quản trị; Linux sẽ hỏi mật khẩu của bạn |

### Cách đọc lệnh trong hướng dẫn

- Khung có chữ `bash` ở đầu: gõ trong **Linux** (trong VM, hoặc qua SSH vào VM).
- Khung có chữ `powershell` ở đầu: gõ trong **PowerShell trên Windows**.
- Dòng bắt đầu bằng `#` là ghi chú, không cần gõ.
- Chữ trong `<...>` phải **thay bằng giá trị của bạn**. Ví dụ `<SUBNET>.20` thành `192.168.150.20`.
- **Gõ mật khẩu trong Linux sẽ không hiện ký tự nào, kể cả dấu `*`.** Cứ gõ bình thường rồi Enter.

### Mật khẩu sẽ dùng

| Tài khoản | Dùng ở đâu | Gợi ý |
| --- | --- | --- |
| `labadmin` | Đăng nhập quản trị vào VM-H và VM-A | Tự đặt, **không dùng lại mật khẩu thật** của bạn |
| `labuser` | Tài khoản giả trên honeypot | Mật khẩu giả, ví dụ `LabOnly-2026` |

Ghi mật khẩu ở chỗ riêng của bạn, **không ghi vào repo**.

---

## Phần B – Chuẩn bị

- [ ] **VMware Workstation** đã cài. Mở được là được.
- [ ] **Git for Windows** đã cài (để có Git Bash). Kiểm tra: bấm phím Windows, gõ `Git Bash`, thấy là có.
- [ ] Đã **clone repo** của nhóm về máy và mở được bằng VS Code.
- [ ] Còn trống ít nhất **40 GB** ổ đĩa.
- [ ] Tải file cài **Ubuntu Server 24.04 LTS**: vào https://ubuntu.com/download/server, bấm nút tải bản **24.04 LTS**. Được một file `.iso` khoảng 2–3 GB. Nhớ nơi lưu file.

---

## Bước 1 – Xem dải IP của mạng lab (VMnet1)

**Làm:**
1. Mở VMware Workstation.
2. Menu **Edit → Virtual Network Editor**.
3. Nếu thấy nút **Change Settings** ở góc dưới thì bấm vào (cần quyền admin), rồi bấm **Yes**.
4. Trong danh sách, chọn dòng **VMnet1**, cột Type là **Host-only**.
5. Nhìn ô **Subnet IP** ở phía dưới, ví dụ `192.168.150.0`.

**Bạn sẽ thấy:** một địa chỉ dạng `192.168.x.0`. **Ba số đầu chính là `<SUBNET>`.** Ví dụ Subnet IP là `192.168.150.0` thì `<SUBNET>` là `192.168.150`.

Ghi lại `<SUBNET>` vào bảng ở Bước 16. Từ đây:
- VM-H sẽ dùng `<SUBNET>.20`;
- VM-A sẽ dùng `<SUBNET>.10`;
- máy Windows là `<SUBNET>.1`.

**Nếu lỗi:**
- Không có VMnet1: bấm **Add Network** → chọn **VMnet1** → OK → chọn Type **Host-only** → **Apply**.
- Đóng cửa sổ bằng **OK**.

---

## Bước 2 – Tạo máy ảo VM-H

**Làm:**
1. Trong VMware: **File → New Virtual Machine**.
2. Chọn **Typical (recommended)** → **Next**.
3. Chọn **I will install the operating system later** → **Next**.
   *(Không chọn file ISO ở bước này, để VMware không tự cài theo kiểu tự động.)*
4. Guest operating system: chọn **Linux**. Version: chọn **Ubuntu 64-bit** → **Next**.
5. Virtual machine name: gõ `VM-H`. Location: để mặc định → **Next**.
6. Maximum disk size: gõ `20` (GB). Chọn **Store virtual disk as a single file** → **Next**.
7. Bấm **Customize Hardware...**:
   - **Memory:** `2048` MB.
   - **Processors:** Number of processors `1`, Number of cores per processor `2`.
   - **New CD/DVD (SATA):** bên phải chọn **Use ISO image file** → **Browse...** → chọn file Ubuntu `.iso` đã tải. Tick **Connect at power on**.
   - **Network Adapter:** chọn **NAT**.
     *(NAT cho VM ra Internet tạm thời để tải phần mềm. Bước 9 sẽ đổi sang VMnet1.)*
   - Bấm **Close**.
8. Bấm **Finish**.

**Bạn sẽ thấy:** VM-H xuất hiện trong danh sách bên trái của VMware.

---

## Bước 3 – Cài Ubuntu Server lên VM-H

Trình cài Ubuntu Server **không dùng chuột**. Dùng các phím:
- **Mũi tên lên/xuống** hoặc **Tab** để di chuyển;
- **Enter** để chọn;
- **Space (phím cách)** để tick ô vuông.

Để gõ vào màn hình VM, **bấm chuột vào trong màn hình VM**. Muốn đưa chuột ra lại Windows, bấm **Ctrl + Alt**.

**Làm:** chọn VM-H → bấm **Power on this virtual machine**, rồi đi lần lượt qua các màn hình:

| # | Màn hình | Làm gì |
| --- | --- | --- |
| 1 | Menu đen có dòng **Try or Install Ubuntu Server** | Nhấn **Enter** (hoặc chờ vài giây) |
| 2 | **Select your language** | Chọn **English** → Enter |
| 3 | **Installer update available** (nếu có) | Chọn **Continue without updating** |
| 4 | **Keyboard configuration** | Để **English (US)** → xuống **[ Done ]** → Enter |
| 5 | **Choose the type of installation** | Để **Ubuntu Server** (có dấu `(X)`) → **[ Done ]** |
| 6 | **Network configuration** | Thấy card mạng (thường là `ens33`) có dòng `DHCPv4` và một IP → **[ Done ]** |
| 7 | **Proxy configuration** | Để trống → **[ Done ]** |
| 8 | **Ubuntu archive mirror configuration** | Chờ kiểm tra xong → **[ Done ]** |
| 9 | **Guided storage configuration** | Để mặc định **Use an entire disk** → **[ Done ]** |
| 10 | **Storage configuration** (tóm tắt) | **[ Done ]** → hỏi **Confirm destructive action** → chọn **[ Continue ]**. *(Chỉ xóa ổ đĩa ảo 20 GB vừa tạo, không đụng tới máy thật.)* |
| 11 | **Profile configuration** | **Your name:** `Lab Admin` · **Your server's name:** `vm-h` · **Pick a username:** `labadmin` · **Choose a password** và **Confirm** → **[ Done ]** |
| 12 | **Upgrade to Ubuntu Pro** | Chọn **Skip for now** → **[ Continue ]** |
| 13 | **SSH configuration** | Di chuyển tới **Install OpenSSH server**, nhấn **Space** để có dấu `[X]` → **[ Done ]**. **Bước này quan trọng:** thiếu nó thì không điều khiển VM từ Windows được |
| 14 | **Featured server snaps** | Không chọn gì → **[ Done ]** |
| 15 | Màn hình cài đặt chạy chữ | Chờ tới khi hiện **Installation complete!** |
| 16 | | Chọn **[ Reboot Now ]** |
| 17 | Nếu hiện **Please remove the installation medium, then press ENTER** | Nhấn **Enter** |

**Bạn sẽ thấy:** sau khi khởi động lại, màn hình đen có dòng `vm-h login:`.

**Nếu lỗi:**
- VMware báo **Intel VT-x / AMD-V is disabled**: tắt máy, vào BIOS, bật mục *Virtualization Technology* (Intel VT-x hoặc AMD SVM), rồi lưu.
- Bị kẹt ở màn hình 8 quá lâu: chờ thêm. Vẫn kẹt thì kiểm tra máy Windows có Internet không.

---

## Bước 4 – Đăng nhập và điều khiển VM-H từ Windows

Màn hình VM của Ubuntu Server **không dán được lệnh** từ Windows. Vì vậy ta dùng SSH từ PowerShell: trong PowerShell thì copy-paste thoải mái.

**Làm:**
1. Ở màn hình VM: gõ `labadmin` → Enter → gõ mật khẩu → Enter.
2. Gõ lệnh sau rồi Enter để xem IP hiện tại:

```bash
ip -br a
```

3. **Bạn sẽ thấy** dạng:

```text
lo     UNKNOWN  127.0.0.1/8 ::1/128
ens33  UP       192.168.200.135/24 ...
```

   Số `192.168.200.135` (của bạn sẽ khác) là IP tạm thời của VM-H trên mạng NAT. Ghi lại.

4. Trên Windows, mở **PowerShell** và gõ (thay IP vừa ghi):

```powershell
ssh labadmin@192.168.200.135
```

5. Lần đầu sẽ hỏi `Are you sure you want to continue connecting (yes/no...)?` → gõ `yes` → Enter → gõ mật khẩu `labadmin`.

**Bạn sẽ thấy:** dòng nhắc lệnh dạng `labadmin@vm-h:~$`. Từ giờ **mọi lệnh Linux gõ trong cửa sổ PowerShell này**, copy-paste được.

**Mẹo dán lệnh:** trong PowerShell, **bấm chuột phải** để dán. Sau khi dán, nhấn **Enter**.

**Nếu lỗi:** `Connection refused` hoặc `timed out` nghĩa là quên tick OpenSSH ở màn hình 13. Sửa bằng cách gõ thẳng trong màn hình VM: `sudo apt update && sudo apt -y install openssh-server`.

---

## Bước 5 – Cập nhật và cài phần mềm cần thiết

**Làm phần này khi VM-H còn mạng NAT.** Sau Bước 9, VM-H không còn Internet.

**Làm** (trong cửa sổ SSH vào VM-H):

```bash
sudo apt update && sudo apt -y upgrade
```

Gõ mật khẩu `labadmin` khi được hỏi. Chờ chạy xong, có thể mất vài phút.

```bash
sudo apt -y install python3-venv python3-dev libssl-dev libffi-dev build-essential jq
```

```bash
python3 --version
```

**Bạn sẽ thấy:** `Python 3.12.x` hoặc cao hơn. Cowrie cần **3.11 trở lên**.

**Nếu lỗi:**
- Hiện màn hình tím hỏi khởi động lại dịch vụ: nhấn **Enter** để đồng ý.
- Báo `Could not get lock`: chờ 1–2 phút rồi chạy lại, vì máy đang tự cập nhật nền.

---

## Bước 6 – Tạo user riêng và cài Cowrie

Cowrie chạy bằng một user riêng tên `cowrie`, không phải quản trị. Nếu honeypot có lỗi thì kẻ xấu cũng không có quyền quản trị.

**Làm:**

```bash
sudo adduser --disabled-password --gecos "" cowrie
```

Chuyển sang user `cowrie`:

```bash
sudo su - cowrie
```

**Bạn sẽ thấy:** dấu nhắc đổi thành `cowrie@vm-h:~$`.

Tạo môi trường Python riêng, rồi cài Cowrie vào đó:

```bash
python3 -m venv cowrie-env
source cowrie-env/bin/activate
```

**Bạn sẽ thấy:** đầu dấu nhắc có thêm `(cowrie-env)`.

```bash
pip install --upgrade pip
pip install cowrie
```

Chờ cài xong (vài phút). Xem phiên bản và khởi tạo cấu hình:

```bash
pip show cowrie | head -2
cowrie init
ls ~/etc ~/var
```

**Bạn sẽ thấy:**
- `Name: cowrie` và `Version: ...`. Ghi phiên bản vào Bước 16.
- Lệnh `ls` cho thấy có `cowrie.cfg` trong `etc` và có thư mục `var`. **[kiểm tra]** Nếu tên file khác, ghi lại vào Bước 16.

**Nếu lỗi:**
- `pip install cowrie` báo lỗi biên dịch: quay lại Bước 5, chắc chắn đã cài đủ các gói.
- Lệnh `cowrie` báo `command not found`: chưa có `(cowrie-env)` ở đầu dấu nhắc. Chạy lại `source ~/cowrie-env/bin/activate`.

---

## Bước 7 – Cấu hình Cowrie

Vẫn ở user `cowrie`, có `(cowrie-env)` ở đầu dấu nhắc.

### 7.1. Bật Telnet giả

Kiểm tra file cấu hình đã có mục `[telnet]` chưa:

```bash
grep -n '^\[telnet\]' ~/etc/cowrie.cfg
```

- **Không in ra gì:** chạy lệnh sau để thêm vào cuối file:

```bash
printf '\n[telnet]\nenabled = true\n' >> ~/etc/cowrie.cfg
```

- **Có in ra một dòng** (ví dụ `12:[telnet]`): mở file để sửa:

```bash
nano ~/etc/cowrie.cfg
```

  Tìm dòng `enabled` ngay dưới `[telnet]`, sửa thành `enabled = true`. Lưu bằng **Ctrl + O** → **Enter**; thoát bằng **Ctrl + X**.

Kiểm tra lại:

```bash
grep -n -A1 '^\[telnet\]' ~/etc/cowrie.cfg
```

**Bạn sẽ thấy:** `[telnet]` và ngay dưới là `enabled = true`.

### 7.2. Tạo danh sách tài khoản giả (bắt buộc)

Nếu bỏ qua bước này, Cowrie dùng danh sách mặc định **chấp nhận gần như mọi mật khẩu**, và thử nghiệm "gõ sai mật khẩu" sẽ hỏng.

Danh sách chính thức do TV4 gửi (bàn giao BG-01). Trong lúc chờ, tạo bản tạm chỉ chấp nhận **một** tài khoản giả. Thay `LabOnly-2026` nếu muốn mật khẩu giả khác:

```bash
echo 'labuser:x:LabOnly-2026' > ~/etc/userdb.txt
cat ~/etc/userdb.txt
```

**Bạn sẽ thấy:** `labuser:x:LabOnly-2026`.

Nghĩa của dòng này: chỉ cặp `labuser` / `LabOnly-2026` vào được; mọi cặp khác bị từ chối. Bước 8 sẽ kiểm tra lại.

### 7.3. Kiểm tra không có gì gửi dữ liệu ra ngoài

```bash
grep -nE '^\[(output_|proxy|llm)|^backend|^enabled' ~/etc/cowrie.cfg
```

**[kiểm tra]** Đọc kết quả:
- Nếu có dòng `backend = ...` thì giá trị phải là `shell`. Không có dòng nào thì mặc định cũng là `shell`.
- Ngoài `[output_jsonlog]` (ghi log ra file), không được có mục `[output_...]` nào khác kèm `enabled = true`. Nếu có, mở `nano ~/etc/cowrie.cfg` sửa thành `enabled = false`.

Chụp màn hình kết quả này để làm minh chứng.

---

## Bước 8 – Chạy thử Cowrie ngay trên VM-H

**Làm** (user `cowrie`):

```bash
cowrie start
```

Chờ khoảng 5 giây, rồi kiểm tra Cowrie đang mở hai cổng:

```bash
ss -ltn | grep -E ':2222|:2223'
```

**Bạn sẽ thấy:** hai dòng, một dòng chứa `:2222`, một dòng chứa `:2223`.

**Nếu không thấy:** xem lỗi bằng lệnh dưới, rồi đọc mục Xử lý sự cố ở cuối file.

```bash
tail -n 30 ~/var/log/cowrie/cowrie.log
```

**Thử đăng nhập vào honeypot.** Mở **cửa sổ PowerShell thứ hai**, SSH vào VM-H bằng `labadmin` như Bước 4, rồi gõ:

```bash
ssh -p 2222 -o PubkeyAuthentication=no labuser@127.0.0.1
```

- Hỏi `yes/no` → gõ `yes`.
- Hỏi password: **cố tình gõ sai** một lần (ví dụ `abc`) → phải báo `Permission denied, please try again.`
- Gõ đúng `LabOnly-2026` → vào được dấu nhắc trông như server thật. **Đây là shell giả của honeypot.**
- Gõ `whoami` → Enter, rồi gõ `exit`.

Xem honeypot đã ghi được gì:

```bash
sudo jq -r '.eventid' /home/cowrie/var/log/cowrie/cowrie.json | sort | uniq -c
```

**Bạn sẽ thấy:** danh sách sự kiện, trong đó có `cowrie.login.failed`, `cowrie.login.success`, `cowrie.command.input`.

**Nếu gõ sai mà vẫn vào được:** file `userdb.txt` chưa đúng; quay lại 7.2. Nếu báo không tìm thấy file `cowrie.json` thì đường dẫn log khác; xem `ls /home/cowrie/var/log/cowrie/` và ghi lại vào Bước 16.

**Dọn log chạy thử**, để log smoke test sau này sạch. Quay lại **cửa sổ PowerShell thứ nhất** (user `cowrie`):

```bash
cowrie stop
mkdir -p ~/archive
mv ~/var/log/cowrie/cowrie.json* ~/archive/
```

---

## Bước 9 – Chuyển VM-H sang mạng lab và đặt IP cố định

Từ bước này, VM-H **không còn Internet**.

### 9.1. Đổi card mạng trong VMware

1. Trong cửa sổ SSH, gõ `exit` cho tới khi về PowerShell của Windows.
2. Trong VMware, chọn VM-H → **VM → Power → Shut Down Guest**. Chờ VM tắt hẳn.
3. Chọn VM-H → **VM → Settings**:
   - Tab **Hardware** → **Network Adapter** → chọn **Custom: Specific virtual network** → chọn **VMnet1 (Host-only)**.
   - **CD/DVD**: bỏ tick **Connect at power on**.
   - Tab **Options** → **Shared Folders** → chọn **Disabled**.
   - Tab **Options** → **Guest Isolation** → bỏ tick **Enable drag and drop** và **Enable copy and paste**.
   - Bấm **OK**.
4. Bật lại VM-H: **Power on this virtual machine**.

### 9.2. Tìm IP tạm trên mạng mới

Đăng nhập ở màn hình VM (`labadmin`), gõ:

```bash
ip -br a
```

**Bạn sẽ thấy** `ens33` có IP dạng `<SUBNET>.1xx`, tức là đã nằm trong mạng VMnet1. Ghi lại IP này và **tên card mạng** (thường là `ens33`).

**Nếu `ens33` không có IP:** trong VMware mở **Edit → Virtual Network Editor** → chọn VMnet1 → tick **Use local DHCP service to distribute IP address to VMs** → **OK**. Sau đó khởi động lại VM-H và xem lại.

Từ PowerShell trên Windows, SSH vào IP tạm đó:

```powershell
ssh labadmin@<IP tạm vừa thấy>
```

### 9.3. Đặt IP cố định `<SUBNET>.20`

Dán lần lượt từng khối. **Sửa dòng đầu cho đúng `<SUBNET>` của bạn.**

```bash
SUBNET=192.168.150
IFACE=$(ip -br link | awk '$1!="lo"{print $1; exit}')
echo "Dai mang: $SUBNET  -  Card mang: $IFACE"
```

**Bạn sẽ thấy:** dải mạng và tên card đúng như đã ghi. Sai thì dừng lại, sửa dòng `SUBNET=` rồi chạy lại.

```bash
echo 'network: {config: disabled}' | sudo tee /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg
```

*(Lệnh trên chặn cloud-init tự ghi đè cấu hình mạng của ta.)*

```bash
sudo tee /etc/netplan/50-cloud-init.yaml >/dev/null <<EOF
network:
  version: 2
  ethernets:
    $IFACE:
      dhcp4: false
      addresses: [$SUBNET.20/24]
EOF
sudo chmod 600 /etc/netplan/50-cloud-init.yaml
cat /etc/netplan/50-cloud-init.yaml
```

**Bạn sẽ thấy:** nội dung file có tên card và địa chỉ `<SUBNET>.20/24`.

Áp dụng cấu hình. **Cửa sổ SSH sẽ bị treo hoặc ngắt; đó là bình thường**, vì IP đã đổi:

```bash
sudo netplan apply
```

Đóng cửa sổ PowerShell đó, mở cửa sổ mới và SSH vào IP mới:

```powershell
ssh labadmin@<SUBNET>.20
```

**Bạn sẽ thấy:** vào được VM-H như bình thường.

**Nếu lỗi:** không SSH được vào `<SUBNET>.20`. Đăng nhập ở màn hình VM, gõ `ip -br a` xem IP thực tế; gõ `cat /etc/netplan/50-cloud-init.yaml` xem có gõ sai dải mạng không. Sửa bằng `sudo nano /etc/netplan/50-cloud-init.yaml`, rồi chạy `sudo netplan apply`.

---

## Bước 10 – Bật firewall, khởi động Cowrie, chụp snapshot

### 10.1. Firewall

Trong SSH vào VM-H (user `labadmin`). Sửa dòng `SUBNET=` cho đúng:

```bash
SUBNET=192.168.150
sudo ufw default deny incoming
sudo ufw default deny outgoing
sudo ufw allow in from $SUBNET.1 to any port 22 proto tcp
sudo ufw allow in from $SUBNET.0/24 to any port 2222 proto tcp
sudo ufw allow in from $SUBNET.0/24 to any port 2223 proto tcp
sudo ufw enable
```

Hỏi `Command may disrupt existing ssh connections. Proceed with operation (y|n)?` → gõ `y` → Enter.

```bash
sudo ufw status verbose
```

**Bạn sẽ thấy:**
- `Status: active`;
- dòng `Default: deny (incoming), deny (outgoing)`;
- 3 luật cho cổng 22 (chỉ từ `<SUBNET>.1`), 2222 và 2223.

Các luật này nghĩa là:
- chỉ máy Windows của bạn vào được cổng quản trị 22;
- cả mạng lab vào được honeypot;
- VM-H không tự kết nối ra đâu được.

**Nếu bị mất kết nối SSH ngay sau `ufw enable`:** đăng nhập ở màn hình VM, gõ `sudo ufw disable`, kiểm tra lại `SUBNET`, rồi làm lại 10.1.

### 10.2. Khởi động Cowrie

```bash
sudo su - cowrie
source ~/cowrie-env/bin/activate
cowrie start
ss -ltn | grep -E ':2222|:2223'
```

**Bạn sẽ thấy:** hai cổng 2222 và 2223 đang mở.

### 10.3. Chụp snapshot

Snapshot là "điểm lưu game": lab có sự cố thì quay về đây trong vài giây.

Trong VMware: chọn VM-H → **VM → Snapshot → Take Snapshot...** → Name: `sau-cai-cowrie` → **Take Snapshot**.

---

## Bước 11 – Tạo VM-A (máy "người thử" số 1)

Làm giống Bước 2–5, chỉ khác những chỗ sau:

| Chỗ | VM-A |
| --- | --- |
| Bước 2 – tên máy | `VM-A` |
| Bước 2 – đĩa | `15` GB |
| Bước 2 – Processors | `1` processor, `1` core |
| Bước 3 – Your server's name | `vm-a` |
| Bước 3 – SSH configuration | Vẫn tick **Install OpenSSH server**, để điều khiển VM-A từ Windows cho dễ |
| Bước 5 | Chỉ cần chạy `sudo apt update && sudo apt -y upgrade`. Không cài Cowrie |

Sau đó làm **Bước 9** cho VM-A, nhưng **dùng IP `.10` thay cho `.20`**:
- Ở 9.3, sửa dòng `addresses: [$SUBNET.20/24]` thành `addresses: [$SUBNET.10/24]`.
- SSH vào VM-A bằng `ssh labadmin@<SUBNET>.10`.
- VM-A **không cần** Bước 10 (firewall, Cowrie).

Kiểm tra VM-A có đủ công cụ:

```bash
ssh -V
script --version
python3 --version
```

**Bạn sẽ thấy:** ba dòng phiên bản, không có lỗi.

Chụp snapshot VM-A tên `sau-cai-dat`.

---

## Bước 12 – Chuẩn bị máy Windows làm "người thử" số 2

**Làm:**

1. Kiểm tra SSH client và IP của Windows trên mạng lab:

```powershell
ssh -V
ipconfig
```

**Bạn sẽ thấy:**
- một dòng `OpenSSH_for_Windows_...`;
- trong `ipconfig`, mục **Ethernet adapter VMware Network Adapter VMnet1** có `IPv4 Address` là `<SUBNET>.1`.

2. Bật Telnet client:
   - Bấm phím Windows, gõ `Turn Windows features on or off`, Enter.
   - Tìm **Telnet Client**, tick vào → **OK**. Chờ cài xong.
   - Kiểm tra: mở PowerShell mới, gõ `telnet` → Enter. Hiện dấu nhắc `Microsoft Telnet>` là được; gõ `quit` → Enter để thoát.

**Nếu không có Telnet Client:** cài **PuTTY** (https://www.putty.org) và khi kết nối chọn **Connection type: Other → Telnet**.

---

## Bước 13 – Smoke test (kiểm tra toàn bộ từ hai nguồn)

Mục tiêu: chứng minh honeypot ghi đúng **SSH và Telnet**, từ **cả hai nguồn**. Log ở bước này gửi cho TV2 (bàn giao BG-02).

### 13.1. Chuẩn bị log sạch và ghi giờ

SSH vào VM-H (`labadmin`), chuyển sang user `cowrie` và làm mới log:

```bash
sudo su - cowrie
source ~/cowrie-env/bin/activate
cowrie stop
mv ~/var/log/cowrie/cowrie.json* ~/archive/ 2>/dev/null
cowrie start
exit
```

Ghi giờ UTC trên cả ba máy và chép kết quả vào một file ghi chú.

Trên VM-H và trên VM-A:

```bash
date -u +%FT%T
```

Trên Windows:

```powershell
(Get-Date).ToUniversalTime().ToString("s")
```

### 13.2. Thử từ VM-A (nguồn 1)

SSH vào VM-A (`ssh labadmin@<SUBNET>.10`), rồi từ VM-A kết nối vào honeypot:

```bash
ssh -p 2222 -o PubkeyAuthentication=no labuser@<SUBNET>.20
```

1. Gõ `yes` nếu được hỏi.
2. Gõ **sai** mật khẩu một lần.
3. Gõ **đúng** mật khẩu.
4. Gõ `whoami`, rồi `exit`.

### 13.3. Thử từ Windows (nguồn 2) – SSH

Trong PowerShell (không SSH vào đâu cả):

```powershell
ssh -p 2222 -o PubkeyAuthentication=no labuser@<SUBNET>.20
```

Làm giống 13.2: sai một lần, đúng một lần, `whoami`, `exit`.

### 13.4. Thử từ Windows (nguồn 2) – Telnet

```powershell
telnet <SUBNET>.20 2223
```

1. Thấy `login:` → gõ `labuser`.
2. Thấy `Password:` → gõ **sai** một lần.
3. Thử lại → gõ **đúng**.
4. Gõ `whoami`, rồi `exit`.

### 13.5. Kiểm tra kết quả trên VM-H

SSH vào VM-H (`labadmin`):

```bash
sudo jq -r 'select(.eventid=="cowrie.session.connect") | [.timestamp, .src_ip, .protocol] | @tsv' /home/cowrie/var/log/cowrie/cowrie.json
```

**Bạn sẽ thấy 3 dòng:**
- một dòng `ssh` từ `<SUBNET>.10`;
- một dòng `ssh` từ `<SUBNET>.1`;
- một dòng `telnet` từ `<SUBNET>.1`.

```bash
sudo jq -r '.eventid' /home/cowrie/var/log/cowrie/cowrie.json | sort | uniq -c
```

**Bạn sẽ thấy:**
- `cowrie.login.failed` khoảng 3 lần (mỗi lần gõ sai một sự kiện);
- `cowrie.login.success` 3 lần;
- có `cowrie.command.input` và `cowrie.session.closed`.

**Smoke test ĐẠT khi** thấy đủ các điều trên. Nếu một lần gõ sai mà lại vào được, kiểm tra lại Bước 7.2.

Lấy log smoke test về repo theo **Bước 15**, nhưng lưu vào thư mục `evidence/smoke_test/` thay cho `data/raw/RUN-01/`.

---

## Bước 14 – Kiểm tra cách ly (TV3 sẽ làm lại độc lập)

Mục tiêu: chứng minh honeypot **không ra được Internet**.

**Trên VM-H** (`labadmin`), hai lệnh sau **phải thất bại**:

```bash
ping -c 2 -W 2 8.8.8.8
curl -m 5 https://example.com
```

**Bạn sẽ thấy:**
- `ping` báo `100% packet loss` hoặc `Network is unreachable`;
- `curl` báo lỗi (không phân giải được tên miền hoặc hết thời gian chờ).

**Trong shell giả của honeypot:** đăng nhập `labuser` qua cổng 2222, gõ `wget http://example.com`. Lệnh phải không tải được gì.

**Từ VM-A, cổng quản trị của VM-H phải bị chặn:**

```bash
ssh -o ConnectTimeout=5 labadmin@<SUBNET>.20
```

**Bạn sẽ thấy:** `Connection timed out` sau khoảng 5 giây.

Chép lệnh và kết quả của cả bước này vào `review/kiem_tra_cach_ly.md` (hoặc chụp màn hình).

**Nếu `ping` hoặc `curl` thành công: DỪNG LẠI.** VM-H vẫn còn Internet. Kiểm tra lại Bước 9.1 (card mạng phải là VMnet1, không còn NAT) và Bước 10.1 (`sudo ufw status verbose`).

---

## Bước 15 – Lấy log về repo

Làm sau **mỗi lượt thử**. Thay `RUN-01` bằng tên lượt thử, ví dụ `RUN-02` cho lượt thứ hai.

**15.1. Trên VM-H** (`labadmin`), chép log sang chỗ đọc được:

```bash
sudo rm -rf /tmp/run && sudo mkdir /tmp/run
sudo cp /home/cowrie/var/log/cowrie/cowrie.json* /tmp/run/
sudo cp -r /home/cowrie/var/lib/cowrie/tty /tmp/run/
sudo chown -R labadmin /tmp/run
ls -R /tmp/run
```

**15.2. Trên Windows**, mở thư mục repo bằng VS Code → menu **Terminal → New Terminal**. Terminal mở sẵn ở thư mục repo. Gõ:

```powershell
mkdir data\raw\RUN-01
scp -r labadmin@<SUBNET>.20:/tmp/run/* data\raw\RUN-01\
```

**15.3. Tính hash** để chứng minh log không bị sửa. Mở **Git Bash** ở thư mục repo: trong VS Code, bấm mũi tên cạnh dấu `+` của Terminal → chọn **Git Bash**. Gõ:

```bash
cd data/raw/RUN-01
find . -type f ! -name SHA256SUMS -exec sha256sum {} + > SHA256SUMS
sha256sum -c SHA256SUMS
```

**Bạn sẽ thấy:** mỗi file một dòng kết thúc bằng `OK`.

**Từ đây không sửa bất kỳ file nào trong `data/raw/`.**

**15.4. Trước lượt thử tiếp theo**, làm mới log trên VM-H như Bước 13.1.

---

## Bước 16 – Ghi thông số thực tế

Điền bảng dưới đây và commit cùng file này.

| Mục | Giá trị |
| --- | --- |
| Phiên bản VMware Workstation (Help → About) | |
| `<SUBNET>` (VMnet1) | |
| Phiên bản Ubuntu (`lsb_release -d`) và Python trên VM-H | |
| Phiên bản Cowrie (`pip show cowrie`) | |
| Tên card mạng VM-H / VM-A | |
| Đường dẫn log thực tế trên VM-H | |
| Tên file JSON sau khi xoay vòng (nếu thấy) | |
| Plugin output đang bật (Bước 7.3) | |
| Lệnh `cowrie status` có chạy được không | |

Sau đó:
1. Chép cấu hình **đã bỏ thông tin nhạy cảm** (`cowrie.cfg`; `userdb.txt` chỉ chứa mật khẩu giả) vào `Implement/lab/cowrie/`.
2. Viết báo cáo ngắn vào `docs/bao_cao_cong_viec/` và làm theo `BAN_GIAO.md` để gửi **BG-02** (cho TV2), **BG-03** và **BG-08** (cho TV3).

---

## Phụ lục 1 – Mỗi lần mở lab lại

Cowrie **không tự chạy** khi bật VM. Mỗi lần bật VM-H:

1. Bật VM-H (và VM-A nếu cần) trong VMware.
2. Từ PowerShell: `ssh labadmin@<SUBNET>.20`.
3. Chạy:

```bash
sudo su - cowrie
source ~/cowrie-env/bin/activate
cowrie start
ss -ltn | grep -E ':2222|:2223'
```

## Phụ lục 2 – Tắt lab

- Trên VM-H (user `cowrie`): `cowrie stop`.
- Trong VMware: **VM → Power → Shut Down Guest** cho từng VM.
- Tắt VM-H khi không dùng.

## Phụ lục 3 – Quay về snapshot khi hỏng

VMware → chọn VM → **VM → Snapshot → Revert to Snapshot** → chọn `sau-cai-cowrie` → **Yes**.

Mọi thay đổi sau thời điểm snapshot sẽ mất, kể cả log. Lấy log về repo trước khi quay về.

## Phụ lục 4 – Đổi danh sách tài khoản khi TV4 gửi (BG-01)

```bash
sudo su - cowrie
source ~/cowrie-env/bin/activate
nano ~/etc/userdb.txt        # dán danh sách mới; Ctrl+O, Enter để lưu; Ctrl+X để thoát
cowrie stop
cowrie start
```

Sau khi đổi, thử lại một lần gõ sai và một lần gõ đúng như Bước 8 để chắc danh sách mới hoạt động.

## Phụ lục 5 – Xử lý sự cố

| Hiện tượng | Nguyên nhân thường gặp | Cách sửa |
| --- | --- | --- |
| VMware báo VT-x/AMD-V disabled | Ảo hóa đang tắt trong BIOS | Vào BIOS bật Virtualization Technology |
| VM chạy rất chậm | Windows đang bật Hyper-V/VBS | Vẫn dùng được, chỉ chậm hơn. Hỏi nhóm trước khi tắt các tính năng bảo mật của Windows |
| `ssh labadmin@...` báo `Connection refused` | VM chưa cài OpenSSH server | Ở màn hình VM: `sudo apt install openssh-server` (cần còn mạng NAT) |
| `ssh` báo `REMOTE HOST IDENTIFICATION HAS CHANGED` | Cùng một IP, máy đã cài lại | `ssh-keygen -R <IP>` (với cổng 2222: `ssh-keygen -R "[<SUBNET>.20]:2222"`) rồi thử lại |
| `pip install cowrie` lỗi | Thiếu gói hoặc Python quá cũ | Làm lại Bước 5; `python3 --version` phải ≥ 3.11 |
| `cowrie: command not found` | Chưa vào môi trường Python | `sudo su - cowrie` rồi `source ~/cowrie-env/bin/activate` |
| Không thấy cổng 2223 | Chưa bật Telnet | Làm lại Bước 7.1, rồi `cowrie stop` và `cowrie start` |
| Cowrie không chạy | Lỗi cấu hình | `tail -n 50 ~/var/log/cowrie/cowrie.log`, copy lỗi gửi nhóm |
| Gõ sai mật khẩu vẫn vào được | `userdb.txt` thiếu hoặc sai | Làm lại Bước 7.2 |
| Windows không kết nối được `<SUBNET>.20` | VM chưa ở VMnet1, sai IP, hoặc firewall | `ipconfig` trên Windows; `ip -br a` và `sudo ufw status` trên VM-H |
| Mất SSH sau khi bật ufw | Sai `SUBNET` trong luật cổng 22 | Ở màn hình VM: `sudo ufw disable`, sửa, làm lại 10.1 |
| `scp` báo `Permission denied` | Chưa chạy `chown` ở 15.1 | Làm lại 15.1 |

## Phụ lục 6 – Checklist hoàn thành WP-03

- [ ] Cowrie chạy bằng user `cowrie`, mở cổng 2222 và 2223
- [ ] Có `userdb.txt` riêng; gõ sai thì bị từ chối
- [ ] VM-H chỉ còn card VMnet1, IP `<SUBNET>.20`, ufw bật; đã tắt Shared Folders, kéo-thả và copy-paste
- [ ] Snapshot `sau-cai-cowrie` (VM-H) và `sau-cai-dat` (VM-A)
- [ ] Smoke test đạt; log lưu ở `evidence/smoke_test/` kèm `SHA256SUMS` → gửi **BG-02** cho TV2
- [ ] Kiểm tra cách ly đạt (Bước 14)
- [ ] Bảng Bước 16 đã điền; cấu hình đã làm sạch nằm trong `Implement/lab/cowrie/` → gửi **BG-03** cho TV3
- [ ] Danh sách yếu tố mồi (tên máy, phiên bản SSH công bố, hệ thống file giả, `userdb`) → gửi **BG-08** cho TV3
