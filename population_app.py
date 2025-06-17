import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, List, Tuple, Callable
import json
from datetime import datetime


class PopulationModels:

    def __init__(self):
        self.models = {
            "logistic": {
                "name": "Model logistyczny",
                "description": "Wzrost populacji z ograniczeniem pojemności środowiska",
                "equations": ["r*x*(1 - x/K)"],
                "math_equations": [r"$\frac{dx}{dt} = rx\left(1 - \frac{x}{K}\right)$"],
                "math_description": "Równanie logistyczne Verhulsta opisuje wzrost populacji ograniczony pojemnością środowiska K. Tempo wzrostu r jest modulowane przez czynnik (1-x/K), który spowalnia wzrost gdy populacja zbliża się do pojemności.",
                "equilibrium": "x* = K (stabilny punkt równowagi)",
                "parameters": ["r", "K"],
                "param_names": ["Tempo wzrostu (r)", "Pojemność środowiska (K)"],
                "param_descriptions": ["Wewnętrzne tempo wzrostu populacji [1/czas]",
                                       "Maksymalna populacja jaką może utrzymać środowisko"],
                "param_defaults": [0.5, 100],
                "param_ranges": [(0.1, 2.0), (10, 1000)],
                "initial_conditions": ["x0"],
                "ic_names": ["Populacja początkowa"],
                "ic_defaults": [10],
                "variables": ["x"],
                "var_names": ["Populacja"],
                "type": "single",
                "analytical_solution": r"$x(t) = \frac{K}{1 + \left(\frac{K-x_0}{x_0}\right)e^{-rt}}$"
            },
            "lotka_volterra": {
                "name": "Model Lotka-Volterra (drapieżnik-ofiara)",
                "description": "Interakcja między populacją ofiar i drapieżników",
                "equations": ["a*x - b*x*y", "c*x*y - d*y"],
                "math_equations": [
                    r"$\frac{dx}{dt} = ax - bxy$",
                    r"$\frac{dy}{dt} = cxy - dy$"
                ],
                "math_description": "Klasyczny model drapieżnik-ofiara. Ofiary (x) rosną eksponencjalnie z tempem 'a', ale są redukowane przez drapieżniki z intensywnością 'bxy'. Drapieżniki (y) rosną proporcjonalnie do dostępności ofiar 'cxy' i maleją z tempem śmiertelności 'd'.",
                "equilibrium": "Punkt równowagi: (d/c, a/b)",
                "parameters": ["a", "b", "c", "d"],
                "param_names": ["Tempo wzrostu ofiar (a)", "Skuteczność polowania (b)",
                                "Efektywność konwersji (c)", "Śmiertelność drapieżników (d)"],
                "param_descriptions": [
                    "Tempo wzrostu ofiar bez drapieżników [1/czas]",
                    "Skuteczność polowania drapieżników [1/(populacja·czas)]",
                    "Efektywność konwersji ofiar na drapieżniki [1/(populacja·czas)]",
                    "Naturalna śmiertelność drapieżników [1/czas]"
                ],
                "param_defaults": [1.0, 0.5, 0.3, 0.8],
                "param_ranges": [(0.1, 3.0), (0.1, 2.0), (0.1, 1.0), (0.1, 2.0)],
                "initial_conditions": ["x0", "y0"],
                "ic_names": ["Populacja ofiar", "Populacja drapieżników"],
                "ic_defaults": [10, 5],
                "variables": ["x", "y"],
                "var_names": ["Ofiary", "Drapieżniki"],
                "type": "system",
                "conserved_quantity": r"$H(x,y) = cx + by - d\ln(x) - a\ln(y) = \text{const}$"
            },
            "competition": {
                "name": "Konkurencja międzygatunkowa",
                "description": "Dwa gatunki konkurujące o te same zasoby",
                "equations": ["r1*x*(1 - (x + alpha*y)/K1)", "r2*y*(1 - (y + beta*x)/K2)"],
                "math_equations": [
                    r"$\frac{dx}{dt} = r_1x\left(1 - \frac{x + \alpha y}{K_1}\right)$",
                    r"$\frac{dy}{dt} = r_2y\left(1 - \frac{y + \beta x}{K_2}\right)$"
                ],
                "math_description": "Model konkurencji Lotka-Volterra. Każdy gatunek rośnie logistycznie, ale jego efektywna pojemność jest redukowana przez obecność konkurenta. Parametry α i β określają siłę konkurencji międzygatunkowej.",
                "equilibrium": "Koegzystencja możliwa gdy αβ < 1",
                "parameters": ["r1", "r2", "K1", "K2", "alpha", "beta"],
                "param_names": ["Tempo wzrostu gat. 1 (r₁)", "Tempo wzrostu gat. 2 (r₂)",
                                "Pojemność dla gat. 1 (K₁)", "Pojemność dla gat. 2 (K₂)",
                                "Wpływ gat. 2 na gat. 1 (α)", "Wpływ gat. 1 na gat. 2 (β)"],
                "param_descriptions": [
                    "Tempo wzrostu gatunku 1 [1/czas]",
                    "Tempo wzrostu gatunku 2 [1/czas]",
                    "Pojemność środowiska dla gatunku 1",
                    "Pojemność środowiska dla gatunku 2",
                    "Współczynnik konkurencji: wpływ gat. 2 na gat. 1",
                    "Współczynnik konkurencji: wpływ gat. 1 na gat. 2"
                ],
                "param_defaults": [1.0, 0.8, 100, 80, 0.5, 0.6],
                "param_ranges": [(0.1, 2.0), (0.1, 2.0), (10, 200), (10, 200), (0.1, 2.0), (0.1, 2.0)],
                "initial_conditions": ["x0", "y0"],
                "ic_names": ["Populacja gatunku 1", "Populacja gatunku 2"],
                "ic_defaults": [20, 15],
                "variables": ["x", "y"],
                "var_names": ["Gatunek 1", "Gatunek 2"],
                "type": "system",
                "coexistence_condition": r"$\alpha < \frac{K_1}{K_2}$ i $\beta < \frac{K_2}{K_1}$"
            },
            "sir": {
                "name": "Model SIR (epidemiologiczny)",
                "description": "Rozprzestrzenianie się choroby w populacji",
                "equations": ["-beta*S*I/N", "beta*S*I/N - gamma*I", "gamma*I"],
                "math_equations": [
                    r"$\frac{dS}{dt} = -\frac{\beta SI}{N}$",
                    r"$\frac{dI}{dt} = \frac{\beta SI}{N} - \gamma I$",
                    r"$\frac{dR}{dt} = \gamma I$"
                ],
                "math_description": "Model epidemiologiczny SIR (Susceptible-Infected-Recovered). Podatni (S) stają się zarażeni z tempem proporcjonalnym do kontaktów βSI/N. Zarażeni (I) wyzdrowieją z tempem γI. Całkowita populacja N = S + I + R jest zachowana.",
                "equilibrium": "Podstawowa liczba reprodukcji: R₀ = β/γ",
                "parameters": ["beta", "gamma", "N"],
                "param_names": ["Tempo transmisji (β)", "Tempo wyzdrowienia (γ)", "Całkowita populacja (N)"],
                "param_descriptions": [
                    "Tempo transmisji choroby [1/czas]",
                    "Tempo wyzdrowienia/usunięcia [1/czas]",
                    "Całkowita populacja (stała)"
                ],
                "param_defaults": [0.3, 0.1, 1000],
                "param_ranges": [(0.01, 1.0), (0.01, 0.5), (100, 10000)],
                "initial_conditions": ["S0", "I0", "R0"],
                "ic_names": ["Podatni", "Zarażeni", "Ozdrowieńcy"],
                "ic_defaults": [990, 10, 0],
                "variables": ["S", "I", "R"],
                "var_names": ["Podatni", "Zarażeni", "Ozdrowieńcy"],
                "type": "system",
                "basic_reproduction": r"$R_0 = \frac{\beta}{\gamma}$ (epidemia gdy $R_0 > 1$)"
            },
            "metapopulation": {
                "name": "Metapopulacja",
                "description": "Populacja podzielona na dwie połączone subpopulacje",
                "equations": ["r1*x*(1 - x/K1) + m*(y - x)", "r2*y*(1 - y/K2) + m*(x - y)"],
                "math_equations": [
                    r"$\frac{dx}{dt} = r_1x\left(1 - \frac{x}{K_1}\right) + m(y - x)$",
                    r"$\frac{dy}{dt} = r_2y\left(1 - \frac{y}{K_2}\right) + m(x - y)$"
                ],
                "math_description": "Model metapopulacji łączy dwie subpopulacje przez migrację. Każda subpopulacja rośnie logistycznie, ale osobniki mogą migrować między populacjami z tempem 'm'. Migracja wyrównuje różnice w gęstości populacji.",
                "equilibrium": "Równowaga zależy od tempa migracji m",
                "parameters": ["r1", "r2", "K1", "K2", "m"],
                "param_names": ["Tempo wzrostu pop. 1 (r₁)", "Tempo wzrostu pop. 2 (r₂)",
                                "Pojemność pop. 1 (K₁)", "Pojemność pop. 2 (K₂)", "Tempo migracji (m)"],
                "param_descriptions": [
                    "Tempo wzrostu subpopulacji 1 [1/czas]",
                    "Tempo wzrostu subpopulacji 2 [1/czas]",
                    "Pojemność środowiska dla subpopulacji 1",
                    "Pojemność środowiska dla subpopulacji 2",
                    "Tempo migracji między subpopulacjami [1/czas]"
                ],
                "param_defaults": [0.8, 0.6, 100, 80, 0.1],
                "param_ranges": [(0.1, 2.0), (0.1, 2.0), (10, 200), (10, 200), (0.01, 0.5)],
                "initial_conditions": ["x0", "y0"],
                "ic_names": ["Populacja 1", "Populacja 2"],
                "ic_defaults": [50, 30],
                "variables": ["x", "y"],
                "var_names": ["Populacja 1", "Populacja 2"],
                "type": "system",
                "migration_effect": r"Migracja: $m(y-x)$ dla pop. 1, $m(x-y)$ dla pop. 2"
            }
        }


