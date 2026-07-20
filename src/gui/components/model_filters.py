import tkinter as tk

from dtos import FiltersDto

from gui.styles import COLORS, FONTS

class ModelFilters:
    """
    A UI component that provides search and filter controls for models.

    This class creates a labeled frame containing input fields for
    filtering models by various criteria:
        - Model name (text input)
        - Parameter name (text input)
        - Compartment name (text input)
        - Situation name (text input)
        - Article name (text input)
        - All linear parameters (checkbox)

    The component includes three action buttons:
        - Search: Applies the current filters
        - Clear: Resets all text fields
        - Show All: Resets all fields and clears the linear checkbox

    The filters are collected into a FiltersDto and passed to the
    on_filter callback when Search is clicked or Show All is pressed.

    Attributes:
        master: The parent widget.
        on_filter (callable): Callback function called when filters are applied.
        on_clear (callable, optional): Callback function called when filters are cleared.
    
    Note:
        The component uses grid layout for the input fields and places
        the buttons in a separate frame on the right side. The Search
        and Show All buttons trigger the on_filter callback, while the
        Clear button clears the text fields and then applies empty filters.
    """

    def __init__(self, master, on_filter: callable, on_clear: callable = None):
        """
        Initializes the ModelFilters component.

        Args:
            master: The parent widget.
            on_filter: Callback function called when filters are applied.
                The callback receives a FiltersDto as its argument.
            on_clear: Optional callback function called when filters are cleared.
        """
        self.master = master
        self.on_filter = on_filter
        self.on_clear = on_clear
        self._create_widgets()

    def _create_widgets(self):
        """
        Creates and arranges all widgets in the filter component.

        This method builds the labeled frame, input fields, checkbox,
        and action buttons using grid layout.
        """
        self.frame = tk.LabelFrame(
            self.master,
            text="Search",
            font=FONTS['subtitle'],
            bg=COLORS['background'],
            fg=COLORS['text'],
            padx=10,
            pady=10
        )
        self.frame.pack(fill='x', padx=5, pady=(0, 10))

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)

        # Row 0: Name
        tk.Label(self.frame, text="Model Name:", font=FONTS['normal'],
                 bg=COLORS['background']).grid(row=0, column=0, sticky='w', padx=(0, 5), pady=2)
        self.entry_name = tk.Entry(self.frame, font=FONTS['normal'], width=25)
        self.entry_name.grid(row=0, column=1, sticky='w', padx=(0, 10), pady=2)

        # Row 1: Parameter
        tk.Label(self.frame, text="Parameter:", font=FONTS['normal'],
                 bg=COLORS['background']).grid(row=1, column=0, sticky='w', padx=(0, 5), pady=2)
        self.entry_parameter = tk.Entry(self.frame, font=FONTS['normal'], width=25)
        self.entry_parameter.grid(row=1, column=1, sticky='w', padx=(0, 10), pady=2)

        # Row 2: Compartment
        tk.Label(self.frame, text="Compartment:", font=FONTS['normal'],
                 bg=COLORS['background']).grid(row=2, column=0, sticky='w', padx=(0, 5), pady=2)
        self.entry_compartment = tk.Entry(self.frame, font=FONTS['normal'], width=25)
        self.entry_compartment.grid(row=2, column=1, sticky='w', padx=(0, 10), pady=2)

        # Row 3: Situation
        tk.Label(self.frame, text="Situation:", font=FONTS['normal'],
                 bg=COLORS['background']).grid(row=3, column=0, sticky='w', padx=(0, 5), pady=2)
        self.entry_situation = tk.Entry(self.frame, font=FONTS['normal'], width=25)
        self.entry_situation.grid(row=3, column=1, sticky='w', padx=(0, 10), pady=2)

        # Row 4: Article
        tk.Label(self.frame, text="Article:", font=FONTS['normal'],
                 bg=COLORS['background']).grid(row=4, column=0, sticky='w', padx=(0, 5), pady=2)
        self.entry_article = tk.Entry(self.frame, font=FONTS['normal'], width=25)
        self.entry_article.grid(row=4, column=1, sticky='w', padx=(0, 10), pady=2)

        # Row 5: Linear checkbox
        self.var_linear = tk.BooleanVar(value=False)
        self.check_linear = tk.Checkbutton(
            self.frame,
            text="Only models with all linear parameters",
            variable=self.var_linear,
            font=FONTS['normal'],
            bg=COLORS['background'],
        )
        self.check_linear.grid(row=5, column=0, columnspan=2, sticky='w', pady=5)

        # Buttons
        button_frame = tk.Frame(self.frame, bg=COLORS['background'])
        button_frame.grid(row=0, column=2, rowspan=6, sticky='n', padx=(20, 0))

        self.btn_search = tk.Button(
            button_frame, text="Search", command=self._apply_filters,
            bg=COLORS['primary'], fg=COLORS['light_text'],
            font=FONTS['normal'], relief='flat', padx=20, pady=8,
            cursor='hand2', width=12
        )
        self.btn_search.pack(pady=(0, 5))

        self.btn_clear = tk.Button(
            button_frame, text="Clear", command=self._clear_filters,
            bg=COLORS['secondary'], fg=COLORS['light_text'],
            font=FONTS['normal'], relief='flat', padx=20, pady=8,
            cursor='hand2', width=12
        )
        self.btn_clear.pack(pady=(0, 5))

        self.btn_show_all = tk.Button(
            button_frame, text="Show All", command=self._show_all,
            bg=COLORS['primary'], fg=COLORS['light_text'],
            font=FONTS['normal'], relief='flat', padx=20, pady=8,
            cursor='hand2', width=12
        )
        self.btn_show_all.pack()

    def _apply_filters(self):
        """
        Collects current filter values and calls the on_filter callback.

        This method is called when the Search button is clicked or
        when filters are cleared.
        """
        self.on_filter(self._get_filters())

    def _clear_filters(self):
        """
        Clears all text input fields.

        This method is called when the Clear button is clicked.
        It clears all entry fields.
        """
        self.entry_name.delete(0, 'end')
        self.entry_parameter.delete(0, 'end')
        self.entry_compartment.delete(0, 'end')
        self.entry_situation.delete(0, 'end')
        self.entry_article.delete(0, 'end')

    def _show_all(self):
        """
        Clears all filters and unchecks the linear checkbox.

        This method is called when the Show All button is clicked.
        It clears all text fields, unchecks the "all linear" checkbox,
        and then applies the empty filters.
        """
        self._clear_filters()
        self._apply_filters()

    def _get_filters(self) -> FiltersDto:
        """
        Collects all filter values into a FiltersDto object.

        Returns:
            FiltersDto: A DTO containing all current filter values.
        """
        return FiltersDto(
            name_contains=self.entry_name.get().strip(),
            parameter_contains=self.entry_parameter.get().strip(),
            compartment_contains=self.entry_compartment.get().strip(),
            situation_contains=self.entry_situation.get().strip(),
            article_contains=self.entry_article.get().strip(),
            all_linear=self.var_linear.get()
        )