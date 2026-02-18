"Will contain all UI logic and code"
"UI library used: Tkinter"


import tkinter as tk
from tkinter import ttk

class UI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PC Builder")
        self.root.geometry("800x500")

        self._create_layout()

    def _create_layout(self):
        #main box
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        #left side panel logic
        left_frame = ttk.LabelFrame(main_frame, text="Components", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(left_frame, text="Select Component Type").pack(anchor="w")

        self.component_type = tk.StringVar()
        component_menu = ttk.Combobox(
            left_frame,
            textvariable=self.component_type,
            values=[
                "CPU", "GPU", "Motherboard", "RAM",
                "Storage", "PSU", "Case"
            ],
            state="readonly"
        )
        component_menu.pack(fill=tk.X, pady=5)

        ttk.Button(
            left_frame,
            text="Add Component",
            command=self.add_component
        ).pack(fill=tk.X, pady=5)

        #right side panel with build summary
        right_frame = ttk.LabelFrame(main_frame, text="Current Build", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.build_list = tk.Listbox(right_frame)
        self.build_list.pack(fill=tk.BOTH, expand=True)

        ttk.Button(
            right_frame,
            text="Finalize Build",
            command=self.finalize_build
        ).pack(pady=5)

    def add_component(self):
        selected = self.component_type.get()
        if selected:
            self.build_list.insert(tk.END, f"{selected} added")

    def finalize_build(self):
        print("Build finalized")

    def run(self):
        self.root.mainloop()