class RK4Solver:

    def solve_single_ode_animated(self, f: Callable, t0: float, x0: float, h: float, n_steps: int):
        t_curr = t0
        x_curr = x0

        yield t_curr, x_curr

        for i in range(n_steps):
            k1 = h * f(t_curr, x_curr)
            k2 = h * f(t_curr + h / 2, x_curr + k1 / 2)
            k3 = h * f(t_curr + h / 2, x_curr + k2 / 2)
            k4 = h * f(t_curr + h, x_curr + k3)

            x_curr = x_curr + (k1 + 2 * k2 + 2 * k3 + k4) / 6
            t_curr = t_curr + h

            yield t_curr, x_curr

    def solve_system_ode_animated(self, functions: List[Callable], t0: float,
                                  initial_conditions: List[float], h: float, n_steps: int):
        n_vars = len(initial_conditions)
        t_curr = t0
        curr_vals = initial_conditions.copy()

        yield t_curr, curr_vals.copy()

        for step in range(n_steps):
            k1 = [h * f(t_curr, *curr_vals) for f in functions]

            k2_vals = [curr_vals[i] + k1[i] / 2 for i in range(n_vars)]
            k2 = [h * f(t_curr + h / 2, *k2_vals) for f in functions]

            k3_vals = [curr_vals[i] + k2[i] / 2 for i in range(n_vars)]
            k3 = [h * f(t_curr + h / 2, *k3_vals) for f in functions]

            k4_vals = [curr_vals[i] + k3[i] for i in range(n_vars)]
            k4 = [h * f(t_curr + h, *k4_vals) for f in functions]

            for i in range(n_vars):
                curr_vals[i] = curr_vals[i] + (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6

            t_curr = t_curr + h

            yield t_curr, curr_vals.copy()


class MathDisplayWindow:

    def __init__(self, parent, model_info, parameters):
        self.window = tk.Toplevel(parent)
        self.window.title(f"Matematyka: {model_info['name']}")
        self.window.geometry("800x700")
        self.window.resizable(True, True)

        self.model_info = model_info
        self.parameters = parameters

        self.setup_display()

    def setup_display(self):

        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Tytuł modelu
        title_label = ttk.Label(scrollable_frame, text=self.model_info['name'],
                                font=('Arial', 16, 'bold'))
        title_label.pack(anchor=tk.W, pady=(0, 10))

        # Opis modelu
        desc_frame = ttk.LabelFrame(scrollable_frame, text="Opis biologiczny", padding=10)
        desc_frame.pack(fill=tk.X, pady=(0, 10))

        desc_label = ttk.Label(desc_frame, text=self.model_info['description'],
                               wraplength=750, justify=tk.LEFT)
        desc_label.pack(anchor=tk.W)

        # Równania matematyczne
        eq_frame = ttk.LabelFrame(scrollable_frame, text="Równania różniczkowe", padding=10)
        eq_frame.pack(fill=tk.X, pady=(0, 10))

        for i, eq in enumerate(self.model_info['math_equations']):
            eq_label = ttk.Label(eq_frame, text=f"Równanie {i + 1}: {eq}",
                                 font=('Courier', 12), foreground='blue')
            eq_label.pack(anchor=tk.W, pady=2)

        # Opis matematyczny
        math_desc_frame = ttk.LabelFrame(scrollable_frame, text="Interpretacja matematyczna", padding=10)
        math_desc_frame.pack(fill=tk.X, pady=(0, 10))

        math_desc_label = ttk.Label(math_desc_frame, text=self.model_info['math_description'],
                                    wraplength=750, justify=tk.LEFT)
        math_desc_label.pack(anchor=tk.W)

        # Parametry z wartościami
        param_frame = ttk.LabelFrame(scrollable_frame, text="Parametry modelu", padding=10)
        param_frame.pack(fill=tk.X, pady=(0, 10))

        for i, (param, name, desc) in enumerate(zip(
                self.model_info['parameters'],
                self.model_info['param_names'],
                self.model_info['param_descriptions']
        )):
            value = self.parameters.get(param, 'N/A')
            param_text = f"{param} = {value} - {name}\n   {desc}"
            param_label = ttk.Label(param_frame, text=param_text,
                                    font=('Arial', 10), foreground='darkgreen')
            param_label.pack(anchor=tk.W, pady=2)

        # Właściwości matematyczne
        props_frame = ttk.LabelFrame(scrollable_frame, text="Właściwości matematyczne", padding=10)
        props_frame.pack(fill=tk.X, pady=(0, 10))

        # Punkt równowagi
        eq_label = ttk.Label(props_frame, text=f"Równowaga: {self.model_info['equilibrium']}",
                             font=('Courier', 11), foreground='red')
        eq_label.pack(anchor=tk.W, pady=2)

        # Dodatkowe właściwości specyficzne dla modelu
        if 'analytical_solution' in self.model_info:
            anal_label = ttk.Label(props_frame,
                                   text=f"Rozwiązanie analityczne: {self.model_info['analytical_solution']}",
                                   font=('Courier', 10), foreground='purple')
            anal_label.pack(anchor=tk.W, pady=2)

        if 'conserved_quantity' in self.model_info:
            cons_label = ttk.Label(props_frame, text=f"Wielkość zachowana: {self.model_info['conserved_quantity']}",
                                   font=('Courier', 10), foreground='purple')
            cons_label.pack(anchor=tk.W, pady=2)

        if 'basic_reproduction' in self.model_info:
            r0_label = ttk.Label(props_frame, text=f"Liczba reprodukcji: {self.model_info['basic_reproduction']}",
                                 font=('Courier', 10), foreground='purple')
            r0_label.pack(anchor=tk.W, pady=2)

        if 'coexistence_condition' in self.model_info:
            coex_label = ttk.Label(props_frame,
                                   text=f"Warunek koegzystencji: {self.model_info['coexistence_condition']}",
                                   font=('Courier', 10), foreground='purple')
            coex_label.pack(anchor=tk.W, pady=2)

        # Obliczenia numeryczne
        numerical_frame = ttk.LabelFrame(scrollable_frame, text="Metoda numeryczna", padding=10)
        numerical_frame.pack(fill=tk.X, pady=(0, 10))

        rk4_text = """Metoda Rungego-Kutty 4. rzędu (RK4):
• Dokładność: O(h⁵) błąd lokalny, O(h⁴) błąd globalny
• Stabilność: h < 2.78/|λ_max| gdzie λ_max to największa wartość własna Jacobiego
• Algorytm: k₁ = hf(t,y), k₂ = hf(t+h/2,y+k₁/2), k₃ = hf(t+h/2,y+k₂/2), k₄ = hf(t+h,y+k₃)
• Aktualizacja: y_{n+1} = y_n + (k₁ + 2k₂ + 2k₃ + k₄)/6"""

        rk4_label = ttk.Label(numerical_frame, text=rk4_text,
                              font=('Courier', 9), justify=tk.LEFT)
        rk4_label.pack(anchor=tk.W)

        # Przycisk zamknięcia
        close_button = ttk.Button(scrollable_frame, text="Zamknij",
                                  command=self.window.destroy)
        close_button.pack(pady=10)

        # Pakowanie canvas i scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind scroll wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)


class AnimatedPopulationGUI:
    """Interfejs graficzny z animacją dla badania dynamiki populacji"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Animowana Dynamika Populacji - Modele Biologiczne z Matematyką")
        self.root.geometry("1700x1000")

        self.models = PopulationModels()
        self.solver = RK4Solver()
        self.current_model = "logistic"

        # Zmienne animacji
        self.animation = None
        self.is_playing = False
        self.animation_speed = 1.0
        self.current_step = 0
        self.max_steps = 1000
        self.animation_data = None
        self.solver_generator = None

        # Dane do wykresów
        self.time_data = []
        self.population_data = []
        self.phase_data = []

        # Okno matematyki
        self.math_window = None

        self.setup_gui()

    def setup_gui(self):

        # Główny kontener
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Lewa strona - parametry i kontrolki
        left_frame = ttk.Frame(main_frame, width=500)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.pack_propagate(False)

        # Prawa strona - wykresy
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.setup_parameters_panel(left_frame)
        self.setup_animation_controls(left_frame)
        self.setup_math_controls(left_frame)
        self.setup_export_controls(left_frame)
        self.setup_plots_panel(right_frame)

    def setup_parameters_panel(self, parent):

        # Wybór modelu
        ttk.Label(parent, text="Model populacyjny:", font=('Arial', 14, 'bold')).pack(anchor=tk.W, pady=(0, 5))

        self.model_var = tk.StringVar(value=self.current_model)
        model_frame = ttk.Frame(parent)
        model_frame.pack(fill=tk.X, pady=(0, 10))

        self.model_combo = ttk.Combobox(model_frame, textvariable=self.model_var,
                                        values=list(self.models.models.keys()),
                                        state="readonly", width=35)
        self.model_combo.pack(side=tk.LEFT)
        self.model_combo.bind('<<ComboboxSelected>>', self.on_model_change)

        # Opis modelu
        self.description_label = ttk.Label(parent, text="", wraplength=480, justify=tk.LEFT)
        self.description_label.pack(anchor=tk.W, pady=(0, 15))

        # Parametry modelu
        self.params_frame = ttk.LabelFrame(parent, text="Parametry biologiczne", padding=10)
        self.params_frame.pack(fill=tk.X, pady=(0, 10))

        # Warunki początkowe
        self.ic_frame = ttk.LabelFrame(parent, text="Warunki początkowe", padding=10)
        self.ic_frame.pack(fill=tk.X, pady=(0, 10))

        # Parametry symulacji
        sim_frame = ttk.LabelFrame(parent, text="Parametry symulacji", padding=10)
        sim_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(sim_frame, text="Czas symulacji:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.time_entry = ttk.Entry(sim_frame, width=15)
        self.time_entry.grid(row=0, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        self.time_entry.insert(0, "30")

        ttk.Label(sim_frame, text="Krok czasowy:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.step_entry = ttk.Entry(sim_frame, width=15)
        self.step_entry.grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        self.step_entry.insert(0, "0.05")

        self.update_model_interface()

    def setup_animation_controls(self, parent):

        # Panel kontroli animacji
        anim_frame = ttk.LabelFrame(parent, text="Kontrola animacji", padding=10)
        anim_frame.pack(fill=tk.X, pady=(10, 10))

        # Przyciski kontroli
        button_frame = ttk.Frame(anim_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))

        self.play_button = ttk.Button(button_frame, text="▶ Start",
                                      command=self.start_animation, width=12)
        self.play_button.pack(side=tk.LEFT, padx=(0, 5))

        self.pause_button = ttk.Button(button_frame, text="⏸ Pauza",
                                       command=self.pause_animation, width=12)
        self.pause_button.pack(side=tk.LEFT, padx=(0, 5))

        self.stop_button = ttk.Button(button_frame, text="⏹ Stop",
                                      command=self.stop_animation, width=12)
        self.stop_button.pack(side=tk.LEFT)

        # Kontrola prędkości
        speed_frame = ttk.Frame(anim_frame)
        speed_frame.pack(fill=tk.X, pady=(5, 0))

        ttk.Label(speed_frame, text="Prędkość animacji:").pack(anchor=tk.W)

        self.speed_var = tk.DoubleVar(value=1.0)
        self.speed_scale = ttk.Scale(speed_frame, from_=0.1, to=5.0,
                                     variable=self.speed_var, orient=tk.HORIZONTAL)
        self.speed_scale.pack(fill=tk.X, pady=(5, 0))
        self.speed_scale.bind('<Motion>', self.on_speed_change)

        # Etykieta prędkości
        self.speed_label = ttk.Label(speed_frame, text="1.0x")
        self.speed_label.pack(anchor=tk.W)

        # Postęp animacji
        progress_frame = ttk.Frame(anim_frame)
        progress_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Label(progress_frame, text="Postęp:").pack(anchor=tk.W)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                            maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(5, 0))

        # Status animacji
        self.status_label = ttk.Label(anim_frame, text="Gotowy do animacji",
                                      font=('Arial', 9))
        self.status_label.pack(anchor=tk.W, pady=(10, 0))

    def setup_math_controls(self, parent):

        math_frame = ttk.LabelFrame(parent, text="Matematyka i analiza", padding=10)
        math_frame.pack(fill=tk.X, pady=(10, 10))

        ttk.Button(math_frame, text="📐 Pokaż równania",
                   command=self.show_math_window).pack(fill=tk.X, pady=2)

        ttk.Button(math_frame, text="📊 Analiza stabilności",
                   command=self.analyze_stability).pack(fill=tk.X, pady=2)

        ttk.Button(math_frame, text="🔢 Oblicz właściwości",
                   command=self.calculate_properties).pack(fill=tk.X, pady=2)

    def setup_export_controls(self, parent):

        export_frame = ttk.LabelFrame(parent, text="Eksport i zapis", padding=10)
        export_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(export_frame, text="💾 Eksportuj wykres czasowy",
                   command=lambda: self.export_plot('time')).pack(fill=tk.X, pady=2)

        ttk.Button(export_frame, text="💾 Eksportuj płaszczyznę fazową",
                   command=lambda: self.export_plot('phase')).pack(fill=tk.X, pady=2)

        ttk.Button(export_frame, text="💾 Eksportuj oba wykresy",
                   command=lambda: self.export_plot('both')).pack(fill=tk.X, pady=2)

        ttk.Button(export_frame, text="📄 Zapisz dane CSV",
                   command=self.export_data_csv).pack(fill=tk.X, pady=2)

        ttk.Button(export_frame, text="⚙️ Zapisz parametry",
                   command=self.save_parameters).pack(fill=tk.X, pady=2)

        ttk.Button(export_frame, text="📂 Wczytaj parametry",
                   command=self.load_parameters).pack(fill=tk.X, pady=2)

    def setup_plots_panel(self, parent):

        # Notebook dla zakładek
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Zakładka - wykres czasowy
        self.time_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.time_frame, text="Dynamika czasowa")

        # Zakładka - płaszczyzna fazowa
        self.phase_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.phase_frame, text="Płaszczyzna fazowa")

        # Konfiguracja wykresów
        self.setup_time_plot()
        self.setup_phase_plot()

    def setup_time_plot(self):
        self.time_fig, self.time_ax = plt.subplots(figsize=(12, 8))
        self.time_ax.set_xlabel('Czas', fontsize=12)
        self.time_ax.set_ylabel('Wielkość populacji', fontsize=12)
        self.time_ax.set_title('Animowana dynamika populacji w czasie', fontsize=14)
        self.time_ax.grid(True, alpha=0.3)

        # Linie dla animacji
        self.time_lines = []
        self.time_points = []  # Punkty pokazujące aktualną pozycję

        self.time_canvas = FigureCanvasTkAgg(self.time_fig, self.time_frame)
        self.time_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def setup_phase_plot(self):
        self.phase_fig, self.phase_ax = plt.subplots(figsize=(12, 8))
        self.phase_ax.set_xlabel('Populacja 1', fontsize=12)
        self.phase_ax.set_ylabel('Populacja 2', fontsize=12)
        self.phase_ax.set_title('Animowana płaszczyzna fazowa', fontsize=14)
        self.phase_ax.grid(True, alpha=0.3)

        # Linia trajektorii i punkt aktualny
        self.phase_line, = self.phase_ax.plot([], [], 'b-', linewidth=2, alpha=0.7)
        self.phase_point, = self.phase_ax.plot([], [], 'ro', markersize=10)
        self.phase_trail, = self.phase_ax.plot([], [], 'b-', linewidth=1, alpha=0.3)

        self.phase_canvas = FigureCanvasTkAgg(self.phase_fig, self.phase_frame)
        self.phase_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def on_model_change(self, event=None):
        self.current_model = self.model_var.get()
        self.update_model_interface()
        self.stop_animation()

    def update_model_interface(self):
        model_info = self.models.models[self.current_model]

        self.description_label.config(text=model_info["description"])

        for widget in self.params_frame.winfo_children():
            widget.destroy()
        for widget in self.ic_frame.winfo_children():
            widget.destroy()

        self.param_entries = {}
        for i, (param, name, default, range_val) in enumerate(zip(
                model_info["parameters"],
                model_info["param_names"],
                model_info["param_defaults"],
                model_info["param_ranges"]
        )):
            ttk.Label(self.params_frame, text=f"{name}:").grid(row=i, column=0, sticky=tk.W, pady=2)
            entry = ttk.Entry(self.params_frame, width=15)
            entry.grid(row=i, column=1, sticky=tk.W, padx=(5, 0), pady=2)
            entry.insert(0, str(default))
            self.param_entries[param] = entry

            ttk.Label(self.params_frame, text=f"({range_val[0]}-{range_val[1]})",
                      font=('Arial', 8)).grid(row=i, column=2, sticky=tk.W, padx=(5, 0), pady=2)

        self.ic_entries = {}
        for i, (ic, name, default) in enumerate(zip(
                model_info["initial_conditions"],
                model_info["ic_names"],
                model_info["ic_defaults"]
        )):
            ttk.Label(self.ic_frame, text=f"{name}:").grid(row=i, column=0, sticky=tk.W, pady=2)
            entry = ttk.Entry(self.ic_frame, width=15)
            entry.grid(row=i, column=1, sticky=tk.W, padx=(5, 0), pady=2)
            entry.insert(0, str(default))
            self.ic_entries[ic] = entry

    def show_math_window(self):
        try:
            model_info = self.models.models[self.current_model]
            parameters = {}
            for param in model_info["parameters"]:
                parameters[param] = float(self.param_entries[param].get())

            if self.math_window:
                self.math_window.window.destroy()

            self.math_window = MathDisplayWindow(self.root, model_info, parameters)

        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wyświetlić równań: {str(e)}")

    def analyze_stability(self):
        try:
            model_info = self.models.models[self.current_model]
            parameters = {}
            for param in model_info["parameters"]:
                parameters[param] = float(self.param_entries[param].get())

            analysis_text = f"Analiza stabilności: {model_info['name']}\n\n"

            if self.current_model == "logistic":
                r = parameters['r']
                K = parameters['K']
                analysis_text += f"Punkt równowagi: x* = {K}\n"
                analysis_text += f"Stabilność: Stabilny dla r > 0 (r = {r})\n"
                analysis_text += f"Czas podwojenia: t₂ ≈ {0.693 / r:.2f}\n"
                analysis_text += f"Czas do 95% K: t₉₅ ≈ {3 / r:.2f}\n"

            elif self.current_model == "lotka_volterra":
                a, b, c, d = parameters['a'], parameters['b'], parameters['c'], parameters['d']
                x_eq = d / c
                y_eq = a / b
                analysis_text += f"Punkt równowagi: ({x_eq:.2f}, {y_eq:.2f})\n"
                analysis_text += f"Typ: Neutralnie stabilny (centrum)\n"
                analysis_text += f"Okres oscylacji: T ≈ {2 * np.pi / np.sqrt(a * d):.2f}\n"

            elif self.current_model == "competition":
                alpha, beta = parameters['alpha'], parameters['beta']
                K1, K2 = parameters['K1'], parameters['K2']
                analysis_text += f"Współczynniki konkurencji: α = {alpha}, β = {beta}\n"
                analysis_text += f"Warunek koegzystencji: αβ = {alpha * beta:.3f}\n"
                if alpha * beta < 1:
                    analysis_text += "✓ Koegzystencja możliwa (αβ < 1)\n"
                    x_coex = (K1 - alpha * K2) / (1 - alpha * beta)
                    y_coex = (K2 - beta * K1) / (1 - alpha * beta)
                    if x_coex > 0 and y_coex > 0:
                        analysis_text += f"Punkt koegzystencji: ({x_coex:.1f}, {y_coex:.1f})\n"
                else:
                    analysis_text += "❌ Koegzystencja niemożliwa (αβ ≥ 1)\n"

            elif self.current_model == "sir":
                beta, gamma = parameters['beta'], parameters['gamma']
                R0 = beta / gamma
                analysis_text += f"Podstawowa liczba reprodukcji: R₀ = {R0:.2f}\n"
                if R0 > 1:
                    analysis_text += "✓ Epidemia się rozwinie (R₀ > 1)\n"
                    analysis_text += f"Próg stadnej odporności: {(1 - 1 / R0) * 100:.1f}%\n"
                else:
                    analysis_text += "❌ Epidemia wygaśnie (R₀ ≤ 1)\n"

            messagebox.showinfo("Analiza stabilności", analysis_text)

        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się przeprowadzić analizy: {str(e)}")

    def calculate_properties(self):
        try:
            if not self.time_data or not self.population_data:
                messagebox.showwarning("Ostrzeżenie", "Najpierw uruchom symulację!")
                return

            model_info = self.models.models[self.current_model]

            properties_text = f"Właściwości numeryczne: {model_info['name']}\n\n"

            # Podstawowe statystyki
            final_time = self.time_data[-1]
            properties_text += f"Czas symulacji: {final_time:.2f}\n"
            properties_text += f"Liczba kroków: {len(self.time_data)}\n"

            for i, (var_name, data) in enumerate(zip(model_info['var_names'], self.population_data)):
                min_val = min(data)
                max_val = max(data)
                final_val = data[-1]
                mean_val = np.mean(data)

                properties_text += f"\n{var_name}:\n"
                properties_text += f"  Minimum: {min_val:.3f}\n"
                properties_text += f"  Maksimum: {max_val:.3f}\n"
                properties_text += f"  Wartość końcowa: {final_val:.3f}\n"
                properties_text += f"  Średnia: {mean_val:.3f}\n"

                if len(data) > 100:
                    diff = np.diff(data)
                    sign_changes = np.sum(np.diff(np.sign(diff)) != 0)
                    if sign_changes > 10:
                        properties_text += f"  Oscylacje: {sign_changes // 2} cykli\n"

            if self.current_model == "lotka_volterra" and len(self.population_data) == 2:
                parameters = {}
                for param in model_info["parameters"]:
                    parameters[param] = float(self.param_entries[param].get())

                a, b, c, d = parameters['a'], parameters['b'], parameters['c'], parameters['d']

                H_values = []
                for x, y in zip(self.population_data[0], self.population_data[1]):
                    if x > 0 and y > 0:
                        H = c * x + b * y - d * np.log(x) - a * np.log(y)
                        H_values.append(H)

                if H_values:
                    H_variation = max(H_values) - min(H_values)
                    H_error = H_variation / abs(H_values[0]) * 100
                    properties_text += f"\nZachowanie Hamiltonianu:\n"
                    properties_text += f"  Zmiana: {H_variation:.6f}\n"
                    properties_text += f"  Błąd względny: {H_error:.4f}%\n"

            messagebox.showinfo("Właściwości modelu", properties_text)

        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się obliczyć właściwości: {str(e)}")

    def export_plot(self, plot_type):
        try:
            if not self.time_data or not self.population_data:
                messagebox.showwarning("Ostrzeżenie", "Najpierw uruchom symulację!")
                return

            # Wybierz plik do zapisu
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            model_name = self.current_model

            if plot_type == 'time':
                default_name = f"{model_name}_czasowy_{timestamp}.png"
            elif plot_type == 'phase':
                default_name = f"{model_name}_fazowy_{timestamp}.png"
            else:
                default_name = f"{model_name}_kompletny_{timestamp}.png"

            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                initialfilename=default_name,
                filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("SVG files", "*.svg"), ("All files", "*.*")]
            )

            if not filename:
                return

            model_info = self.models.models[self.current_model]

            if plot_type == 'time':
                fig, ax = plt.subplots(figsize=(12, 8))
                colors = ['blue', 'red', 'green', 'orange', 'purple']

                for i, (data, name) in enumerate(zip(self.population_data, model_info['var_names'])):
                    ax.plot(self.time_data, data, color=colors[i % len(colors)],
                            linewidth=2, label=name)

                ax.set_xlabel('Czas', fontsize=12)
                ax.set_ylabel('Wielkość populacji', fontsize=12)
                ax.set_title(f'{model_info["name"]} - Dynamika czasowa', fontsize=14)
                ax.grid(True, alpha=0.3)
                ax.legend()

                fig.tight_layout()
                fig.savefig(filename, dpi=300, bbox_inches='tight')
                plt.close(fig)

            elif plot_type == 'phase':
                if len(self.population_data) < 2:
                    messagebox.showwarning("Ostrzeżenie", "Płaszczyzna fazowa dostępna tylko dla modeli 2D!")
                    return

                fig, ax = plt.subplots(figsize=(10, 8))

                x_data = self.population_data[0]
                y_data = self.population_data[1]

                ax.plot(x_data, y_data, 'b-', linewidth=2, alpha=0.8)
                ax.plot(x_data[0], y_data[0], 'go', markersize=10, label='Start')
                ax.plot(x_data[-1], y_data[-1], 'ro', markersize=10, label='Koniec')

                ax.set_xlabel(model_info['var_names'][0], fontsize=12)
                ax.set_ylabel(model_info['var_names'][1], fontsize=12)
                ax.set_title(f'{model_info["name"]} - Płaszczyzna fazowa', fontsize=14)
                ax.grid(True, alpha=0.3)
                ax.legend()

                fig.tight_layout()
                fig.savefig(filename, dpi=300, bbox_inches='tight')
                plt.close(fig)

            else:  # both
                if len(self.population_data) >= 2:
                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
                else:
                    fig, ax1 = plt.subplots(1, 1, figsize=(12, 8))
                    ax2 = None

                # Wykres czasowy
                colors = ['blue', 'red', 'green', 'orange', 'purple']
                for i, (data, name) in enumerate(zip(self.population_data, model_info['var_names'])):
                    ax1.plot(self.time_data, data, color=colors[i % len(colors)],
                             linewidth=2, label=name)

                ax1.set_xlabel('Czas', fontsize=12)
                ax1.set_ylabel('Wielkość populacji', fontsize=12)
                ax1.set_title(f'{model_info["name"]} - Dynamika czasowa', fontsize=14)
                ax1.grid(True, alpha=0.3)
                ax1.legend()

                # Płaszczyzna fazowa
                if ax2 and len(self.population_data) >= 2:
                    x_data = self.population_data[0]
                    y_data = self.population_data[1]

                    ax2.plot(x_data, y_data, 'b-', linewidth=2, alpha=0.8)
                    ax2.plot(x_data[0], y_data[0], 'go', markersize=8, label='Start')
                    ax2.plot(x_data[-1], y_data[-1], 'ro', markersize=8, label='Koniec')

                    ax2.set_xlabel(model_info['var_names'][0], fontsize=12)
                    ax2.set_ylabel(model_info['var_names'][1], fontsize=12)
                    ax2.set_title(f'{model_info["name"]} - Płaszczyzna fazowa', fontsize=14)
                    ax2.grid(True, alpha=0.3)
                    ax2.legend()

                fig.tight_layout()
                fig.savefig(filename, dpi=300, bbox_inches='tight')
                plt.close(fig)

            messagebox.showinfo("Sukces", f"Wykres zapisany jako {filename}")

        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się eksportować wykresu: {str(e)}")

    def export_data_csv(self):
        try:
            if not self.time_data or not self.population_data:
                messagebox.showwarning("Ostrzeżenie", "Najpierw uruchom symulację!")
                return

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            model_name = self.current_model
            default_name = f"{model_name}_dane_{timestamp}.csv"

            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                initialfilename=default_name,
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )

            if not filename:
                return

            model_info = self.models.models[self.current_model]

            import csv
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)

                # Nagłówek
                header = ['Czas'] + model_info['var_names']
                writer.writerow(header)

                # Dane
                for i, t in enumerate(self.time_data):
                    row = [t]
                    for pop_data in self.population_data:
                        row.append(pop_data[i] if i < len(pop_data) else '')
                    writer.writerow(row)

            messagebox.showinfo("Sukces", f"Dane zapisane jako {filename}")

        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się eksportować danych: {str(e)}")

    def create_model_functions(self, model_key: str, parameters: Dict) -> List[Callable]:
        """Tworzy funkcje modelu z parametrami"""
        model_info = self.models.models[model_key]
        functions = []

        for eq_str in model_info["equations"]:
            eq_eval = eq_str
            for param, value in parameters.items():
                eq_eval = eq_eval.replace(param, str(value))

            if model_info["type"] == "single":
                func = lambda t, x, eq=eq_eval: eval(eq, {"t": t, "x": x, "np": np})
            else:
                var_names = model_info["variables"]
                if len(var_names) == 2:
                    func = lambda t, x, y, eq=eq_eval: eval(eq, {"t": t, "x": x, "y": y, "np": np})
                elif len(var_names) == 3:
                    func = lambda t, S, I, R, eq=eq_eval: eval(eq, {"t": t, "S": S, "I": I, "R": R, "np": np})
                else:
                    # Ogólny przypadek
                    def make_func(eq_str):
                        def func(t, *args):
                            local_vars = {"t": t, "np": np}
                            for i, var in enumerate(var_names):
                                local_vars[var] = args[i]
                            return eval(eq_str, local_vars)

                        return func

                    func = make_func(eq_eval)

            functions.append(func)

        return functions

    def prepare_animation_data(self):
        try:
            model_info = self.models.models[self.current_model]

            parameters = {}
            for param in model_info["parameters"]:
                parameters[param] = float(self.param_entries[param].get())

            initial_conditions = []
            for ic in model_info["initial_conditions"]:
                initial_conditions.append(float(self.ic_entries[ic].get()))

            time_end = float(self.time_entry.get())
            h = float(self.step_entry.get())
            self.max_steps = int(time_end / h)

            functions = self.create_model_functions(self.current_model, parameters)

            if model_info["type"] == "single":
                self.solver_generator = self.solver.solve_single_ode_animated(
                    functions[0], 0, initial_conditions[0], h, self.max_steps)
            else:
                self.solver_generator = self.solver.solve_system_ode_animated(
                    functions, 0, initial_conditions, h, self.max_steps)

            # Wyczyść dane
            self.time_data = []
            self.population_data = []
            self.phase_data = []
            self.current_step = 0

            self.setup_animation_plots(model_info)

            return True

        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się przygotować animacji: {str(e)}")
            return False

    def setup_animation_plots(self, model_info):

        self.time_ax.clear()
        self.time_ax.set_xlabel('Czas', fontsize=12)
        self.time_ax.set_ylabel('Wielkość populacji', fontsize=12)
        self.time_ax.set_title(f'{model_info["name"]} - Animowana dynamika', fontsize=14)
        self.time_ax.grid(True, alpha=0.3)

        colors = ['blue', 'red', 'green', 'orange', 'purple']
        self.time_lines = []
        self.time_points = []

        for i, name in enumerate(model_info["var_names"]):
            line, = self.time_ax.plot([], [], color=colors[i % len(colors)],
                                      linewidth=2, label=name)
            point, = self.time_ax.plot([], [], 'o', color=colors[i % len(colors)],
                                       markersize=8)
            self.time_lines.append(line)
            self.time_points.append(point)

        self.time_ax.legend()

        self.phase_ax.clear()
        if len(model_info["var_names"]) == 2:
            self.phase_ax.set_xlabel(model_info["var_names"][0], fontsize=12)
            self.phase_ax.set_ylabel(model_info["var_names"][1], fontsize=12)
            self.phase_ax.set_title(f'{model_info["name"]} - Płaszczyzna fazowa', fontsize=14)
            self.phase_ax.grid(True, alpha=0.3)

            self.phase_line, = self.phase_ax.plot([], [], 'b-', linewidth=2, alpha=0.7)
            self.phase_point, = self.phase_ax.plot([], [], 'ro', markersize=10)
        else:
            self.phase_ax.text(0.5, 0.5, 'Płaszczyzna fazowa dostępna\ntylko dla modeli 2D',
                               ha='center', va='center', transform=self.phase_ax.transAxes,
                               fontsize=14)

        self.time_canvas.draw()
        self.phase_canvas.draw()

    def animate_step(self):
        try:
            t, values = next(self.solver_generator)

            self.time_data.append(t)
            if isinstance(values, list):
                if len(self.population_data) == 0:
                    self.population_data = [[] for _ in range(len(values))]
                for i, val in enumerate(values):
                    self.population_data[i].append(val)

                # Dane dla płaszczyzny fazowej (tylko 2D)
                if len(values) == 2:
                    self.phase_data.append([values[0], values[1]])
            else:
                if len(self.population_data) == 0:
                    self.population_data = [[]]
                self.population_data[0].append(values)

            self.update_animation_plots()

            self.current_step += 1
            progress = (self.current_step / self.max_steps) * 100
            self.progress_var.set(progress)

            self.status_label.config(text=f"Krok {self.current_step}/{self.max_steps} (t={t:.2f})")

            if self.current_step >= self.max_steps:
                self.stop_animation()
                self.status_label.config(text="Animacja zakończona - można eksportować wykresy")
                return False

            return True

        except StopIteration:
            self.stop_animation()
            self.status_label.config(text="Animacja zakończona - można eksportować wykresy")
            return False
        except Exception as e:
            self.stop_animation()
            self.status_label.config(text=f"Błąd animacji: {str(e)}")
            return False

    def update_animation_plots(self):

        # Wykres czasowy
        for i, (line, point) in enumerate(zip(self.time_lines, self.time_points)):
            if i < len(self.population_data):
                line.set_data(self.time_data, self.population_data[i])
                if len(self.population_data[i]) > 0:
                    point.set_data([self.time_data[-1]], [self.population_data[i][-1]])

        # Automatyczne skalowanie
        if len(self.time_data) > 0:
            self.time_ax.set_xlim(0, max(self.time_data) * 1.1)

            all_values = []
            for pop_data in self.population_data:
                all_values.extend(pop_data)

            if all_values:
                min_val = min(all_values)
                max_val = max(all_values)
                margin = (max_val - min_val) * 0.1
                self.time_ax.set_ylim(min_val - margin, max_val + margin)

        # Płaszczyzna fazowa
        if len(self.phase_data) > 0 and hasattr(self, 'phase_line'):
            x_data = [point[0] for point in self.phase_data]
            y_data = [point[1] for point in self.phase_data]

            self.phase_line.set_data(x_data, y_data)
            self.phase_point.set_data([x_data[-1]], [y_data[-1]])

            # Automatyczne skalowanie płaszczyzny fazowej
            if len(x_data) > 0:
                x_margin = (max(x_data) - min(x_data)) * 0.1
                y_margin = (max(y_data) - min(y_data)) * 0.1
                self.phase_ax.set_xlim(min(x_data) - x_margin, max(x_data) + x_margin)
                self.phase_ax.set_ylim(min(y_data) - y_margin, max(y_data) + y_margin)

        self.time_canvas.draw_idle()
        self.phase_canvas.draw_idle()

    def animation_loop(self):
        if self.is_playing:
            success = self.animate_step()
            if success:
                delay = int(50 / self.speed_var.get())  # 50ms opóźnienie
                self.root.after(delay, self.animation_loop)

    def start_animation(self):
        if not self.is_playing:
            if self.current_step == 0:
                if not self.prepare_animation_data():
                    return

            self.is_playing = True
            self.play_button.config(text="▶ Odtwarzanie...", state="disabled")
            self.pause_button.config(state="normal")
            self.stop_button.config(state="normal")

            self.animation_loop()

    def pause_animation(self):
        self.is_playing = False
        self.play_button.config(text="▶ Wznów", state="normal")
        self.pause_button.config(state="disabled")
        self.status_label.config(text="Animacja wstrzymana")

    def stop_animation(self):
        self.is_playing = False
        self.current_step = 0
        self.progress_var.set(0)

        self.play_button.config(text="▶ Start", state="normal")
        self.pause_button.config(state="disabled")
        self.stop_button.config(state="disabled")

        self.status_label.config(text="Gotowy do animacji")

    def on_speed_change(self, event=None):
        speed = self.speed_var.get()
        self.speed_label.config(text=f"{speed:.1f}x")

    def save_parameters(self):
        try:
            model_info = self.models.models[self.current_model]

            data = {
                "model": self.current_model,
                "parameters": {},
                "initial_conditions": {},
                "simulation": {
                    "time": self.time_entry.get(),
                    "step": self.step_entry.get()
                }
            }

            for param in model_info["parameters"]:
                data["parameters"][param] = self.param_entries[param].get()

            for ic in model_info["initial_conditions"]:
                data["initial_conditions"][ic] = self.ic_entries[ic].get()

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_name = f"parametry_{self.current_model}_{timestamp}.json"

            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                initialfilename=default_name,
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )

            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                messagebox.showinfo("Sukces", f"Parametry zapisane do pliku {filename}")

        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zapisać parametrów: {str(e)}")

    def load_parameters(self):
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )

            if not filename:
                return

            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if data["model"] != self.current_model:
                self.model_var.set(data["model"])
                self.on_model_change()

            for param, value in data["parameters"].items():
                if param in self.param_entries:
                    self.param_entries[param].delete(0, tk.END)
                    self.param_entries[param].insert(0, str(value))

            for ic, value in data["initial_conditions"].items():
                if ic in self.ic_entries:
                    self.ic_entries[ic].delete(0, tk.END)
                    self.ic_entries[ic].insert(0, str(value))

            self.time_entry.delete(0, tk.END)
            self.time_entry.insert(0, data["simulation"]["time"])
            self.step_entry.delete(0, tk.END)
            self.step_entry.insert(0, data["simulation"]["step"])

            messagebox.showinfo("Sukces", f"Parametry wczytane z pliku {filename}")

        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wczytać parametrów: {str(e)}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AnimatedPopulationGUI()
    app.run()
