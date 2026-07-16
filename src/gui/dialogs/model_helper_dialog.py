import tkinter as tk
from tkinter import messagebox
from typing import Optional

from .model_dialog import ModelDialog

from services import ServiceHandler

from gui.styles import COLORS, FONTS

class ModelHelperDialog:
    def __init__(self, master, services:ServiceHandler):
        self.master = master
        self.result = None
        self.services = services
        self._create_window()

    def _create_window(self):
        title = "New Model"
        self.window = tk.Toplevel(self.master)
        self.window.title(title)
        
        self.window.resizable(False, False)
        self.window.grab_set()
        self.window.transient(self.master)
        
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.window.winfo_screenheight() // 2) - (200 // 2)
        self.window.geometry(f"+{x}+{y}")
        
        frame = tk.Frame(self.window, bg=COLORS['background'], padx=10, pady=10)
        frame.pack(fill='both', expand=True)
        
        tk.Label(frame, text="Number of Compartments:", font=FONTS['subtitle'], bg=COLORS['background']).pack(anchor='w')
        self.entry_compartments = tk.Entry(frame, font=FONTS['normal'], width=40)
        self.entry_compartments.pack(fill='x', pady=(0, 10))

        tk.Label(frame, text="Number of Params:", font=FONTS['subtitle'], bg=COLORS['background']).pack(anchor='w')
        self.entry_params = tk.Entry(frame, font=FONTS['normal'], width=40)
        self.entry_params.pack(fill='x', pady=(0, 10))

        button_frame = tk.Frame(frame, bg=COLORS['background'])
        button_frame.pack(fill='x', pady=(10, 0))
        
        self.btn_save = tk.Button(
            button_frame, text="Continue", command=self._continue,
            bg=COLORS['primary'], fg=COLORS['light_text'],
            font=FONTS['normal'], relief='flat', padx=20, pady=8, cursor='hand2'
        )
        self.btn_save.pack(side='right', padx=(0, 5))

    def _continue(self):
        try:
            cant_comp = int(self.entry_compartments.get())
            cant_param = int(self.entry_params.get())
            ModelDialog(self.master,self.services,cant_comp,cant_param)
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Validation Error", str(e))
