---
description: Quy trình cập nhật tự động cho mã nguồn và ứng dụng Davis Iron AI
---

# 🔄 Quy trình Update Tự động

Workflow này hướng dẫn cách kiểm tra, tải về và áp dụng các bản cập nhật mới nhất cho Davis Iron AI.

## 🏁 Kiểm tra Phiên bản hiện tại
Mở file `src/main.py` để xem giá trị hằng số `VERSION`.

## 📦 Các phương thức cập nhật

### Cách 1: Cập nhật mã nguồn (Git)
Dành cho môi trường phát triển (Dev).

// turbo
```powershell
git pull origin main
pip install -r requirements.txt
```

### Cách 2: Cập nhật bản EXE (Tính năng tích hợp)
Ứng dụng Davis Iron AI được thiết kế để tự động quản lý vòng đời cập nhật:

1.  **Tự động kiểm tra:** Ngay khi khởi động, ứng dụng sẽ gửi request đến GitHub API để so sánh `VERSION`.
2.  **Thông báo:** Nếu có bản mới, Bot sẽ gửi tin nhắn Telegram: *"Đã có bản cập nhật mới (vX.X.X)! Gõ /update để tự động nâng cấp."*
3.  **Lệnh `/update`:** Khi người dùng gửi lệnh này:
    *   Ứng dụng tải về file `.exe` mới.
    *   Tự động giải phóng file cũ bằng script `update.bat`.
    *   Khởi động lại phiên bản mới nhất ngay lập tức.

## 📝 Quy trình kỹ thuật (Dành cho Dev)

Để tính năng này hoạt động, file [src/updater.py](file:///c:/Users/AcmaTvirus/Desktop/DavisIronAI/src/updater.py) xử lý:
- Request API GitHub.
- Stream download file nhị phân.
- Xử lý tiến trình nền để thay thế EXE đang chạy.

---
**Managed by Davis Iron Agent**

---
**Managed by Davis Iron Agent**
