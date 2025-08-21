class ThemeManager:
    def __init__(self, config):
        self.config = config
        self.themes = {
            'light': {
                'bg': '#ffffff',
                'fg': '#000000',
                'select_bg': '#0078d4',
                'select_fg': '#ffffff',
                'toolbar_bg': '#f0f0f0',
                'status_bg': '#e1e1e1'
            },
            'dark': {
                'bg': '#1e1e1e',
                'fg': '#ffffff',
                'select_bg': '#264f78',
                'select_fg': '#ffffff',
                'toolbar_bg': '#2d2d30',
                'status_bg': '#007acc'
            },
            'blue': {
                'bg': '#f0f8ff',
                'fg': '#000080',
                'select_bg': '#4169e1',
                'select_fg': '#ffffff',
                'toolbar_bg': '#e6f3ff',
                'status_bg': '#87ceeb'
            },
            'green': {
                'bg': '#f0fff0',
                'fg': '#006400',
                'select_bg': '#228b22',
                'select_fg': '#ffffff',
                'toolbar_bg': '#e6ffe6',
                'status_bg': '#90ee90'
            }
        }
    
    def get_theme(self, name=None):
        if name is None:
            name = self.config.get('theme', 'light')
        return self.themes.get(name, self.themes['light'])
    
    def set_theme(self, name):
        if name in self.themes:
            self.config.set('theme', name)
            return True
        return False
    
    def get_available_themes(self):
        return list(self.themes.keys())
    
    def apply_to_text(self, text_widget):
        theme = self.get_theme()
        try:
            text_widget.config(
                bg=theme['bg'],
                fg=theme['fg'],
                selectbackground=theme['select_bg'],
                selectforeground=theme['select_fg'],
                insertbackground=theme['fg']
            )
        except:
            pass
    
    def apply_to_frame(self, frame):
        theme = self.get_theme()
        try:
            frame.config(bg=theme['toolbar_bg'])
        except:
            pass
    
    def apply_to_status(self, widget):
        theme = self.get_theme()
        try:
            widget.config(
                bg=theme['status_bg'],
                fg=theme['fg']
            )
        except:
            pass