"""
The purpose of this module is to define the GUI for the PC Builder application using Tkinter and ttkbootstrap.

Authors: Dorian Lawton, Justin Hanko, Landon Jurmo and Jaykin Hang
Date: April 24, 2026
Version: Python 3.12
"""
# GUI built using Tkinter
# Will contain all UI logic and code
# UI library used: Tkinter

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from components import hardware
import auto_generate


class UI:
    """
    UI class that creates the interface for the application.
    """

    def __init__(self, games, cpu_rankings, gpu_rankings):
        """
        Initializes the UI with game data and benchmark rankings.

        Args:
            games (list[dict]): List of games and the components required for those games
            cpu_rankings (dict): Mapping of CPU model names to benchmark scores
            gpu_rankings (dict): Mapping of GPU model names to benchmark scores.
        Returns:
            None
        """
        self.games = games
        self.cpu_rankings = cpu_rankings
        self.gpu_rankings = gpu_rankings
        self.root = ttk.Window(themename="darkly")
        self.root.title("PC Builder")
        self.root.geometry("1920x1080")
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
        """
        Creates the layout of the GUI components.

        The layout is divided into three regions:
          - bottom_frame: game selection only
          - left_frame:   manual component picker
          - right_frame:  current build display + algorithm options + generate button

        Algorithm-specific option panels (spec tier, budget) are created here
        but shown/hidden dynamically by _on_algorithm_change().

        Returns:
            None
        """
        self.part_var = tk.StringVar()
        self.part_var.trace_add("write", self.add_component)

        # main field
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # bottom area — game selection only
        bottom_frame = ttk.LabelFrame(self.root, text="Games")
        bottom_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(bottom_frame, text="Select Game").grid(row=0, column=0, padx=5)

        self.game_var = tk.StringVar()

        self.game_menu = ttk.Combobox(
            bottom_frame,
            textvariable=self.game_var,
            values=[game["game_name"] for game in self.games],
            state="readonly",
            width=40
        )
        self.game_menu.grid(row=0, column=1, padx=5)

        self.result_label = ttk.Label(bottom_frame, text="Select a game to check requirements")
        self.result_label.grid(row=1, column=0, columnspan=2, pady=5)

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

        # algorithm selection
        ttk.Label(right_frame, text="Generation Algorithm").pack(anchor="w", padx=5)

        self.algorithm_var = tk.StringVar(value="Minimum Cost")

        self.algorithm_menu = ttk.Combobox(
            right_frame,
            textvariable=self.algorithm_var,
            values=[
                "Minimum Cost",
                "Budget",
            ],
            state="readonly"
        )
        self.algorithm_menu.pack(fill=tk.X, padx=5, pady=5)
        self.algorithm_var.trace_add("write", self._on_algorithm_change)

        # spec tier panel, shown only for "Minimum Cost"
        self.tier_frame = ttk.LabelFrame(right_frame, text="Spec Tier")
        self.requirement_level = tk.StringVar(value="min")
        ttk.Radiobutton(
            self.tier_frame,
            text="Minimum  (guarantees minimum playable)",
            variable=self.requirement_level,
            value="min"
        ).pack(anchor="w", padx=5, pady=2)
        ttk.Radiobutton(
            self.tier_frame,
            text="Recommended  (targets recommended settings)",
            variable=self.requirement_level,
            value="rec"
        ).pack(anchor="w", padx=5, pady=2)

        # budget entry panel, shown only for budget
        self.budget_frame = ttk.LabelFrame(right_frame, text="Budget ($)")
        self.budget_var = tk.StringVar(value="1500")
        self.budget_entry = ttk.Entry(self.budget_frame, textvariable=self.budget_var)
        self.budget_entry.pack(fill=tk.X, padx=5, pady=4)
        ttk.Label(
            self.budget_frame,
            text="Total GPU + CPU + RAM spend limit",
            font=("TkDefaultFont", 8)
        ).pack(anchor="w", padx=5)

        # show the correct panels for the default algorithm
        self._on_algorithm_change()

        # generate build button
        ttk.Button(
            right_frame,
            text="Auto-generate Build",
            command=self.generate_build
        ).pack(pady=5)

        # status label for budget warnings and errors
        self.status_label = ttk.Label(right_frame, text="", wraplength=300)
        self.status_label.pack(anchor="w", padx=5)

        # total cost display
        ttk.Separator(right_frame, orient="horizontal").pack(fill=tk.X, padx=5, pady=4)
        self.cost_label = ttk.Label(right_frame, text="Total Build Cost: $0", font=("TkDefaultFont", 11, "bold"))
        self.cost_label.pack(anchor="w", padx=5, pady=2)


    def update_part_dropdown(self, *_):
        """
        Updates the dropdown menus based on the user's selection.

        Args:
            *_: Placeholder for other arguments
        Return:
            None
        """
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
            if self.build.get("CPU_Brand"):
                parts = hardware.get("Motherboards", {}).get(self.build["CPU_Brand"], [])
            else:
                parts = []
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
        """
        Updates the displayed build and total cost label in the UI.

        Each component line shows the part name and its price where known.
        The total cost label at the bottom sums all priced components.

        Return:
            None
        """
        self.build_list.config(state="normal")
        self.build_list.delete("1.0", tk.END)

        for component, value in self.build.items():
            # skip internal brand-tracking keys from the display
            if component.endswith("_Brand"):
                continue
            if value:
                price = auto_generate.get_build_price({**self.build, "__single__": (component, value)})
                # look up price for just this one part
                part_price = self._get_part_price(component, value)
                if part_price is not None:
                    line = f"{component}: {value}  (${part_price:,})\n"
                else:
                    line = f"{component}: {value}\n"
            else:
                line = f"{component}: ---\n"

            self.build_list.insert(tk.END, line)

        self.build_list.config(state="disabled")

        # update total cost label
        total = auto_generate.get_build_price(self.build)
        self.cost_label.config(text=f"Total Build Cost: ${total:,}")

    def _get_part_price(self, component, part_name):
        """
        Look up the price of a single component by its build key and part name.

        Args:
            component (str): Build dict key (e.g. "GPU", "CPU", "RAM").
            part_name (str): The part name string.

        Returns:
            int or None: Price in dollars, or None if not found.
        """
        import components as comp
        if component == "GPU":
            category = "NVIDIA GPUs" if self.build.get("GPU_Brand") == "NVIDIA" else "AMD GPUs"
            return comp.prices.get(category, {}).get(part_name)
        elif component == "CPU":
            category = "Intel CPUs" if self.build.get("CPU_Brand") == "Intel" else "AMD CPUs"
            return comp.prices.get(category, {}).get(part_name)
        elif component == "RAM":
            ram_prices = comp.prices.get("RAM", {})
            for key, price in ram_prices.items():
                if key in part_name:
                    return price
        elif component == "Motherboard":
            return comp.prices.get("Motherboards", {}).get(part_name)
        elif component == "Case":
            return comp.prices.get("Cases", {}).get(part_name)
        elif component == "Storage":
            return comp.prices.get("Storage", {}).get(part_name)
        elif component == "PSU":
            return comp.prices.get("PSU", {}).get(part_name)
        return None


    def add_component(self, *_):
        """
        Adds the selected component to the UI.

        Args:
            *_: Placeholder for other arguments
        Return:
            None
        """
        component = self.component_type.get()
        part = self.part_var.get()
        brand = self.brand_var.get()

        if component and part:
            self.build[component] = part
            if component in ["CPU", "GPU"]:
                self.build[f"{component}_Brand"] = brand
            self.update_build_display()


    def _on_algorithm_change(self, *_):
        """
        Show or hide algorithm-specific option panels when the selected algorithm changes.

        Panel visibility rules:
          "Minimum Cost" -> spec tier panel only
          "Budget"       -> budget panel only (spec tier not shown; the budget cap
                           does all meaningful filtering — analysis confirmed the
                           spec floor had no practical effect for almost all games)

        Args:
            *_: Placeholder for trace callback arguments.
        Return:
            None
        """
        algo = self.algorithm_var.get()

        # spec tier (min/rec radio buttons) — only meaningful for Minimum Cost
        if algo == "Minimum Cost":
            self.tier_frame.pack(fill=tk.X, padx=5, pady=2)
        else:
            self.tier_frame.pack_forget()

        # budget entry — only for Budget algorithm
        if algo == "Budget":
            self.budget_frame.pack(fill=tk.X, padx=5, pady=2)
        else:
            self.budget_frame.pack_forget()

    # using this temporarily to generate build
    def generate_build(self):
        """
        Generates a build based on the selected game and algorithm.

        Dispatch table:
          "Minimum Cost" -> generate_pc (original algorithm, respects spec tier)
          "Budget"       -> generate_pc_budget (best balanced build within budget)

        Return:
             None
        """
        strategy = self.algorithm_var.get()
        self.status_label.config(text="")

        if strategy == "Budget":
            budget = self._parse_budget()
            if budget is None:
                return
            self.build["GPU"], self.build["CPU"], self.build["RAM"] = auto_generate.generate_pc_budget(
                self.game_var.get(),
                self.games,
                self.cpu_rankings,
                self.gpu_rankings,
                self.build.get("CPU_Brand"),
                self.build.get("GPU_Brand"),
                budget,
            )
            if self.build["GPU"] is None or self.build["CPU"] is None or self.build["RAM"] is None:
                self.status_label.config(
                    text="budget is too low to create a build"
                )

        else:
            # default: original Minimum Cost algorithm
            self.build["GPU"], self.build["CPU"], self.build["RAM"] = auto_generate.generate_pc(
                self.game_var.get(),
                self.requirement_level.get(),
                self.games,
                self.cpu_rankings,
                self.gpu_rankings,
                self.build.get("CPU_Brand"),
                self.build.get("GPU_Brand"),
                strategy
            )

        # auto-populate fixed components for both algorithms
        self._auto_populate_fixed_parts()

        self.update_build_display()

    def _auto_populate_fixed_parts(self):
        """
        Automatically fill in fixed components that are not user-selected during
        auto-generation: Storage, PSU, Motherboard (matched to CPU brand), and
        the cheapest available Case.

        Only sets a component if it is not already manually chosen by the user,
        so manual selections made before auto-generating are preserved.

        Return:
            None
        """
        import components as comp

        # Storage, single fixed drive
        if not self.build.get("Storage"):
            storage_list = comp.hardware.get("Storage", [])
            if storage_list:
                self.build["Storage"] = storage_list[0]

        # PSU, single fixed unit
        if not self.build.get("PSU"):
            psu_list = comp.hardware.get("PSU", [])
            if psu_list:
                self.build["PSU"] = psu_list[0]

        # Motherboard, matched to CPU brand
        if not self.build.get("Motherboard"):
            cpu_brand = self.build.get("CPU_Brand", "Intel")
            mobo_list = comp.hardware.get("Motherboards", {}).get(cpu_brand, [])
            if mobo_list:
                self.build["Motherboard"] = mobo_list[0]

        # Case, cheapest available
        if not self.build.get("Case"):
            case_prices = comp.prices.get("Cases", {})
            case_list = comp.hardware.get("Cases", [])
            if case_prices and case_list:
                cheapest = min(case_list, key=lambda c: case_prices.get(c, float("inf")))
                self.build["Case"] = cheapest

    def _parse_budget(self):
        """
        Parse and validate the budget entry field.

        Returns:
            float or None: The budget value, or None if the input is invalid
            (error message written to status_label in that case).
        """
        try:
            value = float(self.budget_var.get().replace(",", "").replace("$", "").strip())
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            self.status_label.config(text="Not a valid budget.")
            return None

    def save_current_build(self):
        name = self.save_name_var.get().strip()

        if not name:
            messagebox.showerror("Error", "Please enter a name for the build.")
            return

        # prevent saving empty builds
        if not self.build.get("CPU") or not self.build.get("GPU"):
            messagebox.showerror("Error", "Build is incomplete.")
            return

        save_load.save_build(name, self.build.copy())
        self.refresh_saved_builds()
        self.status_label.config(text=f"Build '{name}' saved.")

    def load_selected_build(self):
        name = self.saved_builds_var.get()

        if name == "None":
            # clear the build
            for key in self.build:
                if key.endswith("_Brand"):
                    continue
                self.build[key] = None

            self.update_build_display()
            self.status_label.config(text="Cleared current build.")
            return

        if not name:
            messagebox.showerror("Error", "Select a build to load.")
            return

        loaded = save_load.load_build(name)

        if not loaded:
            messagebox.showerror("Error", "Build not found.")
            return

        self.build.clear()
        self.build.update(loaded)
        self.update_build_display()
        self.status_label.config(text=f"Loaded '{name}'.")

    def refresh_saved_builds(self):
        builds = save_load.load_all_builds()
        values = ["None"] + list(builds.keys())
        self.saved_builds_menu["values"] = values
        self.saved_builds_var.set("None")


    def run(self):
        """
        Starts the GUI application.

        Return:
             None
        """
        self.root.mainloop()