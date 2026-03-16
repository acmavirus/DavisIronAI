---
description: Quy trình tự động tạo GitHub Release và upload file EXE
---

# 🚀 Quy trình Phát hành (Release) GitHub

Workflow này hướng dẫn cách tự động tạo Tag, Release và upload file EXE lên GitHub dựa trên `VERSION` trong code.

## 🛠️ Yêu cầu tiền quyết
- Đã cài đặt [GitHub CLI (gh)](https://cli.github.com/).
- Đã đăng nhập bằng lệnh `gh auth login`.
- Đã thực hiện build EXE thành công (có file trong thư mục `dist/`).

## 📝 Các bước thực hiện

# 🚀 Quy trình Phát hành (Release) qua GitHub Actions

Dự án hiện được cấu hình để tự động build và tạo release thông qua GitHub Actions mỗi khi bạn đẩy một **Tag** mới lên repository.

## 📝 Các bước thực hiện

### 1. Chuẩn bị mã nguồn
Đảm bảo bạn đã cập nhật `VERSION` trong `src/main.py` và commit mọi thay đổi.

### 2. Tạo và Đẩy Tag
Sử dụng PowerShell để tạo tag dựa trên phiên bản và đẩy lên GitHub:

// turbo
```powershell
$version = (Select-String -Path .env -Pattern "APP_VERSION=(.*)").Matches.Groups[1].Value
git tag "v$version"
git push origin "v$version"
```

### 3. Tự động hóa (GitHub Actions)
Ngay sau khi lệnh `git push` hoàn tất:
1. GitHub Actions sẽ tự động kích hoạt workflow `release.yml`.
2. Hệ thống sẽ khởi tạo một môi trường Windows ảo.
3. Tự động Build file `DavisIronAI.exe` bằng PyInstaller.
4. Tự động tạo bản Release và gắn file EXE vào.

## 🖥️ Theo dõi tiến độ
Bạn có thể xem tiến trình build tại tab **Actions** trên Repository GitHub của mình.

---
**Managed by Davis Iron Agent**
