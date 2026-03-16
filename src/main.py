import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Thêm thư mục gốc vào PYTHONPATH để import các module trong src/
sys.path.append(str(Path(__file__).parent.parent))

load_dotenv()

from src.bot_logic import DavisBot
from src.settings_ui import SettingsApp

VERSION = os.getenv("APP_VERSION", "1.0.0")

def cleanup_temp():
    """Dọn dẹp thư mục temp khi khởi động"""
    temp_dir = Path("temp")
    if temp_dir.exists():
        for file in temp_dir.glob("*"):
            try:
                if file.is_file():
                    os.remove(file)
            except Exception as e:
                print(f"⚠️ Không thể xóa file tạm {file}: {e}")
    else:
        temp_dir.mkdir(exist_ok=True)

def main():
    # Kiểm tra cấu hình .env, nếu thiếu thì mở Settings UI
    if not os.getenv("GEMINI_API_KEY") or not os.getenv("TELEGRAM_BOT_TOKEN"):
        print("🔍 Thiếu cấu hình, đang mở màn hình cài đặt...")
        settings = SettingsApp()
        settings.run()
        # Load lại env sau khi lưu
        load_dotenv(override=True)

    # Dọn dẹp rác từ lần chạy trước
    cleanup_temp()
    
    try:
        bot = DavisBot(VERSION)
        bot.run()
    except Exception as e:
        print(f"💥 Lỗi nghiêm trọng khi khởi động: {e}")
        print("Vui lòng kiểm tra lại file .env và các dependencies.")

if __name__ == "__main__":
    main()
