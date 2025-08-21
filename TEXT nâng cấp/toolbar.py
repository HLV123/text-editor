import tkinter as tk
from tkinter import ttk

class Toolbar:
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        
        self.frame = tk.Frame(parent, relief=tk.RAISED, bd=1)
        
        self.create_buttons()
        self.create_font_controls()
    
    def create_buttons(self):
        buttons = [
            ("Tạo mới", self.main_window.new_file),
            ("Mở", self.main_window.open_file),
            ("Lưu", self.main_window.save_file),
            ("---", None),
            ("Cắt", self.main_window.cut),
            ("Sao chép", self.main_window.copy),
            ("Dán", self.main_window.paste),
            ("---", None),
            ("Hoàn tác", self.main_window.undo),
            ("Làm lại", self.main_window.redo),
            ("---", None),
            ("Tìm kiếm", self.main_window.show_find_dialog),
        ]
        
        for text, command in buttons:
            if text == "---":
                separator = tk.Frame(self.frame, width=2, bg='gray', relief=tk.SUNKEN, bd=1)
                separator.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)
            else:
                btn = tk.Button(
                    self.frame,
                    text=text,
                    command=command,
                    relief=tk.FLAT,
                    padx=8,
                    pady=2
                )
                btn.pack(side=tk.LEFT, padx=2, pady=2)
    
    def create_font_controls(self):
        tk.Label(self.frame, text="Font:").pack(side=tk.LEFT, padx=(10, 2))
        
        self.font_var = tk.StringVar(value=self.main_window.config.get('font_family'))
        self.font_combo = ttk.Combobox(
            self.frame,
            textvariable=self.font_var,
            width=15,
            state='readonly'
        )
        self.font_combo['values'] = [
            'Consolas', 'Courier New', 'Liberation Mono', 'Arial', 'Times New Roman',
            'DejaVu Sans Mono', 'Ubuntu Mono', 'Source Code Pro', 'Fira Code', 'JetBrains Mono'
        ]
        self.font_combo.pack(side=tk.LEFT, padx=2)
        self.font_combo.bind('<<ComboboxSelected>>', self.on_font_change)
        
        tk.Label(self.frame, text="Cỡ:").pack(side=tk.LEFT, padx=(5, 2))
        
        self.size_var = tk.StringVar(value=str(self.main_window.config.get('font_size')))
        self.size_combo = ttk.Combobox(
            self.frame,
            textvariable=self.size_var,
            width=5,
            state='readonly'
        )
        self.size_combo['values'] = [
            '8', '9', '10', '11', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30', '32', '36', '40', '48'
        ]
        self.size_combo.pack(side=tk.LEFT, padx=2)
        self.size_combo.bind('<<ComboboxSelected>>', self.on_size_change)
    
    def on_font_change(self, event=None):
        font_family = self.font_var.get()
        self.main_window.config.set('font_family', font_family)
        self.main_window.update_fonts()
    
    def on_size_change(self, event=None):
        try:
            font_size = int(self.size_var.get())
            self.main_window.config.set('font_size', font_size)
            self.main_window.update_fonts()
        except:
            pass
    
    def update_font_display(self):
        self.font_var.set(self.main_window.config.get('font_family'))
        self.size_var.set(str(self.main_window.config.get('font_size')))
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)