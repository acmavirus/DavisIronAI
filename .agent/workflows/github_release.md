---
description: Quy trình tự động tạo GitHub Release qua file Changelog
---

# 🚀 Quy trình Phát hành (Release) qua Changelog

Dự án hiện được cấu hình để tự động build và tạo release mỗi khi bạn thêm một file nhật ký thay đổi (**Changelog**) mới vào thư mục `changelogs/`.

## 📝 Các bước thực hiện

### 1. Tạo file Changelog mới
Mỗi phiên bản mới phải có một file tương ứng trong thư mục `changelogs/` với định dạng `vX.X.X.md`.
Ví dụ: `changelogs/v1.0.1.md`

Nội dung file nên bao gồm các thay đổi chính của phiên bản này.

### 2. Đẩy thay đổi lên GitHub
Bạn chỉ cần commit file changelog mới và push lên repository:

// turbo
```powershell
git add changelogs/v1.0.1.md
git commit -m "Release v1.0.1"
git push origin main
```

### 3. Tự động hóa (GitHub Actions)
Ngay sau khi nhận được file changelog mới trong thư mục `changelogs/`:
1. GitHub Actions sẽ tự động kích hoạt.
2. Nó sẽ đọc tên file để xác định số phiên bản (`1.0.1`).
3. Nó sẽ đọc nội dung file để làm mô tả cho bản Release.
4. Tự động Build file `DavisIronAI.exe` và upload lên GitHub.

## 🖥️ Theo dõi tiến độ
Bạn có thể xem tiến trình build và release tại tab **Actions** trên Repository GitHub của mình.

---
**Managed by Davis Iron Agent**
