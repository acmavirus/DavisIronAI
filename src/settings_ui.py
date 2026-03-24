import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import requests
from dotenv import load_dotenv, set_key
from pathlib import Path
from PIL import Image, ImageTk, ImageDraw, ImageOps

class SettingsApp:
    def __init__(self):
        self.base_path = Path.cwd()

        self.env_path = self.base_path / ".env"
        if not self.env_path.exists():
            with open(self.env_path, "w", encoding="utf-8") as f:
                f.write("GEMINI_API_KEY=\nTELEGRAM_BOT_TOKEN=\nWHITELIST_USER_ID=\nAPP_VERSION=1.0.0\nGITHUB_REPO=acmavirus/DavisIronAI\nLOGO_URL=https://ws.io.vn/logo.png\nICON_URL=https://ws.io.vn/icon.ico\n")
        
        load_dotenv(self.env_path, override=True)
        
        # Tự động tải logo/icon nếu chưa có hoặc có URL mặc định
        self._ensure_brand_assets()
        
        self.root = tk.Tk()
        self.root.title("Davis Iron AI - Settings")
        self.root.geometry("520x650")
        self.root.configure(bg="#1E1E2E")
        self.root.resizable(True, True)
        
        # Set Icon
        try:
            icon_path = self.base_path / "assets" / "icon.ico"
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
            
            logo_path = self.base_path / "assets" / "logo.png"
            if logo_path.exists():
                logo_img = Image.open(logo_path)
                self.icon_photo = ImageTk.PhotoImage(logo_img)
                self.root.tk.call('wm', 'iconphoto', self.root._w, self.icon_photo)
        except Exception as e:
            print(f"Icon error: {e}")
        
        # Style
        self.colors = {
            "bg": "#1E1E2E",
            "frame": "#24273A",
            "entry": "#363A4F",
            "text": "#CAD3F5",
            "accent": "#8AADF4",
            "button": "#A6DA95",
            "button_fg": "#11111B",
            "placeholder": "#6E738D"
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header với Logo
        header_frame = tk.Frame(self.root, bg=self.colors["bg"], pady=30)
        header_frame.pack(fill="x")
        
        try:
            logo_path = self.base_path / "assets" / "logo.png"
            if logo_path.exists():
                img = Image.open(logo_path).resize((100, 100), Image.Resampling.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img)
                tk.Label(header_frame, image=self.logo_img, bg=self.colors["bg"]).pack()
        except Exception:
            pass

        tk.Label(header_frame, text="DAVIS IRON AI", font=("Segoe UI", 18, "bold"), fg=self.colors["accent"], bg=self.colors["bg"]).pack(pady=(10, 0))
        tk.Label(header_frame, text="CẤU HÌNH HỆ THỐNG", font=("Segoe UI", 9), fg=self.colors["placeholder"], bg=self.colors["bg"]).pack()
        
        # Create a container for the form
        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(fill="both", expand=True)

        self.scrollable_frame = tk.Frame(container, bg=self.colors["bg"], padx=40)
        self.scrollable_frame.pack(fill="both", expand=True)

        self.entries = {}
        fields = [
            ("DATA_DIR", "Thư mục lưu dữ liệu:"),
            ("GEMINI_API_KEY", "Gemini API Key:"),
            ("TELEGRAM_BOT_TOKEN", "Telegram Bot Token:"),
            ("WHITELIST_USER_ID", "Whitelist User ID:"),
            ("GITHUB_REPO", "GitHub Repository:"),
            ("APP_VERSION", "Phiên bản hiện tại:")
        ]
        
        for key, label_text in fields:
            lbl = tk.Label(self.scrollable_frame, text=label_text, anchor="w", fg=self.colors["text"], bg=self.colors["bg"], font=("Segoe UI", 10))
            lbl.pack(fill="x", pady=(10, 0))
            
            ent = tk.Entry(
                self.scrollable_frame, 
                bg=self.colors["entry"], 
                fg=self.colors["text"], 
                insertbackground="white", 
                relief="flat", 
                font=("Consolas", 11),
                highlightthickness=1,
                highlightbackground=self.colors["entry"],
                highlightcolor=self.colors["accent"]
            )
            
            if key == "DATA_DIR":
                val = str(self.base_path)
                ent.insert(0, val)
                ent.config(state="readonly", fg=self.colors["placeholder"])
            else:
                val = os.getenv(key, "")
                ent.insert(0, val)
                
            ent.pack(fill="x", pady=(2, 10), ipady=7)
            self.entries[key] = ent
            
        # Footer & Save Button
        save_frame = tk.Frame(self.root, bg=self.colors["bg"], pady=20, padx=40)
        save_frame.pack(fill="x", side="bottom")
        
        self.btn_save = tk.Button(
            save_frame, 
            text="LƯU & KHỞI ĐỘNG", 
            command=self.save, 
            bg=self.colors["button"], 
            fg=self.colors["button_fg"], 
            relief="flat", 
            font=("Segoe UI", 11, "bold"), 
            cursor="hand2",
            activebackground="#8BD5CA"
        )
        self.btn_save.pack(fill="x", ipady=10)
        
        def on_hover(e): self.btn_save['bg'] = '#8BD5CA'
        def on_leave(e): self.btn_save['bg'] = self.colors["button"]
        
        self.btn_save.bind("<Enter>", on_hover)
        self.btn_save.bind("<Leave>", on_leave)

        # Exit Button
        self.btn_exit = tk.Button(
            save_frame, 
            text="THOÁT ỨNG DỤNG", 
            command=self.exit_system, 
            bg="#ED8796", 
            fg=self.colors["button_fg"], 
            relief="flat", 
            font=("Segoe UI", 10, "bold"), 
            cursor="hand2",
            activebackground="#EE99A0"
        )
        self.btn_exit.pack(fill="x", ipady=5, pady=(10, 0))

    def _ensure_brand_assets(self):
        """Đảm bảo logo và icon có sẵn bằng cách tải từ URL mặc định"""
        logo_url = os.getenv("LOGO_URL", "https://ws.io.vn/logo.png")
        icon_url = os.getenv("ICON_URL", "https://ws.io.vn/icon.ico")
        
        logo_path = self.base_path / "assets" / "logo.png"
        icon_path = self.base_path / "assets" / "icon.ico"
        
        if not logo_path.exists():
            self._download_asset(logo_url, "logo.png")
        if not icon_path.exists():
            self._download_asset(icon_url, "icon.ico")

    def _download_asset(self, url, filename):
        """Tải file từ URL về thư mục assets"""
        if not url or not url.startswith("http"):
            return
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                assets_dir = self.base_path / "assets"
                assets_dir.mkdir(exist_ok=True)
                with open(assets_dir / filename, "wb") as f:
                    f.write(r.content)
                return True
        except Exception as e:
            print(f"Lỗi tải {filename} từ {url}: {e}")
        return False

    def exit_system(self):
        if messagebox.askokcancel("Xác nhận", "Bạn có chắc chắn muốn thoát hoàn toàn ứng dụng?"):
            sys.exit(0)

    def save(self):
        try:
            for key, entry in self.entries.items():
                if key == "DATA_DIR":
                    continue
                value = entry.get()
                set_key(str(self.env_path), key, value)
            
            messagebox.showinfo("Thành công", "Cấu hình đã được cập nhật thành công!\nỨng dụng sẽ chuyển sang dạng bong bóng nổi.")
            
            # Thay vì đóng hẳn, ta ẩn cửa sổ chính và hiện bong bóng
            self.root.withdraw()
            FloatingBubble(self.root, self.base_path, self)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu cấu hình: {e}")

    def run(self):
        # Centers window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Nếu đã có đầy đủ cấu hình, tự động chuyển sang dạng bong bóng sau khi khởi động
        if os.getenv("GEMINI_API_KEY") and os.getenv("TELEGRAM_BOT_TOKEN"):
            self.root.after(100, self.auto_bubble)
            
        self.root.mainloop()

    def auto_bubble(self):
        self.root.withdraw()
        FloatingBubble(self.root, self.base_path, self)

class FloatingBubble:
    def __init__(self, parent, base_path, app_instance):
        self.parent = parent
        self.app_instance = app_instance
        self.bubble = tk.Toplevel(parent)
        self.bubble.overrideredirect(True) # Xóa thanh tiêu đề
        self.bubble.attributes("-topmost", True)
        self.bubble.geometry("60x60+100+100")
        self.bubble.configure(bg="#1E1E2E")
        
        # Transparent window support
        self.trans_color = "#f0f0f0"
        self.bubble.configure(bg=self.trans_color)
        self.bubble.attributes("-transparentcolor", self.trans_color)
        
        # Create label first (fallback to text if logo fails)
        self.label = tk.Label(
            self.bubble, 
            text="DI", 
            font=("Segoe UI", 12, "bold"), 
            fg="#8AADF4", 
            bg=self.trans_color, 
            cursor="fleur"
        )
        self.label.pack(expand=True, fill="both")
        
        # Apply Bindings immediately
        self.label.bind("<Button-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)
        self.label.bind("<ButtonRelease-1>", self.stop_move)
        
        # Menu
        self.menu = tk.Menu(self.bubble, tearoff=0, bg="#24273A", fg="#CAD3F5", activebackground="#8AADF4", relief="flat")
        self.menu.add_command(label="⚙️ Cài đặt", command=self.show_settings)
        self.menu.add_separator()
        self.menu.add_command(label="❌ Thoát", command=self.exit_app)
        self.label.bind("<Button-3>", self.show_menu)

        # Attempt to load and crop logo to circle
        try:
            # Use current working directory (the data dir) as primary source
            logo_path = Path.cwd() / "assets" / "logo.png"
            
            if logo_path.exists():
                size = (55, 55)
                # Load and Resize
                img = Image.open(str(logo_path)).convert("RGBA").resize(size, Image.Resampling.LANCZOS)
                
                # Create circular mask
                mask = Image.new("L", size, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, size[0], size[1]), fill=255)
                
                # Apply mask to the logo
                circular_img = Image.new("RGBA", size, (0, 0, 0, 0))
                circular_img.paste(img, (0, 0), mask=mask)
                
                # Convert to PhotoImage and keep reference
                self.photo = ImageTk.PhotoImage(circular_img)
                self.label.config(image=self.photo, text="")
        except Exception as e:
                # Fallback silently or print to console if available
                print(f"Error loading circular bubble logo: {e}")

    def start_move(self, event):
        self.x = event.x
        self.y = event.y
        self.moved = False

    def do_move(self, event):
        if abs(event.x - self.x) > 3 or abs(event.y - self.y) > 3:
            self.moved = True
        
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.bubble.winfo_x() + deltax
        y = self.bubble.winfo_y() + deltay
        self.bubble.geometry(f"+{x}+{y}")

    def stop_move(self, event):
        if not self.moved:
            self.show_settings()

    def show_settings(self, event=None):
        self.bubble.withdraw()
        self.parent.deiconify()

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def exit_app(self):
        sys.exit(0)

if __name__ == "__main__":
    app = SettingsApp()
    app.run()
