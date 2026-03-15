# Quy trình Tester Case (Bắt buộc)

Trước khi bàn giao bất kỳ thay đổi nào, Agent phải tự thực hiện bộ kiểm tra sau:

## 1. Kiểm tra Tính Toàn vẹn Dữ liệu (Data Integrity)
- Đảm bảo dữ liệu hiển thị/xử lý là dữ liệu thực từ hệ thống, không phải placeholder.
- Ví dụ: Kiểm tra xem `get_ai_response` có thực sự gọi API Gemini hay không.

## 2. Kiểm tra Đơn vị (Unit Test)
- Chạy các hàm/class mới với input mẫu hợp lệ.
- Kiểm tra các hàm điều khiển OS (mở app, screenshot) trong môi trường an toàn.

## 3. Kiểm tra Build/Run (Build Check)
- Đảm bảo code không gặp lỗi syntax hay dependency.
- Thử chạy `python src/main.py` (nếu đã có file).

## 4. Kiểm tra Trường hợp Biên (Edge Cases)
- Input rỗng hoặc sai định dạng.
- Lỗi mất kết nối Internet/API.
- File config rỗng hoặc thiếu biến môi trường.

## 5. Kiểm tra Nhật ký (Log Review)
- Kiểm tra console output và file trong thư mục `logs/`.
- Đảm bảo không còn Warning/Error tiềm ẩn.

## 6. Xác nhận (Confirmation)
- Kết quả: **PASS** -> Phản hồi Developer.
- Kết quả: **FAIL** -> Tự sửa lỗi và test lại.
