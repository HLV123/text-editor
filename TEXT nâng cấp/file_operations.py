import tkinter as tk
from tkinter import filedialog, messagebox
import os

class FileOperations:
    def __init__(self, config):
        self.config = config
    
    def open_file_dialog(self):
        return filedialog.askopenfilename(
            title="Mở file",
            filetypes=[
                ("Text files", "*.txt"),
                ("Python files", "*.py"),
                ("JavaScript files", "*.js"),
                ("HTML files", "*.html"),
                ("CSS files", "*.css"),
                ("All files", "*.*")
            ]
        )
    
    def save_file_dialog(self):
        return filedialog.asksaveasfilename(
            title="Lưu file",
            filetypes=[
                ("Text files", "*.txt"),
                ("Python files", "*.py"),
                ("JavaScript files", "*.js"),
                ("HTML files", "*.html"),
                ("CSS files", "*.css"),
                ("All files", "*.*")
            ]
        )
    
    def read_file(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return content, None
        except UnicodeDecodeError:
            try:
                with open(filepath, 'r', encoding='latin-1') as f:
                    content = f.read()
                return content, None
            except Exception as e:
                return None, str(e)
        except Exception as e:
            return None, str(e)
    
    def write_file(self, filepath, content):
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, None
        except Exception as e:
            return False, str(e)
    
    def save_tab(self, tab_info):
        if not tab_info['filename']:
            filepath = self.save_file_dialog()
            if not filepath:
                return False
            tab_info['filename'] = filepath
        
        content = tab_info['text_widget'].get('1.0', tk.END + '-1c')
        success, error = self.write_file(tab_info['filename'], content)
        
        if success:
            tab_info['text_widget'].edit_modified(False)
            tab_info['modified'] = False
            self.config.add_recent_file(tab_info['filename'])
            return True
        else:
            messagebox.showerror("Lỗi", f"Không thể lưu file: {error}")
            return False
    
    def save_tab_as(self, tab_info):
        filepath = self.save_file_dialog()
        if not filepath:
            return False
        
        old_filename = tab_info['filename']
        tab_info['filename'] = filepath
        
        if self.save_tab(tab_info):
            return True
        else:
            tab_info['filename'] = old_filename
            return False