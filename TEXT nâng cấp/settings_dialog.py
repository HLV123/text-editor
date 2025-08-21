import tkinter as tk
from tkinter import ttk, messagebox

class SettingsDialog:
    def __init__(self, parent, config, theme_manager, main_window):
        self.parent = parent
        self.config = config
        self.theme_manager = theme_manager
        self.main_window = main_window
        
        self.window = tk.Toplevel(parent)
        self.window.title("Cài đặt")
        self.window.geometry("450x350")
        self.window.transient(parent)
        self.window.resizable(False, False)
        
        self.create_widgets()
        self.load_settings()
        self.center_window()
    
    def create_widgets(self):
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_general_tab(notebook)
        self.create_appearance_tab(notebook)
        
        button_frame = tk.Frame(self.window)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        tk.Button(button_frame, text="Áp dụng", command=self.apply_settings).pack(side=tk.RIGHT, padx=(5, 0))
        tk.Button(button_frame, text="Hủy", command=self.close).pack(side=tk.RIGHT)
        
        self.window.protocol("WM_DELETE_WINDOW", self.close)
    
    def create_general_tab(self, notebook):
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="Chung")
        
        font_group = tk.LabelFrame(general_frame, text="Font chữ", padx=10, pady=10)
        font_group.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(font_group, text="Font:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.font_var = tk.StringVar()
        self.font_combo = ttk.Combobox(font_group, textvariable=self.font_var, width=20, state='readonly')
        self.font_combo['values'] = [
            'Consolas', 'Courier New', 'Liberation Mono', 'Arial', 'Times New Roman',
            'DejaVu Sans Mono', 'Ubuntu Mono', 'Source Code Pro', 'Fira Code', 'JetBrains Mono'
        ]
        self.font_combo.grid(row=0, column=1, padx=(0, 10))
        
        tk.Label(font_group, text="Kích cỡ:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.size_var = tk.IntVar()
        self.size_spin = tk.Spinbox(font_group, from_=8, to=72, textvariable=self.size_var, width=5)
        self.size_spin.grid(row=0, column=3)
        
        file_group = tk.LabelFrame(general_frame, text="File", padx=10, pady=10)
        file_group.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(file_group, text="Xóa danh sách file gần đây", command=self.clear_recent_files).pack(anchor=tk.W)
    
    def create_appearance_tab(self, notebook):
        appearance_frame = ttk.Frame(notebook)
        notebook.add(appearance_frame, text="Giao diện")
        
        theme_group = tk.LabelFrame(appearance_frame, text="Chủ đề", padx=10, pady=10)
        theme_group.pack(fill=tk.X, padx=10, pady=10)
        
        self.theme_var = tk.StringVar()
        themes = [
            ("Sáng", "light"),
            ("Tối", "dark"),
            ("Xanh dương", "blue"),
            ("Xanh lá", "green")
        ]
        
        for text, value in themes:
            tk.Radiobutton(theme_group, text=text, variable=self.theme_var, value=value).pack(anchor=tk.W)
        
        window_group = tk.LabelFrame(appearance_frame, text="Cửa sổ", padx=10, pady=10)
        window_group.pack(fill=tk.X, padx=10, pady=10)
        
        self.remember_window = tk.BooleanVar()
        tk.Checkbutton(window_group, text="Nhớ vị trí và kích thước cửa sổ", 
                      variable=self.remember_window).pack(anchor=tk.W)
    
    def load_settings(self):
        self.font_var.set(self.config.get('font_family', 'Consolas'))
        self.size_var.set(self.config.get('font_size', 12))
        self.theme_var.set(self.config.get('theme', 'light'))
        self.remember_window.set(self.config.get('window.remember', True))
    
    def apply_settings(self):
        self.config.set('font_family', self.font_var.get())
        self.config.set('font_size', self.size_var.get())
        self.config.set('theme', self.theme_var.get())
        self.config.set('window.remember', self.remember_window.get())
        
        self.main_window.update_fonts()
        self.main_window.change_theme(self.theme_var.get())
        
        messagebox.showinfo("Thông báo", "Đã áp dụng cài đặt!")
    
    def clear_recent_files(self):
        result = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa danh sách file gần đây?")
        if result:
            self.config.set('recent_files', [])
            messagebox.showinfo("Thông báo", "Đã xóa danh sách file gần đây")
    
    def close(self):
        self.window.destroy()
    
    def center_window(self):
        self.window.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (self.window.winfo_width() // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (self.window.winfo_height() // 2)
        self.window.geometry(f"+{x}+{y}")