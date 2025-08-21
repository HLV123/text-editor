import json
from pathlib import Path

class Config:
    def __init__(self):
        self.config_dir = Path.home() / '.text_editor'
        self.config_file = self.config_dir / 'config.json'
        self.data = self.load()
    
    def load(self):
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        
        return {
            'font_family': 'Consolas',
            'font_size': 12,
            'theme': 'light',
            'window': {
                'width': 1000,
                'height': 700,
                'x': 100,
                'y': 100
            },
            'recent_files': []
        }
    
    def save(self):
        try:
            self.config_dir.mkdir(exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def get(self, key, default=None):
        keys = key.split('.')
        value = self.data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key, value):
        keys = key.split('.')
        data = self.data
        for k in keys[:-1]:
            if k not in data:
                data[k] = {}
            data = data[k]
        data[keys[-1]] = value
    
    def add_recent_file(self, filepath):
        recent = self.get('recent_files', [])
        if filepath in recent:
            recent.remove(filepath)
        recent.insert(0, filepath)
        self.set('recent_files', recent[:10])
    
    def get_recent_files(self):
        import os
        recent = self.get('recent_files', [])
        return [f for f in recent if os.path.exists(f)]