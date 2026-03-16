import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from .ai_engine import AIEngine
from .updater import AutoUpdater
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
        
        # Phiên bản từ main (giả định được truyền vào hoặc import)
        from .main import VERSION
        self.updater = AutoUpdater(VERSION)
        self.update_available = False

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

        # Kiểm tra lệnh update đặc biệt
        if user_text.lower() == "/update" and user_id == int(self.whitelist_id):
            if self.updater.check_for_updates():
                await update.message.reply_text(f"🔄 Đang bắt đầu cập nhật lên bản v{self.updater.latest_version}...")
                self.updater.download_and_install()
            else:
                await update.message.reply_text("✅ Bạn đang sử dụng phiên bản mới nhất.")
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

    async def post_init(self, application: Application):
        """Kiểm tra update ngay khi bot online"""
        if self.updater.check_for_updates():
            self.update_available = True
            msg = f"✨ **Đã có bản cập nhật mới (v{self.updater.latest_version})!**\n\nGõ `/update` để tự động nâng cấp."
            try:
                await application.bot.send_message(chat_id=self.whitelist_id, text=msg, parse_mode='Markdown')
            except Exception as e:
                print(f"Lỗi gửi tin nhắn update: {e}")

    def run(self):
        self.app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_message))
        self.app.post_init = self.post_init # Đăng ký callback sau khi khởi tạo
        print("🚀 Davis Iron AI đang sẵn sàng trên Telegram...")
        self.app.run_polling()
