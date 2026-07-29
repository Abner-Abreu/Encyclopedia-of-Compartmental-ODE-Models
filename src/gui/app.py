import tkinter as tk

from gui.styles import COLORS, FONTS, SIZES
from gui.views.model_view import ModelsView

class App:
    """
    The main application window for the Encyclopedia of Compartmental ODE Models.

    This class serves as the root application container, managing the main
    window and coordinating the switching between different views. Currently,
    it supports the ModelsView for managing models in the encyclopedia.

    The application uses a single content frame that dynamically switches
    between views based on user navigation. Views are cached after their
    first creation for performance.

    Attributes:
        root (tk.Tk): The root Tkinter window.
        service (ServiceHandler): The service handler for database operations.
        content_frame (tk.Frame): The main content area where views are displayed.
        views (dict): Cache of created views, keyed by view ID.

    Note:
        The application currently only supports the 'models' view.
        Additional views can be added by extending the _switch_view()
        method and creating corresponding view classes.
    """

    def __init__(self, root, service):
        """
        Initializes the main application window.

        Args:
            root: The root Tkinter window.
            service: The ServiceHandler instance for database operations.
        """
        self.root = root
        self.root.title("Encyclopedia of Compartmental ODE Models")
        self.root.geometry(f"{SIZES['window_width']}x{SIZES['window_height']}")
        self.root.configure(bg=COLORS['background'])

        self.service = service

        self._create_widgets()
        self._show_initial_view()

    def _create_widgets(self):
        """
        Creates the main application widgets.

        This method initializes:
            - The content frame where views will be displayed
            - The views cache dictionary
        """
        self.content_frame = tk.Frame(self.root, bg=COLORS['background'])
        self.content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        self.views = {}

    def _show_initial_view(self):
        """
        Displays the initial view of the application.

        The initial view is the ModelsView, which displays the list of
        models in the encyclopedia.
        """
        self._switch_view('models')

    def _switch_view(self, view_id: str):
        """
        Switches the content area to the specified view.

        This method:
            1. Clears all widgets from the content frame
            2. Creates or retrieves the requested view from the cache
            3. Displays the view

        Views are cached after their first creation to improve performance
        when switching between them.

        Args:
            view_id: The identifier of the view to display.
                Currently only 'models' is supported.

        Note:
            When switching to a cached view, the view's _load_all_models()
            method is called to refresh the data before displaying it.
        """
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if view_id == 'models':
            if 'models' not in self.views:
                self.views['models'] = ModelsView(self.content_frame, self.service)
            else:
                self.views['models']._load_all_models()
                self.views['models'].frame.pack(fill='both', expand=True)