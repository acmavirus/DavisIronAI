import os
import subprocess
import webbrowser
import pyautogui
import psutil
from pathlib import Path

def list_running_apps() -> str:
    """
    Liệt kê danh sách các ứng dụng/tiến trình đang chạy.
    """
    try:
        apps = []
        for proc in psutil.process_iter(['name']):
            try:
                name = proc.info['name']
                if name and name not in apps:
                    apps.append(name)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        # Trả về tối đa 30 ứng dụng để tránh quá tải context
        return "Danh sách ứng dụng đang chạy: " + ", ".join(apps[:30])
    except Exception as e:
        return f"❌ Lỗi khi liệt kê ứng dụng: {str(e)}"

def kill_application(app_name: str) -> str:
    """
    Tắt một ứng dụng đang chạy dựa trên tên của nó (ví dụ: 'chrome.exe', 'notepad').
    Args:
        app_name: Tên ứng dụng hoặc tiến trình cần đóng.
    """
    try:
        killed_count = 0
        for proc in psutil.process_iter(['name']):
            try:
                if app_name.lower() in proc.info['name'].lower():
                    proc.kill()
                    killed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if killed_count > 0:
            return f"✅ Đã đóng {killed_count} tiến trình liên quan đến '{app_name}'."
        return f"❓ Không tìm thấy ứng dụng nào có tên '{app_name}' đang chạy."
    except Exception as e:
        return f"❌ Lỗi khi tắt ứng dụng: {str(e)}"

def open_app(app_name: str) -> str:
    """
    Opens a specific application on Windows.
    Args:
        app_name: The name of the application (e.g., 'notepad', 'chrome', 'calc').
    """
    try:
        # On Windows, 'start' can launch many apps/files
        subprocess.Popen(f"start {app_name}", shell=True)
        return f"✅ Đã thực hiện lệnh mở: {app_name}"
    except Exception as e:
        return f"❌ Lỗi khi mở ứng dụng: {str(e)}"

def open_directory(path_name: str) -> str:
    """
    Opens a specific directory in File Explorer.
    Args:
        path_name: Shortcut name like 'Downloads', 'Documents', 'Desktop' or a full path.
    """
    try:
        path_map = {
            "downloads": Path.home() / "Downloads",
            "documents": Path.home() / "Documents",
            "desktop": Path.home() / "Desktop"
        }
        
        target_path = path_map.get(path_name.lower())
        if not target_path:
            target_path = Path(path_name).expanduser()

        if target_path.exists():
            os.startfile(target_path)
            return f"📂 Đã mở thư mục: {target_path}"
        else:
            return f"❓ Không tìm thấy thư mục: {path_name}"
    except Exception as e:
        return f"❌ Lỗi OS: {str(e)}"

def take_screenshot() -> str:
    """
    Takes a screenshot of the primary monitor and saves it as 'screenshot.png'.
    Returns:
        The path to the saved screenshot file.
    """
    try:
        # Create logs/temp directory if not exists
        save_dir = Path("temp")
        save_dir.mkdir(exist_ok=True)
        save_path = save_dir / "screenshot.png"
        
        pyautogui.screenshot(str(save_path))
        return str(save_path)
    except Exception as e:
        return f"❌ Lỗi chụp ảnh: {str(e)}"

def open_link(url: str) -> str:
    """
    Opens a URL in the default web browser.
    Args:
        url: The web link to open (must start with http/https).
    """
    try:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        webbrowser.open(url)
        return f"🌐 Đã mở trình duyệt tại: {url}"
    except Exception as e:
        return f"❌ Lỗi trình duyệt: {str(e)}"
