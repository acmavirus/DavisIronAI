---
description: Quy trình đóng gói ứng dụng Davis Iron AI thành file thực thi (.exe)
---

# 📦 Quy trình Build EXE (Windows)

Workflow này hướng dẫn đóng gói mã nguồn Python thành một file `.exe` duy nhất để chạy trên Windows mà không cần cài đặt Python.

## 🛠️ Yêu cầu tiền quyết
- Đã cài đặt Python 3.10+ và các thư viện trong `requirements.txt`.
- Đã cài đặt `pyinstaller`.

## 📝 Các bước thực hiện

### 1. Cài đặt PyInstaller
// turbo
```powershell
pip install pyinstaller
```

### 2. Kiểm tra môi trường
Đảm bảo file `.env` đã có các biến cần thiết (mặc dù khi build ta thường không đóng gói `.env` thật).

### 3. Thực hiện Build
Sử dụng lệnh sau để tạo file EXE duy nhất, không hiện cửa sổ console:

// turbo
```powershell
pyinstaller --noconfirm --onefile --windowed --name "DavisIronAI" `
--hidden-import "telegram.ext" `
--hidden-import "google.generativeai" `
--hidden-import "pyautogui" `
--hidden-import "psutil" `
--hidden-import "requests" `
--hidden-import "PIL" `
--hidden-import "dotenv" `
src/main.py
```

**Giải thích tham số:**
- `--onefile`: Đóng gói tất cả vào 1 file `.exe` duy nhất.
- `--windowed` / `--noconsole`: Không hiển thị cửa sổ CMD khi chạy bot.
- `--name "DavisIronAI"`: Đặt tên cho file output.
- `--add-data "src;src"`: Bao gồm thư mục code nguồn để các module có thể import lẫn nhau.
- `--hidden-import`: Đảm bảo các thư viện động được nhận diện đúng.

### 4. Thu thập kết quả
- File `.exe` sẽ được tạo trong thư mục `dist/`.
- Di chuyển file `.exe` ra thư mục gốc hoặc tạo folder `release/`.

## ⚠️ Lưu ý
- File `.exe` được build trên Windows nào thì chạy tốt nhất trên Windows đó.
- Người dùng cuối vẫn cần file `.env` nằm cùng thư mục với file `.exe` để bot hoạt động.

---
**Build by Davis Iron Agent**
