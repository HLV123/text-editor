import tkinter as tk
from tkinter import messagebox

class FindDialog:
    def __init__(self, parent, text_widget):
        self.parent = parent
        self.text_widget = text_widget
        
        self.window = tk.Toplevel(parent)
        self.window.title("Tìm kiếm")
        self.window.geometry("400x150")
        self.window.transient(parent)
        self.window.resizable(False, False)
        
        self.create_widgets()
        self.center_window()
        
        self.entry.focus_set()
    
    def create_widgets(self):
        tk.Label(self.window, text="Tìm:").pack(pady=5)
        
        self.entry = tk.Entry(self.window, width=40)
        self.entry.pack(pady=5)
        self.entry.bind('<Return>', lambda e: self.find_text())
        
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Tìm", command=self.find_text).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Đóng", command=self.close).pack(side=tk.LEFT, padx=5)
        
        self.window.protocol("WM_DELETE_WINDOW", self.close)
    
    def find_text(self):
        pattern = self.entry.get()
        if not pattern:
            return
        
        self.text_widget.tag_remove('found', '1.0', tk.END)
        
        start = '1.0'
        count = 0
        positions = []
        
        while True:
            pos = self.text_widget.search(pattern, start, tk.END)
            if not pos:
                break
            
            end_pos = f"{pos}+{len(pattern)}c"
            self.text_widget.tag_add('found', pos, end_pos)
            positions.append(pos)
            start = end_pos
            count += 1
        
        if positions:
            self.text_widget.tag_config('found', background='yellow')
            self.text_widget.mark_set(tk.INSERT, positions[0])
            self.text_widget.see(positions[0])
            messagebox.showinfo("Kết quả", f"Tìm thấy {count} kết quả")
        else:
            messagebox.showinfo("Kết quả", "Không tìm thấy")
    
    def close(self):
        self.text_widget.tag_remove('found', '1.0', tk.END)
        self.window.destroy()
    
    def center_window(self):
        self.window.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (self.window.winfo_width() // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (self.window.winfo_height() // 2)
        self.window.geometry(f"+{x}+{y}")