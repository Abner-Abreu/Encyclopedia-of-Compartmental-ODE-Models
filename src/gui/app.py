import tkinter as tk

from gui.styles import COLORS, FONTS, SIZES
from gui.views.model_view import ModelsView

class App:
    def __init__(self, root, service):
        self.root = root
        self.root.title("Encyclopedia of Compartmental ODE Models")
        self.root.geometry(f"{SIZES['window_width']}x{SIZES['window_height']}")
        self.root.configure(bg=COLORS['background'])
        
        self.service = service
        
        self._create_widgets()
        self._show_initial_view()
    
    def _create_widgets(self):
        self.content_frame = tk.Frame(self.root, bg=COLORS['background'])
        self.content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        self.views = {}
    
    def _show_initial_view(self):
        self._switch_view('models')
    
    def _switch_view(self, view_id: str):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        if view_id == 'models':
            if 'models' not in self.views:
                self.views['models'] = ModelsView(self.content_frame, self.service)
            else:
                self.views['models']._load_all_models()
                self.views['models'].frame.pack(fill='both', expand=True)