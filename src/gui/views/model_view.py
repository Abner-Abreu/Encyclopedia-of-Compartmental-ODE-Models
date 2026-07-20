import tkinter as tk
from tkinter import messagebox

from gui.styles import COLORS, FONTS, SIZES
from gui.components.table import DataTable
from gui.components.model_filters import ModelFilters
from gui.dialogs.model_helper_dialog import ModelHelperDialog

from services import ServiceHandler
from dtos import (ModelDto,
                  FiltersDto)

class ModelsView:
    """
    The main view for displaying and managing models in the encyclopedia.

    This view provides a comprehensive interface for managing models,
    including:
        - A table displaying all models with their situation, article,
          and linearity status
        - Advanced filtering by name, parameter, compartment, situation,
          article, and linearity
        - Add model functionality via a multi-step dialog
        - Delete and view details via context menu (right-click)

    The view interacts with the ServiceHandler to retrieve and manipulate
    data, and uses the DataTable component for display and selection.

    Attributes:
        master: The parent widget.
        service (ServiceHandler): The service handler for database operations.
        all_models (list[ModelDto]): Cache of all models currently loaded.
        filters (ModelFilters): The filter component instance.
        table (DataTable): The data table component.
        context_menu (tk.Menu): Right-click context menu.

    Note:
        The view automatically loads all models upon initialization.
        Filters are applied to the cached data without reloading from
        the database for better performance.
    """

    def __init__(self, master, service: ServiceHandler):
        """
        Initializes the ModelsView.

        Args:
            master: The parent widget.
            service: The ServiceHandler instance for database operations.
        """
        self.master = master
        self.service = service
        self.all_models = []
        self._create_widgets()
        self._load_all_models()

    def _create_widgets(self):
        """
        Creates and arranges all widgets in the view.

        This method builds:
            - The main frame with background color
            - The title label
            - The filter component
            - The button frame with Add Model button
            - The counter label
            - The data table with columns
            - The context menu
        """
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
        """
        Creates the right-click context menu.

        The menu provides options to:
            - Delete the selected model
            - View details of the selected model
        """
        self.context_menu = tk.Menu(self.master, tearoff=0)
        self.context_menu.add_command(label="Delete", command=self._delete_model)
        self.context_menu.add_command(label="View Details", command=self._view_details)
        self.table.tree.bind("<Button-3>", self._show_context_menu)

    def _show_context_menu(self, event):
        """
        Displays the context menu at the mouse position.

        Args:
            event: The mouse event containing the click position.

        Note:
            The menu only appears if a row is clicked. The clicked
            row is automatically selected before showing the menu.
        """
        item = self.table.tree.identify_row(event.y)
        if item:
            self.table.tree.selection_set(item)
            self.table.selected = item
            self.context_menu.post(event.x_root, event.y_root)

    def _load_all_models(self):
        """
        Loads all models from the database via the service.

        This method retrieves all models using the service's to_list()
        method, updates the internal cache, and refreshes the display.
        Any errors are displayed to the user.

        Note:
            The counter label is updated to show the total number of
            models loaded.
        """
        try:
            models = self.service.model.to_list()
            self.all_models = models
            self._display_models(models)
            self.label_counter.config(text=f"📊 Showing {len(self.all_models)} models")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load models: {e}")
            self.all_models = []
            self.table.load_data([])

    def _display_models(self, models: list[ModelDto]):
        """
        Displays a list of models in the data table.

        For each model, this method retrieves:
            - The associated situation name (or "Not found")
            - The associated article name (or "Not found")
            - The linearity status ("Yes", "NO", or "Not found")

        Args:
            models: A list of ModelDto objects to display.
        """
        data = []
        for m in models:
            try:
                situation = self.service.model.get_situation(m.name).name
            except:
                situation = "Not found"
            try:
                article = self.service.model.get_article(m.name).name
            except:
                article = "Not found"
            try:
                params = self.service.model.get_params(m.name)
                all_lineal = "Yes"
                for param in params:
                    if param.linear == False:
                        all_lineal = "NO"
            except:
                all_lineal = "Not found"

            data.append([m.name, situation, article, all_lineal])
        self.table.load_data(data)

    def _apply_filters(self, filters: FiltersDto | None):
        """
        Applies filters to the model list and refreshes the display.

        Args:
            filters: The FiltersDto containing the filter criteria,
                or None for no filters.

        Note:
            The counter label is updated to show the number of filtered
            results relative to the total number of models.
        """
        filtered_models = self.service.model.to_list(filters=filters)
        self._display_models(filtered_models)
        self.label_counter.config(
            text=f"Showing {len(filtered_models)} of {len(self.all_models)} models"
        )

    def _open_create_dialog(self):
        """
        Opens the model creation dialog.

        This method launches the ModelHelperDialog, which guides the user
        through the process of creating a new model with all its associated
        data. On successful completion, the view is refreshed.
        """
        dialog = ModelHelperDialog(self.master, self.service)
        if dialog.result:
            messagebox.showinfo("Success", f"Model '{dialog.result}' created successfully")
        self._load_all_models()

    def _delete_model(self):
        """
        Deletes the currently selected model.

        This method:
            1. Checks if a model is selected
            2. Prompts for confirmation
            3. Deletes the model via the service
            4. Refreshes the view on success

        The method displays appropriate error messages if selection
        is missing or deletion fails.
        """
        selected = self.table.get_selected()
        if not selected:
            messagebox.showwarning("Warning", "Please select a model to delete")
            return
        name = selected[0]
        if not messagebox.askyesno("Confirm Deletion", f"Delete model '{name}'?"):
            return
        try:
            self.service.model.delete(name)
            self._load_all_models()
            messagebox.showinfo("Success", f"Model '{name}' deleted")
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete: {e}")

    def _view_details(self):
        """
        Displays detailed information about the selected model.

        The details include:
            - Model name
            - All compartments (name and expression)
            - All parameters (name, linearity, symbol, meaning)
            - Associated situation (name and description)
            - Associated article (name, author, date)
            - Associated data (name, date, place) or "No data"

        If no model is selected, a warning is shown. If an error occurs
        while retrieving details, an error message is displayed.
        """
        selected = self.table.get_selected()
        if not selected:
            messagebox.showwarning("Warning", "Please select a model")
            return
        name = selected[0]
        try:

            model_info = self.service.model.get_all(name)

            details = f"Model: {model_info.name} \n\n"
            details += "Compartments: \n"
            for compartment in model_info.compartments:
                details += f"   Name: {compartment.name} \n"
                details += f"   Expression: {compartment.expression} \n"
            details += "\n\n"

            details += "Params: \n"
            for params in model_info.params:
                details += f"   Name: {params.name}"
                linear = "NO"
                if params.linear:
                    linear = "YES"
                details += f"   Linear: {linear} \n"
                details += f"   Symbol: {params.symbol} \n"
                details += f"   Meaning: {params.meaning} \n"
            details += "\n\n"

            details += "Situation:\n"
            if model_info.situation:
                details += f"   Name: {model_info.situation.name}\n"
                details += f"   Description: {model_info.situation.description}\n"
            else:
                details += "   Not found"
            details += "\n\n"

            details += "Article:\n"
            if model_info.article:
                details += f"    Name: {model_info.article.name} \n"
                details += f"    Author: {model_info.article.author} \n"
                details += f"    Date: {model_info.article.date} \n"
            else:
                details += "   Not found"
            details += "\n\n"

            details += "Data:\n"
            if model_info.data:
                details += f"    Name: {model_info.data.name} \n"
                details += f"    Date: {model_info.data.date} \n"
                details += f"    Place: {model_info.data.place} \n"
            else:
                details += "    No data"

            messagebox.showinfo(f"Details: {name}", details)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load details: {e}")