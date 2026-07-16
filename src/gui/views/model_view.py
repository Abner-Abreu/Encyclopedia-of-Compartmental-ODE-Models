# gui/views/models_view.py
import tkinter as tk
from tkinter import messagebox
from typing import List, Dict, Any

from gui.styles import COLORS, FONTS, SIZES
from gui.components.table import DataTable
from gui.components.model_filters import ModelFilters
from gui.dialogs.model_helper_dialog import ModelHelperDialog

from services import ModelService
from database import Model

class ModelsView:
    def __init__(self, master, model_service: ModelService):
        self.master = master
        self.model_service = model_service
        self.all_models = []
        self._create_widgets()
        self._load_all_models()
    
    def _create_widgets(self):
        self.frame = tk.Frame(self.master, bg=COLORS['background'])
        self.frame.pack(fill='both', expand=True, padx=SIZES['padding'], pady=SIZES['padding'])
        
        title = tk.Label(self.frame, text="Models", font=FONTS['title'], bg=COLORS['background'])
        title.pack(anchor='w', pady=(0, SIZES['padding']))
        
        self.filters = ModelFilters(self.frame, on_filter=self._apply_filters)
        
        button_frame = tk.Frame(self.frame, bg=COLORS['background'])
        button_frame.pack(fill='x', pady=(0, SIZES['padding']))
        
        self.btn_new = tk.Button(
            button_frame, text="➕ Add Model", command=self._open_create_dialog,
            bg=COLORS['primary'], fg=COLORS['light_text'],
            font=FONTS['normal'], relief='flat', padx=20, pady=10, cursor='hand2'
        )
        self.btn_new.pack(side='left')
        
        self.label_counter = tk.Label(
            button_frame, text="", font=FONTS['normal'],
            bg=COLORS['background'], fg=COLORS['primary']
        )
        self.label_counter.pack(side='right')
        
        columns = [
            {'id': 'name', 'text': 'Name', 'width': 250},
            {'id': 'situation', 'text': 'Situation', 'width': 120},
            {'id': 'article', 'text': 'Article', 'width': 120},
            {'id': 'all_lineal', 'text': 'All Lineal', 'width': 120}
        ]
        
        self.table = DataTable(self.frame, columns, height=18)
        self._create_context_menu()
    
    def _create_context_menu(self):
        self.context_menu = tk.Menu(self.master, tearoff=0)
        self.context_menu.add_command(label="Delete", command=self._delete_model)
        self.context_menu.add_command(label="View Details", command=self._view_details)
        self.table.tree.bind("<Button-3>", self._show_context_menu)
    
    def _show_context_menu(self, event):
        item = self.table.tree.identify_row(event.y)
        if item:
            self.table.tree.selection_set(item)
            self.table.selected = item
            self.context_menu.post(event.x_root, event.y_root)
    
    def _load_all_models(self):
        try:
            models = self.model_service.to_list()
            self.all_models = models
            self._display_models(models)
            self.label_counter.config(text=f"📊 Showing {len(self.all_models)} models")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load models: {e}")
            self.all_models = []
            self.table.load_data([])
    
    def _display_models(self, models: List[Model]):
        data = []
        for m in models:
            try:
                situation = self.model_service.get_situation(m.name)['name']
            except:
                situation = "Not found"

            try:
                article = self.model_service.get_article(m.name)['name']
            except:
                article = "Not found"
            
            try:
                params = self.model_service.get_params(m.name)
                all_lineal = "Yes"
                for param in params:
                    if param['lineal'] == False:
                        all_lineal = "NO"
            except:
                all_lineal = "Not found"
            data.append([m.name, situation, article, all_lineal])
        self.table.load_data(data)
    
    def _apply_filters(self, filters: Dict[str, Any]):
        filtered_models = self.model_service.to_list(filters=filters)
        self._display_models(filtered_models)
        self.label_counter.config(
            text=f"Showing {len(filtered_models)} of {len(self.all_models)} models"
        )
    
    def _open_create_dialog(self):
        dialog = ModelHelperDialog(self.master, self.model_service)
        if dialog.result:
            messagebox.showinfo("Success", f"Model '{dialog.result}' created successfully")
        self._load_all_models()
    
    def _delete_model(self, *args):
        selected = self.table.get_selected()
        if not selected:
            messagebox.showwarning("Warning", "Please select a model to delete")
            return
        name = selected[0]
        if not messagebox.askyesno("Confirm Deletion", f"Delete model '{name}'?"):
            return
        try:
            self.model_service.delete(name)
            self._load_all_models()
            messagebox.showinfo("Success", f"Model '{name}' deleted")
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete: {e}")
    
    def _view_details(self):
        selected = self.table.get_selected()
        if not selected:
            messagebox.showwarning("Warning", "Please select a model")
            return
        name = selected[0]
        try:
            model = self.model_service.get_by_id(name)
            model_info = self.model_service.get_all(name)

            details = f"Model: {model_info['name']} \n\n"
            details += "Compartments: \n"
            for compartment in model_info['compartments']:
                details += f"   Name: {compartment['name']} \n"
                details += f"   Expression: {compartment['expression']} \n"
            details += "\n\n"

            details += "Params: \n"
            for params in model_info['params']:
                details += f"   Name: {params['name']}"
                linear = "NO"
                if params['name']:
                    linear = "YES"
                details += f"   Linear: {linear} \n"   
                details += f"   Symbol: {params['symbol']} \n"
                details += f"   Meaning: {params['meaning']} \n"
            details += "\n\n"

            details += "Situation:\n"
            for situation in model_info['situation']:
                details += f"   Name: {situation['name']}\n"
                details += f"   Description: {situation['description']}\n"
            details += "\n\n"

            details += "Article:\n"
            for article in model_info['article']:
                details += f"    Name: {article['name']} \n"  
                details += f"    Author: {article['author']} \n"   
                details += f"    Date: {article['date']} \n" 
            details += "\n\n"

            details += "Data:\n"
            if model_info['data']:
                for data in model_info['data']:
                    details += f"    Name: {data['name']} \n"     
                    details += f"    Date: {data['date']} \n"
                    details += f"    Place: {data['place']} \n" 
            else:
                details += "No data"

            messagebox.showinfo(f"Details: {name}", details)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load details: {e}")