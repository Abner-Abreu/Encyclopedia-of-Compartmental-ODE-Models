import tkinter as tk
from tkinter import ttk

class DataTable:
    """
    A reusable table component with scrollbar and selection handling.

    This class provides a wrapper around ttk.Treeview to create a
    consistent table component with built-in features:
        - Column definitions with configurable widths
        - Vertical scrollbar
        - Single row selection tracking
        - Double-click event handling
        - Data loading and clearing methods

    The table stores data internally and provides methods to load,
    add, delete, and retrieve selected rows.

    Attributes:
        master: The parent widget.
        columns (list[dict[str, str]]): List of column definitions.
            Each dict must contain 'id' and 'text', optionally 'width'.
        on_double_click (callable, optional): Callback for double-click events.
        height (int): Number of visible rows. Defaults to 15.
        selected: The currently selected tree item (if any).
        data (list[list]): The data currently loaded in the table.

    Note:
        The table uses ttk.Treeview internally. The data is stored
        as a list of lists where each inner list corresponds to a row
        with values matching the column order.
    """

    def __init__(self, master, columns: list[dict[str, str]],
                 on_double_click: callable = None,
                 height: int = 15):
        """
        Initializes the DataTable component.

        Args:
            master: The parent widget.
            columns: List of column definitions. Each dictionary must
                contain 'id' and 'text' keys, optionally 'width'.
            on_double_click: Optional callback function triggered when
                a row is double-clicked. Receives the row values as a list.
            height: Number of visible rows in the table.
        """
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
        """
        Handles row selection events.

        Stores the selected item ID for later retrieval.
        """
        selection = self.tree.selection()
        self.selected = selection[0] if selection else None

    def _on_double_click(self, event):
        """
        Handles double-click events on table rows.

        Triggers the on_double_click callback with the row values
        if a row is selected and a callback is defined.
        """
        if self.selected and self.on_double_click:
            item = self.tree.item(self.selected)
            self.on_double_click(item['values'])

    def load_data(self, data: list[list]):
        """
        Loads new data into the table, replacing existing data.

        Args:
            data: A list of rows, where each row is a list of values
                matching the column order and types.
        """
        self.data = data
        self.clear()
        for row in data:
            self.tree.insert('', 'end', values=row)

    def add_row(self, row: list):
        """
        Appends a new row to the table.

        Args:
            row: A list of values matching the column order.
        """
        self.data.append(row)
        self.tree.insert('', 'end', values=row)

    def delete_selected(self) -> bool:
        """
        Deletes the currently selected row from the table.

        Returns:
            bool: True if a row was deleted, False if no row was selected.

        Note:
            This method removes the selected row from both the display
            and the internal data cache.
        """
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
        """
        Retrieves the values of the currently selected row.

        Returns:
            list | None: The row values as a list if a row is selected,
                otherwise None.
        """
        if self.selected:
            item = self.tree.item(self.selected)
            return item['values']
        return None

    def clear(self):
        """
        Clears all rows from the table.

        This method removes all data from the display and resets the
        internal data cache to an empty list.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.data = []
        self.selected = None