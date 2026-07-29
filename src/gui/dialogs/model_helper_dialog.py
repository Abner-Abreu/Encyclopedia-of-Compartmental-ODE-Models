import tkinter as tk
from tkinter import messagebox

from .model_dialog import ModelDialog

from services import ServiceHandler

from gui.styles import COLORS, FONTS

class ModelHelperDialog:
    """
    A helper dialog that collects the number of compartments and parameters.

    This dialog serves as a preliminary step before opening the main
    ModelDialog. It asks the user to specify how many compartments and
    parameters they want to create for the new model.

    The dialog:
        - Prompts the user for the number of compartments
        - Prompts the user for the number of parameters
        - Validates that both inputs are valid integers
        - Opens the ModelDialog with the specified counts
        - Closes itself after opening the main dialog

    This design separates the configuration step (how many entities)
    from the data entry step (what are their names/expressions).

    Attributes:
        master: The parent widget.
        services (ServiceHandler): The service handler for database operations.
        result: The result of the dialog (currently always None).
    """

    def __init__(self, master, services: ServiceHandler):
        """
        Initializes the ModelHelperDialog.

        Args:
            master: The parent widget.
            services: The ServiceHandler instance for database operations.
        """
        self.master = master
        self.result = None
        self.services = services
        self._create_window()

    def _create_window(self):
        """
        Creates and configures the dialog window with input fields.

        The window contains:
            - A title "New Model"
            - An entry field for number of compartments
            - An entry field for number of parameters
            - A Continue button that triggers the main dialog

        The window is centered on the screen, non-resizable, modal,
        and transient to the parent window.
        """
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

        tk.Label(
            frame,
            text="Number of Compartments:",
            font=FONTS['subtitle'],
            bg=COLORS['background']
        ).pack(anchor='w')
        self.entry_compartments = tk.Entry(frame, font=FONTS['normal'], width=40)
        self.entry_compartments.pack(fill='x', pady=(0, 10))

        tk.Label(
            frame,
            text="Number of Params:",
            font=FONTS['subtitle'],
            bg=COLORS['background']
        ).pack(anchor='w')
        self.entry_params = tk.Entry(frame, font=FONTS['normal'], width=40)
        self.entry_params.pack(fill='x', pady=(0, 10))

        button_frame = tk.Frame(frame, bg=COLORS['background'])
        button_frame.pack(fill='x', pady=(10, 0))

        self.btn_save = tk.Button(
            button_frame,
            text="Continue",
            command=self._continue,
            bg=COLORS['primary'],
            fg=COLORS['light_text'],
            font=FONTS['normal'],
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        self.btn_save.pack(side='right', padx=(0, 5))

    def _continue(self):
        """
        Validates user input and opens the main ModelDialog.

        This method:
            1. Retrieves the values from both entry fields
            2. Attempts to convert them to integers
            3. If successful, opens ModelDialog with the specified counts
            4. Closes this helper dialog
            5. If conversion fails, shows an error message

        Raises:
            ValueError: If the input cannot be converted to an integer.
                This is caught and displayed to the user.
        """
        try:
            cant_comp = int(self.entry_compartments.get())
            cant_param = int(self.entry_params.get())
            ModelDialog(self.master, self.services, cant_comp, cant_param)
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Validation Error", str(e))