import tkinter as tk

class MenuBar:
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        
        self.menubar = tk.Menu(parent)
        parent.config(menu=self.menubar)
        
        self.create_file_menu()
        self.create_edit_menu()
        self.create_format_menu()
        self.create_tools_menu()
        self.create_view_menu()
        self.create_help_menu()
    
    def create_file_menu(self):
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)
        
        file_menu.add_command(label="Tạo mới", command=self.main_window.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Mở...", command=self.main_window.open_file, accelerator="Ctrl+O")
        
        recent_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Mở gần đây", menu=recent_menu)
        self.update_recent_menu(recent_menu)
        
        file_menu.add_separator()
        file_menu.add_command(label="Lưu", command=self.main_window.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Lưu với tên...", command=self.main_window.save_as, accelerator="Ctrl+Shift+S")
        
        file_menu.add_separator()
        file_menu.add_command(label="Đóng tab", command=self.main_window.close_current_tab, accelerator="Ctrl+W")
        file_menu.add_command(label="Thoát", command=self.main_window.on_closing, accelerator="Ctrl+Q")
    
    def create_edit_menu(self):
        edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Chỉnh sửa", menu=edit_menu)
        
        edit_menu.add_command(label="Hoàn tác", command=self.main_window.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Làm lại", command=self.main_window.redo, accelerator="Ctrl+Y")
        
        edit_menu.add_separator()
        edit_menu.add_command(label="Cắt", command=self.main_window.cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="Sao chép", command=self.main_window.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="Dán", command=self.main_window.paste, accelerator="Ctrl+V")
        
        edit_menu.add_separator()
        edit_menu.add_command(label="Chọn tất cả", command=self.main_window.select_all, accelerator="Ctrl+A")
        edit_menu.add_command(label="Tìm kiếm...", command=self.main_window.show_find_dialog, accelerator="Ctrl+F")
    
    def create_format_menu(self):
        format_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Định dạng", menu=format_menu)
        
        format_menu.add_command(label="Font...", command=self.main_window.show_font_dialog)
        format_menu.add_command(label="Màu chữ...", command=self.main_window.change_font_color)
        format_menu.add_command(label="Màu nền...", command=self.main_window.change_bg_color)
    
    def create_tools_menu(self):
        tools_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Công cụ", menu=tools_menu)
        
        tools_menu.add_command(label="Chuyển đổi dữ liệu...", command=self.main_window.show_converter)
    
    def create_view_menu(self):
        view_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Xem", menu=view_menu)
        
        zoom_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Zoom", menu=zoom_menu)
        zoom_menu.add_command(label="Phóng to", command=self.main_window.zoom_in, accelerator="Ctrl++")
        zoom_menu.add_command(label="Thu nhỏ", command=self.main_window.zoom_out, accelerator="Ctrl+-")
        zoom_menu.add_command(label="Kích thước gốc", command=self.main_window.reset_zoom, accelerator="Ctrl+0")
        
        view_menu.add_separator()
        
        theme_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Giao diện", menu=theme_menu)
        
        themes = [
            ("Sáng", "light"),
            ("Tối", "dark"),
            ("Xanh dương", "blue"),
            ("Xanh lá", "green")
        ]
        
        for text, value in themes:
            theme_menu.add_command(
                label=text,
                command=lambda t=value: self.main_window.change_theme(t)
            )
        
        view_menu.add_separator()
        view_menu.add_command(label="Toàn màn hình", command=self.main_window.toggle_fullscreen, accelerator="F11")
        view_menu.add_command(label="Cài đặt...", command=self.main_window.show_settings)
    
    def create_help_menu(self):
        help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Trợ giúp", menu=help_menu)
        
        help_menu.add_command(label="Phím tắt", command=self.main_window.show_shortcuts)
        help_menu.add_command(label="Về chương trình", command=self.main_window.show_about)
    
    def update_recent_menu(self, menu):
        menu.delete(0, tk.END)
        recent_files = self.main_window.config.get_recent_files()
        
        if not recent_files:
            menu.add_command(label="(Trống)", state='disabled')
        else:
            for filepath in recent_files:
                import os
                filename = os.path.basename(filepath)
                menu.add_command(
                    label=filename,
                    command=lambda f=filepath: self.main_window.open_recent_file(f)
                )