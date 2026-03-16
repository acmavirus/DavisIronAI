import os
from dotenv import load_dotenv

# Thêm thư mục gốc vào PYTHONPATH để import các module trong src/
sys.path.append(str(Path(__file__).parent.parent))

load_dotenv()

from src.bot_logic import DavisBot

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
    # Dọn dẹp rác từ lần chạy trước
    cleanup_temp()
    
    try:
        bot = DavisBot()
        bot.run()
    except Exception as e:
        print(f"💥 Lỗi nghiêm trọng khi khởi động: {e}")
        print("Vui lòng kiểm tra lại file .env và các dependencies.")

if __name__ == "__main__":
    main()
