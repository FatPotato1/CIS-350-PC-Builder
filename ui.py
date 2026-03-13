#GUI built using Tkinter


#Will contain all UI logic and code
# UI library used: Tkinter


import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from components import hardware


class UI:

    def __init__(self):
        self.root = ttk.Window(themename="darkly")
        self.root.title("PC Builder")
        self.root.geometry("800x500")
        self._create_layout()

    def _create_layout(self):

        #main field
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        #left panel for component selection
        left_frame = ttk.LabelFrame(main_frame, text="Components")
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(left_frame, text="Select Component Type").pack(anchor="w")

        #dropdown for components
        self.component_type = tk.StringVar()
        self.component_type.trace_add("write", self.update_part_dropdown)

        self.component_menu = ttk.Combobox(
            left_frame,
            textvariable=self.component_type,
            values=["CPU", "GPU", "Motherboard", "RAM", "Storage", "PSU", "Case"],
            state="readonly"
        )
        self.component_menu.pack(fill=tk.X, pady=5)

        #part selection dropdown
        ttk.Label(left_frame, text="Select Part").pack(anchor="w")

        self.part_var = tk.StringVar()
        self.part_menu = ttk.Combobox(
            left_frame,
            textvariable=self.part_var,
            state="readonly"
        )
        self.part_menu.pack(fill=tk.X, pady=5)

        #add selected component to build list
        ttk.Button(
            left_frame,
            text="Add Component",
            command=self.add_component
        ).pack(fill=tk.X, pady=5)

        #build summary
        right_frame = ttk.LabelFrame(main_frame, text="Current Build")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.build_list = tk.Listbox(right_frame)
        self.build_list.pack(fill=tk.BOTH, expand=True)

        #placeholder save build button
        ttk.Button(
            right_frame,
            text="Save Build",
            command=self.save_build
        ).pack(pady=5)

    def update_part_dropdown(self, *_):

        component = self.component_type.get()
        parts = []

        # fill cpu fields
        if component == "CPU":
            parts = (
                [cpu["name"] for cpu in hardware["Intel"]["CPUs"]] +
                [cpu["name"] for cpu in hardware["AMD"]["CPUs"]]
            )

        #fill gpu fields
        elif component == "GPU":
            parts = (
                [gpu["name"] for gpu in hardware["NVIDIA"]["GPUs"]] +
                [gpu["name"] for gpu in hardware["AMD"]["GPUs"]]
            )

        #update the dropdown values and reset selection
        self.part_menu["values"] = parts
        self.part_var.set("")

    def add_component(self):
        component = self.component_type.get()
        part = self.part_var.get()

        if component and part:
            self.build_list.insert(tk.END, f"{component}: {part}")

    def save_build(self):
        #placeholder, does not function yet
        print("Build saved")

    def run(self):
        self.root.mainloop()

