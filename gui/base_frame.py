import tkinter as tk
from tkinter import ttk
from typing import Any, Dict

class BaseFrame(ttk.Frame):
    def __init__(self, parent: Any, controller: Any):
        super().__init__(parent)
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        """Initialize the UI components"""
        pass

    def on_show(self):
        """Called when the frame is shown"""
        pass

    def create_scrollable_frame(self) -> ttk.Frame:
        """Create a scrollable frame and return the inner frame"""
        # Create a canvas
        canvas = tk.Canvas(self)
        canvas.pack(side="left", fill="both", expand=True)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        # Configure the canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas
        inner_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        # Update scroll region when the size of the inner frame changes
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        inner_frame.bind("<Configure>", on_configure)

        return inner_frame

    def create_form_field(self, parent: ttk.Frame, label: str, row: int,
                         readonly: bool = False) -> ttk.Entry:
        """Create a labeled form field"""
        ttk.Label(parent, text=label).grid(row=row, column=0, padx=5, pady=5, sticky="e")
        entry = ttk.Entry(parent, state="readonly" if readonly else "normal")
        entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        return entry

    def create_table(self, parent: ttk.Frame, columns: Dict[str, int],
                    height: int = 10) -> ttk.Treeview:
        """Create a table with the specified columns"""
        tree = ttk.Treeview(parent, columns=list(columns.keys()),
                           show='headings', height=height)
        
        # Configure columns and headings
        for col, width in columns.items():
            tree.column(col, width=width)
            tree.heading(col, text=col.title())

        # Add scrollbars
        y_scroll = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        x_scroll = ttk.Scrollbar(parent, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        # Create a container frame for the table and scrollbars
        container = ttk.Frame(parent)
        container.pack(fill="both", expand=True)
        
        # Pack the table and scrollbars
        tree.pack(side="left", fill="both", expand=True)
        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")

        return tree
