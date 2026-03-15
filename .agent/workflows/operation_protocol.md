# Quy trình Vận hành (Standard Operating Procedure - SOP)

Workflow này tuân thủ bộ lọc 5 bước nghiêm ngặt theo quy định của dự án Davis Iron AI.

## Bước 1: Specify (Xác định)
- Làm rõ yêu cầu của Developer.
- Xác định Input, Output và các sự phụ thuộc (Dependencies).
- Kiểm tra `infrastructure.md` để đảm bảo môi trường sẵn sàng.

## Bước 2: Plan (Lập kế hoạch)
- Đối chiếu với cấu trúc dự án và Tech Stack.
- Xác định các file bị ảnh hưởng.
- Đảm bảo tính "Nguyên tử" (Atomic): Mỗi task ảnh hưởng $\le 3$ files.

## Bước 3: Tasks (Chia nhỏ công việc)
- Liệt kê các bước thực thi độc lập.
- Sử dụng PowerShell 5.1+ để kết nối các lệnh.

## Bước 4: Implement (Triển khai)
- Viết code thực tế, kết nối logic nghiệp vụ.
- **KHÔNG** dùng mock-up hay placeholder.
- Sử dụng dải port [8900-8999] nếu cần.

## Bước 5: Verify (Kiểm thử - Tester Case)
- Thực thi workflow `tester_case.md`.
- Chỉ bàn giao khi kết quả là **PASS**.
