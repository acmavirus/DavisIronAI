import sys
from pathlib import Path

# Thêm thư mục gốc vào PYTHONPATH để import các module trong src/
sys.path.append(str(Path(__file__).parent.parent))

from src.bot_logic import DavisBot

def main():
    try:
        bot = DavisBot()
        bot.run()
    except Exception as e:
        print(f"💥 Lỗi nghiêm trọng khi khởi động: {e}")
        print("Vui lòng kiểm tra lại file .env và các dependencies.")

if __name__ == "__main__":
    main()
