import os
import subprocess
import webbrowser
import pyautogui
import psutil
from pathlib import Path
from datetime import datetime
from .memory_manager import memory

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

def open_app_with_folder(app_name: str, folder_path: str = None) -> str:
    """
    Mở một ứng dụng cụ thể và có thể kèm theo một thư mục hoặc tệp tin.
    Args:
        app_name: Tên ứng dụng (ví dụ: 'Code', 'Notepad')
        folder_path: Đường dẫn đầy đủ đến thư mục hoặc tệp tin cần mở (ví dụ: 'C:\\Users\\Path\\To\\Project')
    """
    try:
        if folder_path:
            # Kiểm tra nếu đường dẫn tồn tại trước khi mở
            if os.path.exists(folder_path):
                # Sử dụng command line để mở app với path
                # Một số app cần truyền path như đối số, một số khác dùng start "app" "path"
                subprocess.Popen([app_name, folder_path], shell=True)
                return f"✅ Đã mở {app_name} với dự án tại {folder_path}"
            else:
                # Nếu path không tồn tại, chỉ mở app
                subprocess.Popen(f"start {app_name}", shell=True)
                return f"⚠️ Thư mục {folder_path} không tồn tại, nhưng tôi đã mở {app_name} cho bạn."
        
        subprocess.Popen(f"start {app_name}", shell=True)
        return f"✅ Đã mở {app_name}"
    except Exception as e:
        return f"❌ Lỗi: {str(e)}"


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

def get_directory_status(directory_path: str) -> str:
    """
    Thống kê sơ bộ về thư mục (số lượng file, ngày cập nhật gần nhất).
    Args:
        directory_path: Đường dẫn đến thư mục cần thống kê.
    """
    try:
        path = Path(directory_path)
        if not path.exists():
            return f"❌ Thư mục {directory_path} không tồn tại."
        
        # Quét tất cả file (loại trừ các thư mục ẩn và vendor/node_modules để nhanh hơn)
        files = []
        for f in path.rglob('*'):
            if f.is_file() and not any(part.startswith('.') or part in ['vendor', 'node_modules'] for part in f.parts):
                files.append(f)
        
        file_count = len(files)
        
        if files:
            latest_file = max(files, key=lambda f: f.stat().st_mtime)
            mtime = datetime.fromtimestamp(latest_file.stat().st_mtime).strftime('%d/%m/%Y %H:%M:%S')
            return (
                f"📊 **Báo cáo tiến độ cho {path.name}:**\n"
                f"- Tổng số file code: {file_count}\n"
                f"- File cập nhật cuối: `{latest_file.name}`\n"
                f"- Thời gian: {mtime}\n"
                f"Davis thấy bạn đang làm rất tốt! 🚀"
            )
        
        return f"📊 Thư mục {path.name} hiện đang trống."
    except Exception as e:
        return f"❌ Lỗi thống kê: {str(e)}"

def save_memory(key: str, value: str) -> str:
    """
    Lưu trữ một thông tin quan trọng vào bộ nhớ lâu dài.
    Args:
        key: Tên thông tin (ví dụ: 'sinh nhật của Nam', 'project_status')
        value: Nội dung cần nhớ.
    """
    return memory.store(key, value)

def get_memory(key: str) -> str:
    """
    Lấy lại thông tin đã lưu từ bộ nhớ.
    Args:
        key: Tên thông tin cần tìm.
    """
    return memory.retrieve(key)

def list_memories() -> str:
    """
    Liệt kê tất cả các thông tin đang có trong bộ nhớ.
    """
    return memory.list_all()
