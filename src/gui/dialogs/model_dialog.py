import tkinter as tk
from tkinter import messagebox

from gui.styles import COLORS, FONTS

from services import ServiceHandler

from dtos import (ModelInfoDto,
                  CompartmentDto,
                  ParamInfoDto,
                  SituationDto,
                  DataDto,
                  ArticleDto)

from datetime import datetime

class ModelDialog:
    def __init__(self, master, model_service :ServiceHandler, compartments_cant: int = 1,
                 params_cant: int = 1):
        self.master = master
        self.model_service = model_service
        self.result = None
        self.compartments_cant = compartments_cant
        self.params_cant = params_cant
        self._create_window()

    def _create_window(self):
        title = "New Model"
        self.window = tk.Toplevel(self.master)
        self.window.title(title)
        self.window.geometry("1100x650")
        self.window.resizable(True, True)
        self.window.grab_set()
        self.window.transient(self.master)

        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (1100 // 2)
        y = (self.window.winfo_screenheight() // 2) - (650 // 2)
        self.window.geometry(f"+{x}+{y}")

        # Main container
        main_frame = tk.Frame(self.window, bg=COLORS['background'], padx=15, pady=15)
        main_frame.pack(fill='both', expand=True)

        # === THREE COLUMNS ===
        columns_frame = tk.Frame(main_frame, bg=COLORS['background'])
        columns_frame.pack(fill='both', expand=True)

        # Configure column weights (1:1:1)
        columns_frame.columnconfigure(0, weight=1)
        columns_frame.columnconfigure(1, weight=1)
        columns_frame.columnconfigure(2, weight=1)
        columns_frame.rowconfigure(0, weight=1)

        # --- COLUMN 1: Model Name + Situation + Article + Data ---
        col1 = tk.Frame(columns_frame, bg=COLORS['background'])
        col1.grid(row=0, column=0, sticky='nsew', padx=(0, 5))

        # Model Name
        tk.Label(
            col1,
            text="📝 Model Name:",
            font=FONTS['subtitle'],
            bg=COLORS['background']
        ).pack(anchor='w', pady=(0, 2))

        self.entry_name = tk.Entry(
            col1,
            font=FONTS['normal'],
            width=30
        )
        self.entry_name.pack(fill='x', pady=(0, 10))

        # === SITUATION ===
        situation_frame = tk.LabelFrame(
            col1,
            text="📌 Situation",
            font=FONTS['subtitle'],
            bg=COLORS['background'],
            fg=COLORS['text'],
            padx=8,
            pady=8
        )
        situation_frame.pack(fill='x', pady=(0, 10))

        tk.Label(
            situation_frame,
            text="Name:",
            font=FONTS['normal'],
            bg=COLORS['background']
        ).pack(anchor='w')

        self.entry_situation_name = tk.Entry(
            situation_frame,
            font=FONTS['normal'],
            width=30
        )
        self.entry_situation_name.pack(fill='x', pady=(0, 5))

        tk.Label(
            situation_frame,
            text="Description:",
            font=FONTS['normal'],
            bg=COLORS['background']
        ).pack(anchor='w')

        self.entry_situation_description = tk.Entry(
            situation_frame,
            font=FONTS['normal'],
            width=30
        )
        self.entry_situation_description.pack(fill='x')

        # === ARTICLE ===
        article_frame = tk.LabelFrame(
            col1,
            text="📄 Article",
            font=FONTS['subtitle'],
            bg=COLORS['background'],
            fg=COLORS['text'],
            padx=8,
            pady=8
        )
        article_frame.pack(fill='x', pady=(0, 10))

        tk.Label(
            article_frame,
            text="Name:",
            font=FONTS['normal'],
            bg=COLORS['background']
        ).pack(anchor='w')

        self.entry_article_name = tk.Entry(
            article_frame,
            font=FONTS['normal'],
            width=30
        )
        self.entry_article_name.pack(fill='x', pady=(0, 5))

        tk.Label(
            article_frame,
            text="Author:",
            font=FONTS['normal'],
            bg=COLORS['background']
        ).pack(anchor='w')

        self.entry_article_author = tk.Entry(
            article_frame,
            font=FONTS['normal'],
            width=30
        )
        self.entry_article_author.pack(fill='x', pady=(0, 5))

        tk.Label(
            article_frame,
            text="Date (YYYY-MM-DD):",
            font=FONTS['normal'],
            bg=COLORS['background']
        ).pack(anchor='w')

        self.entry_article_date = tk.Entry(
            article_frame,
            font=FONTS['normal'],
            width=30
        )
        self.entry_article_date.pack(fill='x')

        # === DATA ===
        data_frame = tk.LabelFrame(
            col1,
            text="📈 Data",
            font=FONTS['subtitle'],
            bg=COLORS['background'],
            fg=COLORS['text'],
            padx=8,
            pady=8
        )
        data_frame.pack(fill='x')

        tk.Label(
            data_frame,
            text="Name:",
            font=FONTS['normal'],
            bg=COLORS['background']
        ).pack(anchor='w')

        self.entry_data_name = tk.Entry(
            data_frame,
            font=FONTS['normal'],
            width=30
        )
        self.entry_data_name.pack(fill='x', pady=(0, 5))

        tk.Label(
            data_frame,
            text="Place:",
            font=FONTS['normal'],
            bg=COLORS['background']
        ).pack(anchor='w')

        self.entry_data_place = tk.Entry(
            data_frame,
            font=FONTS['normal'],
            width=30
        )
        self.entry_data_place.pack(fill='x', pady=(0, 5))

        tk.Label(
            data_frame,
            text="Date (YYYY-MM-DD):",
            font=FONTS['normal'],
            bg=COLORS['background']
        ).pack(anchor='w')

        self.entry_data_date = tk.Entry(
            data_frame,
            font=FONTS['normal'],
            width=30
        )
        self.entry_data_date.pack(fill='x')

        # --- COLUMN 2: Compartments (with scroll) ---
        col2 = tk.LabelFrame(
            columns_frame,
            text="🧩 Compartments",
            font=FONTS['subtitle'],
            bg=COLORS['background'],
            fg=COLORS['text'],
            padx=8,
            pady=8
        )
        col2.grid(row=0, column=1, sticky='nsew', padx=5)

        # Create entries for compartments
        self.compartments_entries = []
        self._create_compartment_entries(col2)

        # --- COLUMN 3: Parameters (with scroll) ---
        col3 = tk.LabelFrame(
            columns_frame,
            text="⚙️ Parameters",
            font=FONTS['subtitle'],
            bg=COLORS['background'],
            fg=COLORS['text'],
            padx=8,
            pady=8
        )
        col3.grid(row=0, column=2, sticky='nsew', padx=(5, 0))

        # Create entries for parameters
        self.parameters_entries = []
        self._create_parameter_entries(col3)

        # --- BUTTONS ---
        button_frame = tk.Frame(main_frame, bg=COLORS['background'])
        button_frame.pack(fill='x', pady=(15, 0))

        self.btn_save = tk.Button(
            button_frame,
            text="💾 Save",
            command=self._save,
            bg=COLORS['primary'],
            fg=COLORS['light_text'],
            font=FONTS['normal'],
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        self.btn_save.pack(side='right', padx=(0, 5))

        self.btn_cancel = tk.Button(
            button_frame,
            text="❌ Cancel",
            command=self._cancel,
            bg=COLORS['danger'],
            fg=COLORS['light_text'],
            font=FONTS['normal'],
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        self.btn_cancel.pack(side='right')

        self.window.bind('<Return>', lambda e: self._save())
        self.window.bind('<Escape>', lambda e: self._cancel())
        self.entry_name.focus_set()

    def _create_compartment_entries(self, parent):
        """Creates scrollable entries for compartments."""
        # Canvas with scrollbar
        canvas = tk.Canvas(parent, bg=COLORS['background'], highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['background'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Create compartment entries
        for i in range(self.compartments_cant):
            frame = tk.Frame(scrollable_frame, bg=COLORS['background'])
            frame.pack(fill='x', pady=(0, 10))

            tk.Label(
                frame,
                text=f"Compartment {i+1}:",
                font=FONTS['bold'],
                bg=COLORS['background']
            ).pack(anchor='w')

            tk.Label(
                frame,
                text="Name:",
                font=FONTS['normal'],
                bg=COLORS['background']
            ).pack(anchor='w')

            entry_name = tk.Entry(frame, font=FONTS['normal'], width=25)
            entry_name.pack(fill='x', pady=(0, 3))

            tk.Label(
                frame,
                text="Expression:",
                font=FONTS['normal'],
                bg=COLORS['background']
            ).pack(anchor='w')

            entry_expression = tk.Entry(frame, font=FONTS['normal'], width=25)
            entry_expression.pack(fill='x')

            self.compartments_entries.append({
                'name': entry_name,
                'expression': entry_expression
            })

    def _create_parameter_entries(self, parent):
        """Creates scrollable entries for parameters."""
        # Canvas with scrollbar
        canvas = tk.Canvas(parent, bg=COLORS['background'], highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['background'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Create parameter entries
        for i in range(self.params_cant):
            frame = tk.Frame(scrollable_frame, bg=COLORS['background'])
            frame.pack(fill='x', pady=(0, 10))

            tk.Label(
                frame,
                text=f"Parameter {i+1}:",
                font=FONTS['bold'],
                bg=COLORS['background']
            ).pack(anchor='w')

            tk.Label(
                frame,
                text="Name:",
                font=FONTS['normal'],
                bg=COLORS['background']
            ).pack(anchor='w')

            entry_name = tk.Entry(frame, font=FONTS['normal'], width=25)
            entry_name.pack(fill='x', pady=(0, 3))

            tk.Label(
                frame,
                text="Symbol:",
                font=FONTS['normal'],
                bg=COLORS['background']
            ).pack(anchor='w')

            entry_symbol = tk.Entry(frame, font=FONTS['normal'], width=25)
            entry_symbol.pack(fill='x', pady=(0, 3))

            tk.Label(
                frame,
                text="Meaning:",
                font=FONTS['normal'],
                bg=COLORS['background']
            ).pack(anchor='w')

            entry_meaning = tk.Entry(frame, font=FONTS['normal'], width=25)
            entry_meaning.pack(fill='x', pady=(0, 3))

            tk.Label(
                frame,
                text="Linear (True/False):",
                font=FONTS['normal'],
                bg=COLORS['background']
            ).pack(anchor='w')

            entry_linear = tk.Entry(frame, font=FONTS['normal'], width=25)
            entry_linear.pack(fill='x')

            self.parameters_entries.append({
                'name': entry_name,
                'symbol': entry_symbol,
                'meaning': entry_meaning,
                'linear': entry_linear
            })

    def _get_compartment_data(self) -> list[CompartmentDto]: 
        """Returns list of compartment data from the entries."""
        compartments = []
        for entry in self.compartments_entries:
            name = entry['name'].get().strip()
            expression = entry['expression'].get().strip()
            
            compartments.append(
                CompartmentDto(name=name,
                               expression=expression))
        return compartments

    def _get_parameter_data(self) -> list[ParamInfoDto]:
        """Returns list of parameter data from the entries."""
        parameters = []
        for entry in self.parameters_entries:
            name = entry['name'].get().strip()
            symbol = entry['symbol'].get().strip()
            meaning = entry['meaning'].get().strip()
            linear_str = entry['linear'].get().strip().lower()

            # Convert linear string to boolean
            linear = linear_str in ('true', 'yes', '1', 'si')

            parameters.append(
                ParamInfoDto(name=name,
                             linear=linear,
                             symbol=symbol,
                             meaning=meaning))
        return parameters

    def _save(self):
        

        try:
            self.model_service.create_complete(self._generate_model_info())
            self.result = self.entry_name.get().strip()

            self.window.destroy()

        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Could not save: {e}")

    def _cancel(self):
        self.window.destroy()

    def _generate_model_info(self) -> ModelInfoDto:

        name = self.entry_name.get().strip()

        # Get all data from entries
        compartments = self._get_compartment_data()
        parameters = self._get_parameter_data()

        # Get situation, article, data data
        situation_name = self.entry_situation_name.get().strip()
        situation_desc = self.entry_situation_description.get().strip()
        situation = SituationDto(name=situation_name,
                                 description=situation_desc)

        article_name = self.entry_article_name.get().strip()
        article_author = self.entry_article_author.get().strip()
        article_date = datetime.fromisoformat(self.entry_article_date.get().strip())
        article = ArticleDto(name=article_name,
                             author=article_author,
                             date=article_date)
        
        data_name = self.entry_data_name.get().strip()
        data_place = self.entry_data_place.get().strip()
        data_date = datetime.fromisoformat(self.entry_data_date.get().strip())
        
        data = DataDto(name=data_name,
                       date=data_date,
                       place=data_place)

        return ModelInfoDto(name=name,
                            compartments=compartments,
                            params=parameters,
                            situation=situation,
                            article=article,
                            data=data)