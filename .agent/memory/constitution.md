# Hiến pháp Dự án: Davis Iron AI (Project Constitution)

## 1. Tầm nhìn (Vision)
Xây dựng một trợ lý AI mạnh mẽ, linh hoạt và an toàn chạy trên Desktop, cho phép người dùng điều khiển máy tính cá nhân từ xa thông qua Telegram với sự hỗ trợ của Gemini Flash.

## 2. Nguyên tắc Phát triển (Development Principles)
- **An toàn là trên hết:** Mọi lệnh thực thi hệ thống phải được kiểm soát chặt chẽ. Chỉ chủ nhân (Whitelist ID) mới có quyền truy cập.
- **Tốc độ & Hiệu quả:** Tận dụng Gemini Flash để phản hồi nhanh và tiết kiệm chi phí.
- **Tính module hóa:** Tách biệt rõ ràng giữa logic AI, logic Bot và logic Thực thi Hệ thống.
- **Dữ liệu Thực:** Không sử dụng mock data trong quá trình phát triển logic thực thi.

## 3. Quy tắc Code (Coding Standards)
- Ngôn ngữ: Python 3.10+
- Định dạng: PEP 8
- Tài liệu: Mọi hàm thực thi (Action) cho AI phải có docstring rõ ràng để Function Calling hoạt động chính xác.

## 4. Bảo mật (Security)
- Tuyệt đối không commit file `.env` chứa API Key.
- Sử dụng whitelist ID cho mọi request từ Telegram.
