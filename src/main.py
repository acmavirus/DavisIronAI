import os
import sys
import shutil
from pathlib import Path

# Thêm thư mục gốc vào PYTHONPATH để import các module trong src/
if getattr(sys, 'frozen', False):
    # PyInstaller extract path is in sys._MEIPATH (if onefile)
    bundle_root = Path(getattr(sys, '_MEIPATH', os.path.dirname(sys.executable))).resolve()
    if str(bundle_root) not in sys.path:
        sys.path.insert(0, str(bundle_root))
else:
    # Khi chạy từ source trong môi trường dev
    # main.py đang nằm trong src/, nên cha của nó là root dự án
    dev_root = Path(__file__).resolve().parent.parent
    if str(dev_root) not in sys.path:
        sys.path.insert(0, str(dev_root))

def setup_data_directory():
    """Thiết lập thư mục gốc chứa dữ liệu khi chạy dưới dạng exe"""
    is_frozen = getattr(sys, 'frozen', False)
    if not is_frozen:
        # Nếu đang chạy từ source (môi trường dev), đảm bảo thư mục làm việc là thư mục root của dự án
        os.chdir(Path(__file__).parent.parent)
        return

    # Nếu đang chạy file exe
    appdata_dir = Path(os.getenv('APPDATA', Path.home())) / "DavisIronAI"
    appdata_dir.mkdir(parents=True, exist_ok=True)
    config_file = appdata_dir / "data_path.txt"

    target_dir = None
    if config_file.exists():
        saved_dir = config_file.read_text('utf-8').strip()
        if os.path.exists(saved_dir):
            target_dir = saved_dir

    if not target_dir:
        # Hiển thị UI chọn thư mục
        import tkinter as tk
        from tkinter import filedialog, messagebox
        
        root = tk.Tk()
        root.withdraw()  # Ẩn cửa sổ chính
        
        messagebox.showinfo(
            "Thiết lập lần đầu", 
            "Chào mừng đến với Davis Iron AI!\n\nVì bạn đang chạy phiên bản đóng gói, vui lòng chọn một thư mục trên máy (ví dụ: Documents/DavisIronAI_Data) để lưu trữ các file cấu hình (.env) và dữ liệu trí nhớ."
        )
        
        chosen_dir = filedialog.askdirectory(title="Chọn thư mục chứa dữ liệu Davis Iron AI")
        if chosen_dir:
            config_file.write_text(chosen_dir, 'utf-8')
            target_dir = chosen_dir
        else:
            messagebox.showerror("Lỗi", "Bạn chưa chọn thư mục dữ liệu. Ứng dụng sẽ thoát.")
            sys.exit(1)

    # 📦 Tự động giải nén/copy assets từ bundle ra thư mục data
    try:
        data_assets_path = Path(target_dir) / "assets"
        data_assets_path.mkdir(parents=True, exist_ok=True)
        
        # Tìm assets trong bundle (bundle_root đã được xác định ở đầu file)
        bundle_assets = bundle_root / "assets"
        
        # Nếu không thấy folder assets chuẩn, thử quét đệ quy
        if not bundle_assets.exists():
            for p in bundle_root.rglob("logo.png"):
                bundle_assets = p.parent
                break
        
        if bundle_assets.exists():
            for item in bundle_assets.glob("*"):
                if item.is_file():
                    target_item = data_assets_path / item.name
                    shutil.copy2(str(item), str(target_item))
    except Exception:
        pass

    # Đổi Thư mục làm việc (Working Directory) về thư mục được chọn
    os.chdir(target_dir)

# Chạy setup directory trước khi import và xử lý bất cứ module nội bộ nào khác
setup_data_directory()

from dotenv import load_dotenv
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

import threading

def run_bot_worker():
    """Hàm chạy bot trong thread riêng"""
    try:
        # Load lại env để đảm bảo các thay đổi mới được áp dụng
        load_dotenv(override=True)
        if os.getenv("GEMINI_API_KEY") and os.getenv("TELEGRAM_BOT_TOKEN"):
            print("🚀 Đang khởi chạy Davis Bot ngầm...")
            bot = DavisBot(VERSION)
            bot.run()
    except Exception as e:
        print(f"💥 Lỗi bot: {e}")

def main():
    # Dọn dẹp rác từ lần chạy trước
    cleanup_temp()
    
    # Khởi chạy giao diện chính (Settings & Bubble)
    app = SettingsApp()
    
    # Nếu đã có cấu hình, ta khởi chạy bot ngay trong thread ngầm
    if os.getenv("GEMINI_API_KEY") and os.getenv("TELEGRAM_BOT_TOKEN"):
        bot_thread = threading.Thread(target=run_bot_worker, daemon=True)
        bot_thread.start()
    
    # Chạy UI chính (mainloop)
    app.run()

if __name__ == "__main__":
    main()
