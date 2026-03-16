import requests
import os
import sys
import subprocess
import time
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

GITHUB_REPO = os.getenv("GITHUB_REPO", "acmavirus/DavisIronAI")

class AutoUpdater:
    def __init__(self, current_version):
        self.current_version = current_version
        self.latest_version = None
        self.download_url = None

    def check_for_updates(self):
        """Kiểm tra bản cập nhật mới nhất từ GitHub Releases"""
        try:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.latest_version = data.get("tag_name", "").replace("v", "")
                
                # Tìm asset là file .exe
                assets = data.get("assets", [])
                for asset in assets:
                    if asset.get("name", "").endswith(".exe"):
                        self.download_url = asset.get("browser_download_url")
                        break
                
                if self.latest_version and self.latest_version > self.current_version:
                    return True
            return False
        except Exception as e:
            logger.error(f"Lỗi khi kiểm tra cập nhật: {e}")
            return False

    def download_and_install(self):
        """Tải về và thay thế file exe hiện tại"""
        if not self.download_url:
            return False
            
        try:
            print(f"📥 Đang tải bản cập nhật {self.latest_version}...")
            response = requests.get(self.download_url, stream=True)
            
            new_exe = "DavisIronAI_new.exe"
            with open(new_exe, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Tạo script batch để thay thế file khi app đã đóng
            current_exe = sys.executable
            if not current_exe.endswith(".exe"):
                # Nếu đang chạy bằng python script, chỉ cần thông báo
                print("💡 Đang chạy ở chế độ script, vui lòng git pull để cập nhật.")
                return False

            update_script = "update.bat"
            with open(update_script, "w") as f:
                f.write(f"@echo off\n")
                f.write(f"timeout /t 2 /nobreak > nul\n")
                f.write(f"del \"{current_exe}\"\n")
                f.write(f"move \"{new_exe}\" \"{current_exe}\"\n")
                f.write(f"start \"\" \"{current_exe}\"\n")
                f.write(f"del \"%~f0\"\n")
            
            print("🚀 Đang khởi động lại để áp dụng cập nhật...")
            subprocess.Popen([update_script], shell=True)
            sys.exit(0)
        except Exception as e:
            logger.error(f"Lỗi khi cài đặt cập nhật: {e}")
            return False
