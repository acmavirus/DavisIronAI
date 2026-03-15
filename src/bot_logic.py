import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from .ai_engine import AIEngine
from dotenv import load_dotenv

load_dotenv()

# Cấu hình logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class DavisBot:
    def __init__(self):
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.whitelist_id = os.getenv("WHITELIST_USER_ID")
        
        if not token or not self.whitelist_id:
            raise ValueError("Thiếu TELEGRAM_BOT_TOKEN hoặc WHITELIST_USER_ID trong .env")
            
        self.ai = AIEngine()
        self.app = Application.builder().token(token).build()

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        # 💡 Mẹo: Nếu bạn chưa biết ID của mình, bot sẽ in ra console
        print(f"📩 Nhận tin nhắn từ ID: {user_id} (@{update.effective_user.username})")

        # 🛡️ Kiểm tra bảo mật
        try:
            allowed_id = int(self.whitelist_id)
        except (ValueError, TypeError):
            allowed_id = None

        if user_id != allowed_id:
            await update.message.reply_text(
                f"⛔ Truy cập bị từ chối.\n"
                f"ID của bạn là: `{user_id}`\n"
                f"Hãy copy số này dán vào `WHITELIST_USER_ID` trong file `.env`.",
                parse_mode='Markdown'
            )
            return

        user_text = update.message.text
        if not user_text:
            return

        # Gửi thông báo đang xử lý
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

        # Gọi AI Engine
        reply = self.ai.process_message(user_text)

        # Kiểm tra nếu reply liên quan đến screenshot (giả định logic trả về path)
        if "temp\\screenshot.png" in str(reply) or os.path.exists("temp/screenshot.png"):
            # Nếu AI đã chụp ảnh, gửi ảnh thay vì text (Cần logic check path thực tế)
            # Lưu ý: Gemini SDK tự động gọi hàm, ta có thể cần check file mới nhất trong temp
            photo_path = "temp/screenshot.png"
            if os.path.exists(photo_path):
                await update.message.reply_photo(photo=open(photo_path, 'rb'), caption="📸 Ảnh chụp màn hình của bạn đây!")
                os.remove(photo_path) # Xóa sau khi gửi để bảo mật
                return

        await update.message.reply_text(reply)

    def run(self):
        self.app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_message))
        print("🚀 Davis Iron AI đang sẵn sàng trên Telegram...")
        self.app.run_polling()
