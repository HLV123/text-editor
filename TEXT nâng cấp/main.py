#!/usr/bin/env python3

import tkinter as tk
from config import Config
from main_window import MainWindow

def main():
    root = tk.Tk()
    config = Config()
    app = MainWindow(root, config)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        app.on_closing()
    finally:
        config.save()

if __name__ == "__main__":
    main()