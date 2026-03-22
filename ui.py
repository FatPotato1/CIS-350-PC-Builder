# GUI built using Tkinter
# Will contain all UI logic and code
# UI library used: Tkinter

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from components import hardware
import auto_generate


class UI:


    def __init__(self, games, cpu_rankings, gpu_rankings):
        self.games = games
        self.cpu_rankings = cpu_rankings
        self.gpu_rankings = gpu_rankings
        self.root = ttk.Window(themename="darkly")
        self.root.title("PC Builder")
        self.root.geometry("800x500")
        self._create_layout()
        # main part data that is stored
        self.build = {
            "CPU": None,
            "CPU_Brand": "Intel",
            "GPU": None,
            "GPU_Brand": "NVIDIA",
            "Motherboard": None,
            "RAM": None,
            "Storage": None,
            "PSU": None,
            "Case": None
        }
        self.update_build_display()

    def _create_layout(self):
        self.part_var = tk.StringVar()
        self.part_var.trace_add("write", self.add_component)

        # main field
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        bottom_frame = ttk.LabelFrame(self.root, text="Games")
        bottom_frame.pack(fill=tk.X, padx=10, pady=5)

        # bottom area
        ttk.Label(bottom_frame, text="Select Game").grid(row=0, column=0, padx=5)

        self.game_var = tk.StringVar()

        self.game_menu = ttk.Combobox(
            bottom_frame,
            textvariable=self.game_var,
            values=[game["game_name"] for game in self.games],
            state="readonly",
            width=40
        )
        # game selection area
        self.requirement_level = tk.StringVar(value="min")

        ttk.Radiobutton(
            bottom_frame,
            text="Minimum",
            variable=self.requirement_level,
            value="min"
        ).grid(row=0, column=2)

        ttk.Radiobutton(
            bottom_frame,
            text="Recommended",
            variable=self.requirement_level,
            value="rec"
        ).grid(row=0, column=3)
        self.game_menu.grid(row=0, column=1, padx=5)

        self.result_label = ttk.Label(bottom_frame, text="Select a game to check requirements")
        self.result_label.grid(row=1, column=0, columnspan=4, pady=5)


        # left panel for component selection
        left_frame = ttk.LabelFrame(main_frame, text="Components")
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(left_frame, text="Select Component Type").pack(anchor="w")

        # dropdown for components
        self.component_type = tk.StringVar()
        self.component_type.trace_add("write", self.update_part_dropdown)

        self.component_menu = ttk.Combobox(
            left_frame,
            textvariable=self.component_type,
            values=["CPU", "GPU", "Motherboard", "RAM", "Storage", "PSU", "Case"],
            state="readonly"
        )
        self.component_menu.pack(fill=tk.X, pady=5)

        # pick brands for parts
        ttk.Label(left_frame, text="Select Brand").pack(anchor="w")

        self.brand_var = tk.StringVar()
        self.brand_menu = ttk.Combobox(
            left_frame,
            textvariable=self.brand_var,
            state="readonly"
        )
        self.brand_menu.pack(fill=tk.X, pady=5)
        self.brand_var.trace_add("write", self.update_part_dropdown)

        # part selection dropdown
        ttk.Label(left_frame, text="Select Part").pack(anchor="w")

        self.part_menu = ttk.Combobox(
            left_frame,
            textvariable=self.part_var,
            state="readonly"
        )
        self.part_menu.pack(fill=tk.X, pady=5)

        # build summary
        right_frame = ttk.LabelFrame(main_frame, text="Current Build")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.build_list = tk.Text(right_frame, height=15, state="disabled")
        self.build_list.pack(fill=tk.BOTH, expand=True)

        # generate build button
        ttk.Button(
            right_frame,
            text="Auto-generate Build",
            command=self.generate_build
        ).pack(pady=5)


    def update_part_dropdown(self, *_):
        component = self.component_type.get()
        brand = self.brand_var.get()

        # automatically update brand menu
        if component == "CPU":
            self.brand_menu["values"] = ["Intel", "AMD"]
            if brand not in ["Intel", "AMD"]:
                self.brand_var.set("")
        elif component == "GPU":
            self.brand_menu["values"] = ["NVIDIA", "AMD"]
            if brand not in ["NVIDIA", "AMD"]:
                self.brand_var.set("")
        else:
            self.brand_menu["values"] = []
            self.brand_var.set("")

        if component in ("CPU", "GPU") and brand:
            self.build[f"{component}_Brand"] = brand
            self.update_build_display()
        # fill in part menu based on brand selection
        parts = []
        if component == "CPU":
            if brand == "Intel":
                parts = hardware.get("Intel CPUs", [])
            elif brand == "AMD":
                parts = hardware.get("AMD CPUs", [])
        elif component == "GPU":
            if brand == "NVIDIA":
                parts = hardware.get("NVIDIA GPUs", [])
            elif brand == "AMD":
                parts = hardware.get("AMD GPUs", [])
        elif component == "Motherboard":
            parts = hardware.get("Motherboards", [])
        elif component == "RAM":
            parts = hardware.get("RAM", [])
        elif component == "Storage":
            parts = hardware.get("Storage", [])
        elif component == "PSU":
            parts = hardware.get("PSU", [])
        elif component == "Case":
            parts = hardware.get("Cases", [])

        self.part_menu["values"] = parts
        if self.part_var.get() not in parts:
            self.part_var.set("")


    def update_build_display(self):

        self.build_list.config(state="normal")
        self.build_list.delete("1.0", tk.END)

        for component, value in self.build.items():
            if value:
                line = f"{component}: {value}\n"
            else:
                line = f"{component}: ---\n"

            self.build_list.insert(tk.END, line)

        self.build_list.config(state="disabled")



    def add_component(self, *_):
        component = self.component_type.get()
        part = self.part_var.get()
        brand = self.brand_var.get()

        if component and part:
            self.build[component] = part
            if component in ["CPU", "GPU"]:
                self.build[f"{component}_Brand"] = brand
            self.update_build_display()


    # using this temporarily to generate build
    def generate_build(self):
        self.build["GPU"], self.build["CPU"] = auto_generate.generate_pc(self.game_var.get(), self.requirement_level.get(),
        self.games, self.cpu_rankings, self.gpu_rankings, self.build.get("CPU_Brand"),self.build.get("GPU_Brand"),)
        self.update_build_display()


    def run(self):
        self.root.mainloop()