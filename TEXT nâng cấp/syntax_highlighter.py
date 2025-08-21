import tkinter as tk
import re

class SyntaxHighlighter:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.language = 'text'
        
        self.python_keywords = {
            'keyword': ['def', 'class', 'if', 'elif', 'else', 'while', 'for', 'try', 'except', 'finally', 
                       'with', 'as', 'import', 'from', 'return', 'yield', 'break', 'continue', 'pass',
                       'and', 'or', 'not', 'in', 'is', 'lambda', 'global', 'nonlocal', 'assert', 'del',
                       'True', 'False', 'None'],
            'builtin': ['print', 'len', 'range', 'str', 'int', 'float', 'list', 'dict', 'tuple', 'set',
                       'type', 'isinstance', 'hasattr', 'getattr', 'setattr', 'open', 'enumerate', 'zip',
                       'map', 'filter', 'all', 'any', 'sum', 'max', 'min', 'sorted', 'reversed']
        }
        
        self.js_keywords = {
            'keyword': ['function', 'var', 'let', 'const', 'if', 'else', 'for', 'while', 'do', 'switch',
                       'case', 'default', 'break', 'continue', 'return', 'try', 'catch', 'finally',
                       'throw', 'new', 'this', 'typeof', 'instanceof', 'delete', 'void', 'in',
                       'true', 'false', 'null', 'undefined'],
            'builtin': ['console', 'document', 'window', 'alert', 'prompt', 'confirm', 'setTimeout',
                       'setInterval', 'JSON', 'Array', 'Object', 'String', 'Number', 'Boolean',
                       'Date', 'Math', 'RegExp']
        }
        
        self.html_tags = ['html', 'head', 'body', 'title', 'meta', 'link', 'script', 'style',
                         'div', 'span', 'p', 'a', 'img', 'ul', 'ol', 'li', 'table', 'tr', 'td', 'th',
                         'form', 'input', 'button', 'textarea', 'select', 'option', 'label',
                         'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'br', 'hr', 'strong', 'em', 'b', 'i']
        
        self.css_properties = ['color', 'background', 'font-size', 'font-family', 'margin', 'padding',
                              'border', 'width', 'height', 'display', 'position', 'top', 'left',
                              'right', 'bottom', 'float', 'clear', 'text-align', 'line-height',
                              'font-weight', 'text-decoration', 'overflow', 'z-index']
        
        self.setup_tags()
    
    def setup_tags(self):
        try:
            current_font = self.text_widget.cget('font')
            if isinstance(current_font, tuple):
                font_family = current_font[0]
                font_size = current_font[1]
            else:
                font_family = 'Consolas'
                font_size = 12
        except:
            font_family = 'Consolas'
            font_size = 12
        
        self.text_widget.tag_configure('keyword', foreground='#0000FF', font=(font_family, font_size, 'bold'))
        self.text_widget.tag_configure('builtin', foreground='#795E26')
        self.text_widget.tag_configure('string', foreground='#A31515')
        self.text_widget.tag_configure('comment', foreground='#008000', font=(font_family, font_size, 'italic'))
        self.text_widget.tag_configure('number', foreground='#0070C1')
        self.text_widget.tag_configure('tag', foreground='#800000')
        self.text_widget.tag_configure('attribute', foreground='#FF0000')
        self.text_widget.tag_configure('property', foreground='#0451A5')
    
    def detect_language(self, filename):
        if not filename:
            return 'text'
        
        ext = filename.lower().split('.')[-1]
        language_map = {
            'py': 'python',
            'js': 'javascript',
            'html': 'html',
            'htm': 'html',
            'css': 'css',
            'txt': 'text'
        }
        return language_map.get(ext, 'text')
    
    def set_language(self, language):
        self.language = language
        self.highlight_all()
    
    def highlight_all(self):
        content = self.text_widget.get('1.0', tk.END)
        
        for tag in ['keyword', 'builtin', 'string', 'comment', 'number', 'tag', 'attribute', 'property']:
            self.text_widget.tag_remove(tag, '1.0', tk.END)
        
        if self.language == 'python':
            self.highlight_python(content)
        elif self.language == 'javascript':
            self.highlight_javascript(content)
        elif self.language == 'html':
            self.highlight_html(content)
        elif self.language == 'css':
            self.highlight_css(content)
    
    def highlight_python(self, content):
        self.highlight_strings(content, ['"', "'", '"""', "'''"])
        self.highlight_comments(content, '#')
        self.highlight_numbers(content)
        self.highlight_keywords(content, self.python_keywords['keyword'], 'keyword')
        self.highlight_keywords(content, self.python_keywords['builtin'], 'builtin')
    
    def highlight_javascript(self, content):
        self.highlight_strings(content, ['"', "'", '`'])
        self.highlight_comments(content, '//')
        self.highlight_multiline_comments(content, '/*', '*/')
        self.highlight_numbers(content)
        self.highlight_keywords(content, self.js_keywords['keyword'], 'keyword')
        self.highlight_keywords(content, self.js_keywords['builtin'], 'builtin')
    
    def highlight_html(self, content):
        self.highlight_html_tags(content)
        self.highlight_html_attributes(content)
        self.highlight_strings(content, ['"', "'"])
        self.highlight_html_comments(content)
    
    def highlight_css(self, content):
        self.highlight_css_properties(content)
        self.highlight_css_values(content)
        self.highlight_strings(content, ['"', "'"])
        self.highlight_css_comments(content)
    
    def highlight_strings(self, content, delimiters):
        for delimiter in delimiters:
            if delimiter in ['"""', "'''"]:
                pattern = re.escape(delimiter) + r'.*?' + re.escape(delimiter)
                for match in re.finditer(pattern, content, re.DOTALL):
                    start_idx = self.get_index_from_offset(match.start())
                    end_idx = self.get_index_from_offset(match.end())
                    self.text_widget.tag_add('string', start_idx, end_idx)
            else:
                pattern = re.escape(delimiter) + r'[^' + re.escape(delimiter) + r']*' + re.escape(delimiter)
                for match in re.finditer(pattern, content):
                    start_idx = self.get_index_from_offset(match.start())
                    end_idx = self.get_index_from_offset(match.end())
                    self.text_widget.tag_add('string', start_idx, end_idx)
    
    def highlight_comments(self, content, comment_char):
        lines = content.split('\n')
        for line_num, line in enumerate(lines):
            comment_pos = line.find(comment_char)
            if comment_pos != -1:
                start_idx = f"{line_num + 1}.{comment_pos}"
                end_idx = f"{line_num + 1}.{len(line)}"
                self.text_widget.tag_add('comment', start_idx, end_idx)
    
    def highlight_multiline_comments(self, content, start_delim, end_delim):
        pattern = re.escape(start_delim) + r'.*?' + re.escape(end_delim)
        for match in re.finditer(pattern, content, re.DOTALL):
            start_idx = self.get_index_from_offset(match.start())
            end_idx = self.get_index_from_offset(match.end())
            self.text_widget.tag_add('comment', start_idx, end_idx)
    
    def highlight_numbers(self, content):
        pattern = r'\b\d+\.?\d*\b'
        for match in re.finditer(pattern, content):
            start_idx = self.get_index_from_offset(match.start())
            end_idx = self.get_index_from_offset(match.end())
            self.text_widget.tag_add('number', start_idx, end_idx)
    
    def highlight_keywords(self, content, keywords, tag):
        for keyword in keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            for match in re.finditer(pattern, content):
                start_idx = self.get_index_from_offset(match.start())
                end_idx = self.get_index_from_offset(match.end())
                self.text_widget.tag_add(tag, start_idx, end_idx)
    
    def highlight_html_tags(self, content):
        pattern = r'</?([a-zA-Z][a-zA-Z0-9]*)'
        for match in re.finditer(pattern, content):
            tag_name = match.group(1).lower()
            if tag_name in self.html_tags:
                start_idx = self.get_index_from_offset(match.start())
                end_idx = self.get_index_from_offset(match.end())
                self.text_widget.tag_add('tag', start_idx, end_idx)
    
    def highlight_html_attributes(self, content):
        pattern = r'\s([a-zA-Z-]+)='
        for match in re.finditer(pattern, content):
            start_idx = self.get_index_from_offset(match.start(1))
            end_idx = self.get_index_from_offset(match.end(1))
            self.text_widget.tag_add('attribute', start_idx, end_idx)
    
    def highlight_html_comments(self, content):
        pattern = r'<!--.*?-->'
        for match in re.finditer(pattern, content, re.DOTALL):
            start_idx = self.get_index_from_offset(match.start())
            end_idx = self.get_index_from_offset(match.end())
            self.text_widget.tag_add('comment', start_idx, end_idx)
    
    def highlight_css_properties(self, content):
        for prop in self.css_properties:
            pattern = r'\b' + re.escape(prop) + r'\s*:'
            for match in re.finditer(pattern, content):
                start_idx = self.get_index_from_offset(match.start())
                end_idx = self.get_index_from_offset(match.start() + len(prop))
                self.text_widget.tag_add('property', start_idx, end_idx)
    
    def highlight_css_values(self, content):
        pattern = r':\s*([^;{}]+)'
        for match in re.finditer(pattern, content):
            start_idx = self.get_index_from_offset(match.start(1))
            end_idx = self.get_index_from_offset(match.end(1))
            self.text_widget.tag_add('string', start_idx, end_idx)
    
    def highlight_css_comments(self, content):
        pattern = r'/\*.*?\*/'
        for match in re.finditer(pattern, content, re.DOTALL):
            start_idx = self.get_index_from_offset(match.start())
            end_idx = self.get_index_from_offset(match.end())
            self.text_widget.tag_add('comment', start_idx, end_idx)
    
    def get_index_from_offset(self, offset):
        content = self.text_widget.get('1.0', tk.END)
        lines = content[:offset].split('\n')
        line = len(lines)
        col = len(lines[-1])
        return f"{line}.{col}"
    
    def on_text_change(self, event=None):
        self.text_widget.after_idle(self.highlight_all)