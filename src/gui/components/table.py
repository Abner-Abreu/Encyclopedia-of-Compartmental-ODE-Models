import tkinter as tk
from tkinter import ttk

class DataTable:
    def __init__(self, master, columns: list[dict[str, str]],
                 on_double_click: callable = None,
                 height: int = 15):
        self.master = master
        self.columns = columns
        self.on_double_click = on_double_click
        self.data = []
        
        self.frame = tk.Frame(master)
        self.frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        column_ids = [col['id'] for col in columns]
        self.tree = ttk.Treeview(
            self.frame,
            columns=column_ids,
            show='headings',
            height=height
        )
        
        for col in columns:
            self.tree.heading(col['id'], text=col['text'])
            self.tree.column(col['id'], width=col.get('width', 100), anchor='w')
        
        scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        if on_double_click:
            self.tree.bind('<Double-Button-1>', self._on_double_click)
        
        self.selected = None
        self.tree.bind('<<TreeviewSelect>>', self._on_select)
    
    def _on_select(self, event):
        selection = self.tree.selection()
        self.selected = selection[0] if selection else None
    
    def _on_double_click(self, event):
        if self.selected and self.on_double_click:
            item = self.tree.item(self.selected)
            self.on_double_click(item['values'])
    
    def load_data(self, data: list[list]):
        self.data = data
        self.clear()
        for row in data:
            self.tree.insert('', 'end', values=row)
    
    def add_row(self, row: list):
        self.data.append(row)
        self.tree.insert('', 'end', values=row)
    
    def delete_selected(self):
        if self.selected:
            indices = self.tree.get_children()
            index = indices.index(self.selected)
            self.tree.delete(self.selected)
            if index < len(self.data):
                del self.data[index]
            self.selected = None
            return True
        return False
    
    def get_selected(self) -> list | None:
        if self.selected:
            item = self.tree.item(self.selected)
            return item['values']
        return None
    
    def clear(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.data = []
        self.selected = None