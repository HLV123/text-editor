import tkinter as tk
import threading
import time

class StatusBar:
    def __init__(self, parent, config, theme_manager, tab_manager):
        self.parent = parent
        self.config = config
        self.theme_manager = theme_manager
        self.tab_manager = tab_manager
        self.running = True
        
        self.frame = tk.Frame(parent, relief=tk.SUNKEN, bd=1)
        
        self.left_label = tk.Label(self.frame, text="Sẵn sàng", anchor=tk.W)
        self.left_label.pack(side=tk.LEFT, padx=5)
        
        self.info_label = tk.Label(self.frame, text="", anchor=tk.CENTER)
        self.info_label.pack(side=tk.LEFT, expand=True, padx=10)
        
        self.position_label = tk.Label(self.frame, text="Dòng 1, Cột 1", anchor=tk.E)
        self.position_label.pack(side=tk.RIGHT, padx=5)
        
        self.encoding_label = tk.Label(self.frame, text="UTF-8", anchor=tk.E)
        self.encoding_label.pack(side=tk.RIGHT, padx=5)
        
        self.time_label = tk.Label(self.frame, text="", anchor=tk.E)
        self.time_label.pack(side=tk.RIGHT, padx=10)
        
        self.start_time_thread()
    
    def start_time_thread(self):
        def update_time():
            while self.running:
                try:
                    current_time = time.strftime("%H:%M:%S")
                    if self.running and hasattr(self, 'time_label') and self.time_label.winfo_exists():
                        self.time_label.config(text=current_time)
                except:
                    break
                time.sleep(1)
        
        threading.Thread(target=update_time, daemon=True).start()
    
    def show_message(self, message):
        try:
            self.left_label.config(text=message)
        except:
            pass
    
    def update_position(self, line, col):
        try:
            self.position_label.config(text=f"Dòng {line}, Cột {col}")
        except:
            pass
    
    def update_info(self):
        try:
            tab_info = self.tab_manager.get_current_tab_info()
            if tab_info:
                info_text = f"Tổng: {tab_info['total_lines']} dòng | {tab_info['char_count']} ký tự | {tab_info['word_count']} từ"
                self.info_label.config(text=info_text)
                
                self.position_label.config(text=f"Dòng {tab_info['line']}, Cột {tab_info['column']}")
                self.encoding_label.config(text=tab_info['encoding'].upper())
            else:
                self.info_label.config(text="")
                self.position_label.config(text="Dòng 1, Cột 1")
                self.encoding_label.config(text="UTF-8")
        except:
            pass
    
    def apply_theme(self):
        self.theme_manager.apply_to_status(self.left_label)
        self.theme_manager.apply_to_status(self.info_label)
        self.theme_manager.apply_to_status(self.position_label)
        self.theme_manager.apply_to_status(self.encoding_label)
        self.theme_manager.apply_to_status(self.time_label)
        self.theme_manager.apply_to_status(self.frame)
    
    def destroy(self):
        self.running = False
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)