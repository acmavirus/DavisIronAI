import json
import os
from pathlib import Path

class MemoryManager:
    def __init__(self, file_path="data/memory.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self._save_data({})

    def _load_data(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_data(self, data):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def get_raw(self, key: str, default=None):
        data = self._load_data()
        return data.get(key, default)

    def store(self, key: str, value: str):
        data = self._load_data()
        data[key] = value
        self._save_data(data)
        return f"💡 Đã ghi nhớ: {key} = {value}"

    def retrieve(self, key: str):
        data = self._load_data()
        value = data.get(key)
        if value:
            return f"🔍 Thông tin tìm thấy cho '{key}': {value}"
        return f"❓ Xin lỗi, Davis không tìm thấy thông tin cho '{key}'."

    def list_all(self):
        data = self._load_data()
        if not data:
            return "📭 Bộ nhớ hiện tại đang trống."
        summary = "\n".join([f"- {k}: {v}" for k, v in data.items()])
        return f"📋 Danh sách thông tin đã lưu:\n{summary}"

# Instance duy nhất để sử dụng trong actions
memory = MemoryManager()
