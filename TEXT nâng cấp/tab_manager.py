import tkinter as tk
from tkinter import ttk, messagebox
import os
from syntax_highlighter import SyntaxHighlighter

class LineNumbers(tk.Canvas):
    def __init__(self, parent, text_widget):
        super().__init__(parent, width=50, highlightthickness=0, bd=0)
        self.text_widget = text_widget
        self.text_widget.bind('<KeyRelease>', self.on_text_change)
        self.text_widget.bind('<Button-1>', self.on_text_change)
        self.text_widget.bind('<MouseWheel>', self.on_text_change)
        self.text_widget.bind('<Configure>', self.on_text_change)
        self.update_line_numbers()
    
    def on_text_change(self, event=None):
        self.after_idle(self.update_line_numbers)
    
    def update_line_numbers(self):
        self.delete('all')
        
        i = self.text_widget.index('@0,0')
        while True:
            dline = self.text_widget.dlineinfo(i)
            if dline is None:
                break
            
            y = dline[1]
            linenum = str(i).split('.')[0]
            self.create_text(2, y, anchor='nw', text=linenum, font=('Consolas', 10), fill='gray')
            i = self.text_widget.index(f'{i}+1line')

class TabManager:
    def __init__(self, parent, config, theme_manager):
        self.parent = parent
        self.config = config
        self.theme_manager = theme_manager
        
        self.notebook = ttk.Notebook(parent)
        self.tabs = {}
        self.tab_counter = 0
        
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.notebook.bind("<Button-3>", self.show_context_menu)
    
    def create_tab(self, filename=None, content=""):
        self.tab_counter += 1
        tab_id = f"tab_{self.tab_counter}"
        
        frame = ttk.Frame(self.notebook)
        
        main_frame = tk.Frame(frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        line_frame = tk.Frame(main_frame)
        line_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        text_frame = tk.Frame(main_frame)
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        text_widget = tk.Text(
            text_frame,
            wrap=tk.WORD,
            undo=True,
            maxundo=50,
            font=(self.config.get('font_family'), self.config.get('font_size'))
        )
        
        line_numbers = LineNumbers(line_frame, text_widget)
        line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        scrollbar_v = ttk.Scrollbar(main_frame, orient=tk.VERTICAL)
        scrollbar_h = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=text_widget.xview)
        
        def on_text_scroll(*args):
            text_widget.yview(*args)
            line_numbers.on_text_change()
        
        def on_scrollbar_scroll(*args):
            scrollbar_v.set(*args)
            line_numbers.on_text_change()
        
        scrollbar_v.config(command=on_text_scroll)
        text_widget.config(yscrollcommand=on_scrollbar_scroll, xscrollcommand=scrollbar_h.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_h.pack(side=tk.BOTTOM, fill=tk.X)
        
        syntax_highlighter = SyntaxHighlighter(text_widget)
        
        if content:
            text_widget.insert('1.0', content)
        
        if filename:
            language = syntax_highlighter.detect_language(filename)
            syntax_highlighter.set_language(language)
        
        tab_name = os.path.basename(filename) if filename else f"Tài liệu {self.tab_counter}"
        
        self.notebook.add(frame, text=tab_name)
        self.notebook.select(frame)
        
        self.tabs[tab_id] = {
            'frame': frame,
            'text_widget': text_widget,
            'line_numbers': line_numbers,
            'syntax_highlighter': syntax_highlighter,
            'filename': filename,
            'modified': False,
            'encoding': 'utf-8'
        }
        
        text_widget.bind('<<Modified>>', lambda e: self.on_text_modified(tab_id))
        text_widget.bind('<KeyRelease>', lambda e: self.on_text_change(tab_id, e))
        text_widget.focus_set()
        
        self.theme_manager.apply_to_text(text_widget)
        
        return tab_id
    
    def get_current_tab(self):
        try:
            if not self.tabs:
                return None, None
            
            current_frame = self.notebook.nametowidget(self.notebook.select())
            for tab_id, tab_info in self.tabs.items():
                if tab_info['frame'] == current_frame:
                    return tab_id, tab_info
        except:
            pass
        return None, None
    
    def get_current_text_widget(self):
        tab_id, tab_info = self.get_current_tab()
        return tab_info['text_widget'] if tab_info else None
    
    def close_tab(self, tab_id=None):
        if tab_id is None:
            tab_id, tab_info = self.get_current_tab()
        else:
            tab_info = self.tabs.get(tab_id)
        
        if not tab_info:
            return False
        
        if tab_info['modified']:
            filename = tab_info['filename']
            name = os.path.basename(filename) if filename else f"Tài liệu {tab_id.split('_')[1]}"
            
            result = messagebox.askyesnocancel(
                "Lưu thay đổi",
                f"Bạn có muốn lưu thay đổi cho '{name}'?"
            )
            
            if result is True:
                from file_operations import FileOperations
                file_ops = FileOperations(self.config)
                if not file_ops.save_tab(tab_info):
                    return False
            elif result is None:
                return False
        
        try:
            self.notebook.forget(tab_info['frame'])
            del self.tabs[tab_id]
        except:
            pass
        
        if not self.tabs:
            self.create_tab()
        
        return True
    
    def close_all_tabs(self):
        tab_ids = list(self.tabs.keys())
        for tab_id in tab_ids:
            if not self.close_tab(tab_id):
                return False
        return True
    
    def on_text_modified(self, tab_id):
        if tab_id in self.tabs:
            tab_info = self.tabs[tab_id]
            is_modified = tab_info['text_widget'].edit_modified()
            
            if is_modified != tab_info['modified']:
                tab_info['modified'] = is_modified
                self.update_tab_title(tab_id)
    
    def on_text_change(self, tab_id, event=None):
        if tab_id in self.tabs:
            tab_info = self.tabs[tab_id]
            tab_info['syntax_highlighter'].on_text_change(event)
    
    def update_tab_title(self, tab_id):
        if tab_id in self.tabs:
            tab_info = self.tabs[tab_id]
            
            if tab_info['filename']:
                name = os.path.basename(tab_info['filename'])
            else:
                name = f"Tài liệu {tab_id.split('_')[1]}"
            
            if tab_info['modified']:
                name = "* " + name
            
            try:
                self.notebook.tab(tab_info['frame'], text=name)
            except:
                pass
    
    def on_tab_changed(self, event=None):
        pass
    
    def show_context_menu(self, event):
        try:
            tab_index = self.notebook.index(f"@{event.x},{event.y}")
            menu = tk.Menu(self.parent, tearoff=0)
            menu.add_command(label="Đóng tab", command=self.close_current_tab)
            menu.add_command(label="Đóng tab khác", command=self.close_other_tabs)
            menu.add_command(label="Đóng tất cả", command=self.close_all_tabs)
            menu.tk_popup(event.x_root, event.y_root)
        except:
            pass
    
    def close_current_tab(self):
        self.close_tab()
    
    def close_other_tabs(self):
        current_tab_id, _ = self.get_current_tab()
        if not current_tab_id:
            return
        
        tabs_to_close = [tab_id for tab_id in self.tabs.keys() if tab_id != current_tab_id]
        for tab_id in tabs_to_close:
            self.close_tab(tab_id)
    
    def update_fonts(self):
        font = (self.config.get('font_family'), self.config.get('font_size'))
        for tab_info in self.tabs.values():
            try:
                tab_info['text_widget'].config(font=font)
                tab_info['syntax_highlighter'].setup_tags()
            except:
                pass
    
    def apply_theme(self):
        for tab_info in self.tabs.values():
            self.theme_manager.apply_to_text(tab_info['text_widget'])
            try:
                theme = self.theme_manager.get_theme()
                tab_info['line_numbers'].config(bg=theme['toolbar_bg'])
            except:
                pass
    
    def zoom_in(self):
        current_size = self.config.get('font_size', 12)
        new_size = min(current_size + 2, 72)
        self.config.set('font_size', new_size)
        self.update_fonts()
    
    def zoom_out(self):
        current_size = self.config.get('font_size', 12)
        new_size = max(current_size - 2, 8)
        self.config.set('font_size', new_size)
        self.update_fonts()
    
    def reset_zoom(self):
        self.config.set('font_size', 12)
        self.update_fonts()
    
    def get_current_tab_info(self):
        tab_id, tab_info = self.get_current_tab()
        if not tab_info:
            return None
        
        text_widget = tab_info['text_widget']
        cursor_pos = text_widget.index(tk.INSERT)
        line, col = cursor_pos.split('.')
        total_lines = int(text_widget.index(tk.END).split('.')[0]) - 1
        
        content = text_widget.get('1.0', tk.END)
        char_count = len(content) - 1
        word_count = len(content.split())
        
        return {
            'line': int(line),
            'column': int(col) + 1,
            'total_lines': total_lines,
            'char_count': char_count,
            'word_count': word_count,
            'encoding': tab_info.get('encoding', 'utf-8'),
            'filename': tab_info.get('filename', '')
        }
    
    def pack(self, **kwargs):
        self.notebook.pack(**kwargs)