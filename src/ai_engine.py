import os
import google.generativeai as genai
from dotenv import load_dotenv
from .actions import (
    open_app, open_directory, take_screenshot, 
    open_link, list_running_apps, kill_application
)

load_dotenv()

class AIEngine:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Thiếu GEMINI_API_KEY trong file .env")
        
        genai.configure(api_key=api_key)
        
        # Danh sách tools để AI có thể gọi
        self.tools = [
            open_app, open_directory, take_screenshot, 
            open_link, list_running_apps, kill_application
        ]
        
        self.model = genai.GenerativeModel(
            model_name='gemini-3-flash-preview',
            tools=self.tools,
            system_instruction=(
                "Bạn là Davis Iron, trợ lý AI thông minh trên Desktop của chủ nhân. "
                "Bạn có quyền điều khiển máy tính thông qua các công cụ được cung cấp. "
                "Hãy phản hồi lịch sự, ngắn gọn và thực thi lệnh ngay khi được yêu cầu. "
                "Nếu không chắc chắn về đường dẫn, hãy hỏi lại chủ nhân."
            )
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def process_message(self, user_input: str):
        """Xử lý tin nhắn và trả về kết quả (Text hoặc Path tới file)"""
        try:
            response = self.chat.send_message(user_input)
            
            # Kiểm tra xem có kết quả từ function calling là đường dẫn file không
            # (Đặc biệt cho screenshot)
            for part in response.candidates[0].content.parts:
                if part.function_call:
                    # Nếu là take_screenshot, giá trị trả về thực tế sẽ được xử lý tự động bởi SDK
                    # Nhưng chúng ta cần biết liệu user có nhận được ảnh không
                    pass

            return response.text
        except Exception as e:
            return f"⚠️ Lỗi AI Engine: {str(e)}"
