import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from converter import Converter

class ConverterDialog:
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.converter = Converter()
        
        self.window = tk.Toplevel(parent)
        self.window.title("Chuyển đổi dữ liệu")
        self.window.geometry("800x600")
        self.window.transient(parent)
        self.window.resizable(True, True)
        
        self.create_widgets()
        self.center_window()
    
    def create_widgets(self):
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_url_tab(notebook)
        self.create_base64_tab(notebook)
        self.create_case_tab(notebook)
        self.create_encoding_tab(notebook)
        self.create_format_tab(notebook)
        
        button_frame = tk.Frame(self.window)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        tk.Button(button_frame, text="Đóng", command=self.close).pack(side=tk.RIGHT)
        
        self.window.protocol("WM_DELETE_WINDOW", self.close)
    
    def create_url_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="URL")
        
        tk.Label(frame, text="Văn bản:").pack(anchor=tk.W, padx=5, pady=5)
        self.url_input = scrolledtext.ScrolledText(frame, height=8)
        self.url_input.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(btn_frame, text="Encode", command=self.url_encode).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Decode", command=self.url_decode).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Lấy từ editor", command=lambda: self.get_from_editor(self.url_input)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Đưa vào editor", command=lambda: self.put_to_editor(self.url_input)).pack(side=tk.LEFT, padx=5)
    
    def create_base64_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Base64")
        
        tk.Label(frame, text="Văn bản:").pack(anchor=tk.W, padx=5, pady=5)
        self.base64_input = scrolledtext.ScrolledText(frame, height=8)
        self.base64_input.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(btn_frame, text="Encode", command=self.base64_encode).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Decode", command=self.base64_decode).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Lấy từ editor", command=lambda: self.get_from_editor(self.base64_input)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Đưa vào editor", command=lambda: self.put_to_editor(self.base64_input)).pack(side=tk.LEFT, padx=5)
    
    def create_case_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Chữ hoa/thường")
        
        tk.Label(frame, text="Văn bản:").pack(anchor=tk.W, padx=5, pady=5)
        self.case_input = scrolledtext.ScrolledText(frame, height=8)
        self.case_input.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(btn_frame, text="UPPERCASE", command=self.to_uppercase).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="lowercase", command=self.to_lowercase).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Title Case", command=self.to_title_case).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="camelCase", command=self.to_camel_case).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="snake_case", command=self.to_snake_case).pack(side=tk.LEFT, padx=2)
        
        btn_frame2 = tk.Frame(frame)
        btn_frame2.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(btn_frame2, text="Lấy từ editor", command=lambda: self.get_from_editor(self.case_input)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame2, text="Đưa vào editor", command=lambda: self.put_to_editor(self.case_input)).pack(side=tk.LEFT, padx=5)
    
    def create_encoding_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Encoding")
        
        tk.Label(frame, text="Văn bản:").pack(anchor=tk.W, padx=5, pady=5)
        self.encoding_input = scrolledtext.ScrolledText(frame, height=6)
        self.encoding_input.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        control_frame = tk.Frame(frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(control_frame, text="Từ:").pack(side=tk.LEFT, padx=5)
        self.from_encoding = ttk.Combobox(control_frame, width=12, state='readonly')
        self.from_encoding['values'] = ['auto', 'utf-8', 'utf-16', 'ascii', 'latin-1', 'windows-1252', 'iso-8859-1']
        self.from_encoding.set('auto')
        self.from_encoding.pack(side=tk.LEFT, padx=5)
        
        tk.Label(control_frame, text="Đến:").pack(side=tk.LEFT, padx=5)
        self.to_encoding = ttk.Combobox(control_frame, width=12, state='readonly')
        self.to_encoding['values'] = ['utf-8', 'utf-16', 'ascii', 'latin-1', 'windows-1252', 'iso-8859-1']
        self.to_encoding.set('utf-8')
        self.to_encoding.pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="Chuyển đổi", command=self.convert_encoding).pack(side=tk.LEFT, padx=5)
        
        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(btn_frame, text="Lấy từ editor", command=lambda: self.get_from_editor(self.encoding_input)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Đưa vào editor", command=lambda: self.put_to_editor(self.encoding_input)).pack(side=tk.LEFT, padx=5)
    
    def create_format_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Format")
        
        tk.Label(frame, text="Dữ liệu nguồn:").pack(anchor=tk.W, padx=5, pady=5)
        self.format_input = scrolledtext.ScrolledText(frame, height=8)
        self.format_input.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(btn_frame, text="CSV → JSON", command=self.csv_to_json).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="CSV → XML", command=self.csv_to_xml).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="JSON → XML", command=self.json_to_xml).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="XML → JSON", command=self.xml_to_json).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="JSON → YAML", command=self.json_to_yaml).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="YAML → JSON", command=self.yaml_to_json).pack(side=tk.LEFT, padx=2)
        
        btn_frame2 = tk.Frame(frame)
        btn_frame2.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(btn_frame2, text="Lấy từ editor", command=lambda: self.get_from_editor(self.format_input)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame2, text="Đưa vào editor", command=lambda: self.put_to_editor(self.format_input)).pack(side=tk.LEFT, padx=5)
    
    def get_from_editor(self, text_widget):
        text_editor = self.main_window.tab_manager.get_current_text_widget()
        if text_editor:
            try:
                selected_text = text_editor.selection_get()
                text_widget.delete('1.0', tk.END)
                text_widget.insert('1.0', selected_text)
            except:
                content = text_editor.get('1.0', tk.END + '-1c')
                text_widget.delete('1.0', tk.END)
                text_widget.insert('1.0', content)
    
    def put_to_editor(self, text_widget):
        text_editor = self.main_window.tab_manager.get_current_text_widget()
        if text_editor:
            content = text_widget.get('1.0', tk.END + '-1c')
            try:
                text_editor.delete(tk.SEL_FIRST, tk.SEL_LAST)
                text_editor.insert(tk.INSERT, content)
            except:
                text_editor.delete('1.0', tk.END)
                text_editor.insert('1.0', content)
    
    def url_encode(self):
        text = self.url_input.get('1.0', tk.END + '-1c')
        result = self.converter.url_encode(text)
        self.url_input.delete('1.0', tk.END)
        self.url_input.insert('1.0', result)
    
    def url_decode(self):
        text = self.url_input.get('1.0', tk.END + '-1c')
        result = self.converter.url_decode(text)
        self.url_input.delete('1.0', tk.END)
        self.url_input.insert('1.0', result)
    
    def base64_encode(self):
        text = self.base64_input.get('1.0', tk.END + '-1c')
        result = self.converter.base64_encode(text)
        self.base64_input.delete('1.0', tk.END)
        self.base64_input.insert('1.0', result)
    
    def base64_decode(self):
        text = self.base64_input.get('1.0', tk.END + '-1c')
        result = self.converter.base64_decode(text)
        self.base64_input.delete('1.0', tk.END)
        self.base64_input.insert('1.0', result)
    
    def to_uppercase(self):
        text = self.case_input.get('1.0', tk.END + '-1c')
        result = self.converter.to_uppercase(text)
        self.case_input.delete('1.0', tk.END)
        self.case_input.insert('1.0', result)
    
    def to_lowercase(self):
        text = self.case_input.get('1.0', tk.END + '-1c')
        result = self.converter.to_lowercase(text)
        self.case_input.delete('1.0', tk.END)
        self.case_input.insert('1.0', result)
    
    def to_title_case(self):
        text = self.case_input.get('1.0', tk.END + '-1c')
        result = self.converter.to_title_case(text)
        self.case_input.delete('1.0', tk.END)
        self.case_input.insert('1.0', result)
    
    def to_camel_case(self):
        text = self.case_input.get('1.0', tk.END + '-1c')
        result = self.converter.to_camel_case(text)
        self.case_input.delete('1.0', tk.END)
        self.case_input.insert('1.0', result)
    
    def to_snake_case(self):
        text = self.case_input.get('1.0', tk.END + '-1c')
        result = self.converter.to_snake_case(text)
        self.case_input.delete('1.0', tk.END)
        self.case_input.insert('1.0', result)
    
    def convert_encoding(self):
        text = self.encoding_input.get('1.0', tk.END + '-1c')
        from_enc = self.from_encoding.get()
        to_enc = self.to_encoding.get()
        result = self.converter.convert_encoding(text, from_enc, to_enc)
        self.encoding_input.delete('1.0', tk.END)
        self.encoding_input.insert('1.0', result)
    
    def csv_to_json(self):
        text = self.format_input.get('1.0', tk.END + '-1c')
        result = self.converter.csv_to_json(text)
        self.format_input.delete('1.0', tk.END)
        self.format_input.insert('1.0', result)
    
    def csv_to_xml(self):
        text = self.format_input.get('1.0', tk.END + '-1c')
        result = self.converter.csv_to_xml(text)
        self.format_input.delete('1.0', tk.END)
        self.format_input.insert('1.0', result)
    
    def json_to_xml(self):
        text = self.format_input.get('1.0', tk.END + '-1c')
        result = self.converter.json_to_xml(text)
        self.format_input.delete('1.0', tk.END)
        self.format_input.insert('1.0', result)
    
    def xml_to_json(self):
        text = self.format_input.get('1.0', tk.END + '-1c')
        result = self.converter.xml_to_json(text)
        self.format_input.delete('1.0', tk.END)
        self.format_input.insert('1.0', result)
    
    def json_to_yaml(self):
        text = self.format_input.get('1.0', tk.END + '-1c')
        result = self.converter.json_to_yaml(text)
        self.format_input.delete('1.0', tk.END)
        self.format_input.insert('1.0', result)
    
    def yaml_to_json(self):
        text = self.format_input.get('1.0', tk.END + '-1c')
        result = self.converter.yaml_to_json(text)
        self.format_input.delete('1.0', tk.END)
        self.format_input.insert('1.0', result)
    
    def close(self):
        self.window.destroy()
    
    def center_window(self):
        self.window.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (self.window.winfo_width() // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (self.window.winfo_height() // 2)
        self.window.geometry(f"+{x}+{y}")