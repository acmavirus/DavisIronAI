import tkinter as tk
from tkinter import ttk, messagebox
import os
from dotenv import load_dotenv, set_key
from pathlib import Path

class SettingsApp:
    def __init__(self):
        self.env_path = Path(".env")
        if not self.env_path.exists():
            with open(self.env_path, "w") as f:
                f.write("GEMINI_API_KEY=\nTELEGRAM_BOT_TOKEN=\nWHITELIST_USER_ID=\nAPP_VERSION=1.0.0\nGITHUB_REPO=acmavirus/DavisIronAI\n")
        
        load_dotenv(self.env_path)
        
        self.root = tk.Tk()
        self.root.title("Davis Iron AI - Settings")
        self.root.geometry("500x450")
        self.root.configure(bg="#1e1e2e")
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", foreground="white", background="#1e1e2e", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"))
        
        self.setup_ui()
        
    def setup_ui(self):
        frame = tk.Frame(self.root, bg="#1e1e2e", padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        tk.Label(frame, text="⚙️ CẤU HÌNH HỆ THỐNG", font=("Segoe UI", 14, "bold"), fg="#89b4fa", bg="#1e1e2e").pack(pady=(0, 20))
        
        self.entries = {}
        fields = [
            ("GEMINI_API_KEY", "Gemini API Key:"),
            ("TELEGRAM_BOT_TOKEN", "Telegram Bot Token:"),
            ("WHITELIST_USER_ID", "Whitelist User ID:"),
            ("GITHUB_REPO", "GitHub Repository:"),
            ("APP_VERSION", "Phiên bản hiện tại:")
        ]
        
        for key, label in fields:
            lbl = tk.Label(frame, text=label, anchor="w", fg="#cdd6f4", bg="#1e1e2e")
            lbl.pack(fill="x", pady=(5, 0))
            
            ent = tk.Entry(frame, bg="#313244", fg="white", insertbackground="white", relief="flat", font=("Consolas", 10))
            ent.insert(0, os.getenv(key, ""))
            ent.pack(fill="x", pady=(0, 10), ipady=5)
            self.entries[key] = ent
            
        btn_save = tk.Button(frame, text="LƯU CẤU HÌNH", command=self.save, bg="#a6e3a1", fg="#11111b", relief="flat", font=("Segoe UI", 10, "bold"), cursor="hand2")
        btn_save.pack(fill="x", pady=(20, 0), ipady=8)
        
        tk.Label(frame, text="* App sẽ khởi động sau khi lưu", font=("Segoe UI", 8), fg="#6c7086", bg="#1e1e2e").pack(pady=5)

    def save(self):
        try:
            for key, entry in self.entries.items():
                value = entry.get()
                set_key(str(self.env_path), key, value)
            messagebox.showinfo("Thành công", "Đã lưu cấu hình vào .env!")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu file: {e}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SettingsApp()
    app.run()
