import tkinter as tk
from tkinter import messagebox, colorchooser
import os

from themes import ThemeManager
from tab_manager import TabManager
from file_operations import FileOperations
from toolbar import Toolbar
from menubar import MenuBar
from statusbar import StatusBar
from find_dialog import FindDialog
from settings_dialog import SettingsDialog
from converter_dialog import ConverterDialog

class MainWindow:
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.is_closing = False
        
        self.theme_manager = ThemeManager(config)
        self.file_operations = FileOperations(config)
        
        self.setup_window()
        self.create_widgets()
        self.setup_bindings()
        self.apply_theme()
        
        self.tab_manager.create_tab()
    
    def setup_window(self):
        self.root.title("Text Editor - Python 3.13")
        
        width = self.config.get('window.width', 1000)
        height = self.config.get('window.height', 700)
        x = self.config.get('window.x', 100)
        y = self.config.get('window.y', 100)
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.minsize(600, 400)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        self.menubar = MenuBar(self.root, self)
        self.toolbar = Toolbar(self.root, self)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        
        self.tab_manager = TabManager(self.root, self.config, self.theme_manager)
        self.tab_manager.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.statusbar = StatusBar(self.root, self.config, self.theme_manager, self.tab_manager)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_bindings(self):
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-Shift-S>', lambda e: self.save_as())
        self.root.bind('<Control-w>', lambda e: self.close_current_tab())
        self.root.bind('<Control-q>', lambda e: self.on_closing())
        self.root.bind('<Control-z>', lambda e: self.undo())
        self.root.bind('<Control-y>', lambda e: self.redo())
        self.root.bind('<Control-x>', lambda e: self.cut())
        self.root.bind('<Control-c>', lambda e: self.copy())
        self.root.bind('<Control-v>', lambda e: self.paste())
        self.root.bind('<Control-a>', lambda e: self.select_all())
        self.root.bind('<Control-f>', lambda e: self.show_find_dialog())
        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())
        
        self.root.bind('<Control-plus>', lambda e: self.zoom_in())
        self.root.bind('<Control-equal>', lambda e: self.zoom_in())
        self.root.bind('<Control-minus>', lambda e: self.zoom_out())
        self.root.bind('<Control-0>', lambda e: self.reset_zoom())
        
        self.root.bind_all('<KeyRelease>', self.update_status)
        self.root.bind_all('<Button-1>', self.update_status)
    
    def new_file(self):
        if not self.is_closing:
            self.tab_manager.create_tab()
    
    def open_file(self):
        if self.is_closing:
            return
        
        filename = self.file_operations.open_file_dialog()
        if filename:
            content, error = self.file_operations.read_file(filename)
            if content is not None:
                self.tab_manager.create_tab(filename, content)
                self.statusbar.show_message(f"Đã mở: {os.path.basename(filename)}")
            else:
                messagebox.showerror("Lỗi", f"Không thể mở file: {error}")
    
    def open_recent_file(self, filepath):
        if os.path.exists(filepath):
            content, error = self.file_operations.read_file(filepath)
            if content is not None:
                self.tab_manager.create_tab(filepath, content)
                self.statusbar.show_message(f"Đã mở: {os.path.basename(filepath)}")
            else:
                messagebox.showerror("Lỗi", f"Không thể mở file: {error}")
        else:
            messagebox.showerror("Lỗi", f"File không tồn tại: {filepath}")
    
    def save_file(self):
        tab_id, tab_info = self.tab_manager.get_current_tab()
        if tab_info:
            if self.file_operations.save_tab(tab_info):
                self.tab_manager.update_tab_title(tab_id)
                filename = tab_info['filename']
                if filename:
                    self.statusbar.show_message(f"Đã lưu: {os.path.basename(filename)}")
                    language = tab_info['syntax_highlighter'].detect_language(filename)
                    tab_info['syntax_highlighter'].set_language(language)
                return True
        return False
    
    def save_as(self):
        tab_id, tab_info = self.tab_manager.get_current_tab()
        if tab_info:
            if self.file_operations.save_tab_as(tab_info):
                self.tab_manager.update_tab_title(tab_id)
                filename = tab_info['filename']
                if filename:
                    self.statusbar.show_message(f"Đã lưu: {os.path.basename(filename)}")
                    language = tab_info['syntax_highlighter'].detect_language(filename)
                    tab_info['syntax_highlighter'].set_language(language)
                return True
        return False
    
    def close_current_tab(self):
        return self.tab_manager.close_tab()
    
    def undo(self):
        text_widget = self.tab_manager.get_current_text_widget()
        if text_widget:
            try:
                text_widget.edit_undo()
            except:
                pass
    
    def redo(self):
        text_widget = self.tab_manager.get_current_text_widget()
        if text_widget:
            try:
                text_widget.edit_redo()
            except:
                pass
    
    def cut(self):
        text_widget = self.tab_manager.get_current_text_widget()
        if text_widget:
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(text_widget.selection_get())
                text_widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
            except:
                pass
    
    def copy(self):
        text_widget = self.tab_manager.get_current_text_widget()
        if text_widget:
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(text_widget.selection_get())
            except:
                pass
    
    def paste(self):
        text_widget = self.tab_manager.get_current_text_widget()
        if text_widget:
            try:
                text_widget.insert(tk.INSERT, self.root.clipboard_get())
            except:
                pass
    
    def select_all(self):
        text_widget = self.tab_manager.get_current_text_widget()
        if text_widget:
            text_widget.tag_add(tk.SEL, "1.0", tk.END)
    
    def update_status(self, event=None):
        try:
            self.statusbar.update_info()
        except:
            pass
    
    def zoom_in(self):
        self.tab_manager.zoom_in()
        self.toolbar.update_font_display()
        self.statusbar.show_message("Đã phóng to")
    
    def zoom_out(self):
        self.tab_manager.zoom_out()
        self.toolbar.update_font_display()
        self.statusbar.show_message("Đã thu nhỏ")
    
    def reset_zoom(self):
        self.tab_manager.reset_zoom()
        self.toolbar.update_font_display()
        self.statusbar.show_message("Đã đặt lại kích thước")
    
    def show_find_dialog(self):
        if self.is_closing:
            return
        
        text_widget = self.tab_manager.get_current_text_widget()
        if text_widget:
            FindDialog(self.root, text_widget)
    
    def show_font_dialog(self):
        if self.is_closing:
            return
        
        font_window = tk.Toplevel(self.root)
        font_window.title("Chọn Font")
        font_window.geometry("350x200")
        font_window.transient(self.root)
        font_window.resizable(False, False)
        
        tk.Label(font_window, text="Font:").pack(pady=5)
        font_var = tk.StringVar(value=self.config.get('font_family'))
        font_combo = tk.ttk.Combobox(font_window, textvariable=font_var, 
                                   values=self.toolbar.font_combo['values'], 
                                   state='readonly', width=30)
        font_combo.pack(pady=5)
        
        tk.Label(font_window, text="Kích cỡ:").pack(pady=5)
        size_var = tk.IntVar(value=self.config.get('font_size'))
        size_spin = tk.Spinbox(font_window, from_=8, to=72, textvariable=size_var, width=10)
        size_spin.pack(pady=5)
        
        def apply_font():
            self.config.set('font_family', font_var.get())
            self.config.set('font_size', size_var.get())
            self.toolbar.update_font_display()
            self.update_fonts()
            font_window.destroy()
        
        button_frame = tk.Frame(font_window)
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Áp dụng", command=apply_font).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Hủy", command=font_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def change_font_color(self):
        text_widget = self.tab_manager.get_current_text_widget()
        if not text_widget:
            return
        
        color = colorchooser.askcolor(title="Chọn màu chữ")
        if color[1]:
            try:
                if text_widget.tag_ranges(tk.SEL):
                    text_widget.tag_add("color_change", tk.SEL_FIRST, tk.SEL_LAST)
                    text_widget.tag_config("color_change", foreground=color[1])
                else:
                    text_widget.config(fg=color[1])
            except:
                text_widget.config(fg=color[1])
    
    def change_bg_color(self):
        text_widget = self.tab_manager.get_current_text_widget()
        if not text_widget:
            return
        
        color = colorchooser.askcolor(title="Chọn màu nền")
        if color[1]:
            try:
                if text_widget.tag_ranges(tk.SEL):
                    text_widget.tag_add("bg_change", tk.SEL_FIRST, tk.SEL_LAST)
                    text_widget.tag_config("bg_change", background=color[1])
                else:
                    text_widget.config(bg=color[1])
            except:
                text_widget.config(bg=color[1])
    
    def change_theme(self, theme_name):
        if self.theme_manager.set_theme(theme_name):
            self.apply_theme()
    
    def apply_theme(self):
        try:
            theme = self.theme_manager.get_theme()
            self.root.config(bg=theme['bg'])
            self.tab_manager.apply_theme()
            self.statusbar.apply_theme()
        except:
            pass
    
    def update_fonts(self):
        self.tab_manager.update_fonts()
    
    def toggle_fullscreen(self):
        if self.is_closing:
            return
        
        try:
            is_fullscreen = self.root.attributes('-fullscreen')
            self.root.attributes('-fullscreen', not is_fullscreen)
        except:
            pass
    
    def show_converter(self):
        if not self.is_closing:
            ConverterDialog(self.root, self)
    
    def show_settings(self):
        if not self.is_closing:
            SettingsDialog(self.root, self.config, self.theme_manager, self)
    
    def show_shortcuts(self):
        shortcuts = """Phím tắt:

File:
Ctrl+N - Tạo mới
Ctrl+O - Mở file
Ctrl+S - Lưu
Ctrl+Shift+S - Lưu với tên
Ctrl+W - Đóng tab
Ctrl+Q - Thoát

Chỉnh sửa:
Ctrl+Z - Hoàn tác
Ctrl+Y - Làm lại
Ctrl+X - Cắt
Ctrl+C - Sao chép
Ctrl+V - Dán
Ctrl+A - Chọn tất cả
Ctrl+F - Tìm kiếm

Zoom:
Ctrl++ - Phóng to
Ctrl+- - Thu nhỏ
Ctrl+0 - Kích thước gốc

Khác:
F11 - Toàn màn hình"""
        
        messagebox.showinfo("Phím tắt", shortcuts)
    
    def show_about(self):
        about_text = """Text Editor - Python 3.13

Phiên bản: 3.0 Enhanced
Ngôn ngữ: Python 3.13
GUI: Tkinter

Tính năng:
• Hỗ trợ nhiều tab
• Hiển thị số dòng
• Syntax highlighting
• Zoom in/out
• Thông tin chi tiết
• Tìm kiếm văn bản
• 4 giao diện màu
• Tùy chỉnh font
• Phím tắt đầy đủ
• Tự động lưu cài đặt

Phát triển: 2025"""
        
        messagebox.showinfo("Về chương trình", about_text)
    
    def on_closing(self):
        if self.is_closing:
            return
        
        self.is_closing = True
        
        try:
            geometry = self.root.geometry()
            width, height, x, y = map(int, geometry.replace('x', '+').replace('+', ' ').split())
            self.config.set('window.width', width)
            self.config.set('window.height', height)
            self.config.set('window.x', x)
            self.config.set('window.y', y)
        except:
            pass
        
        if not self.tab_manager.close_all_tabs():
            self.is_closing = False
            return
        
        self.statusbar.destroy()
        self.config.save()
        
        try:
            self.root.quit()
            self.root.destroy()
        except:
            pass