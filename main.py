import random
import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

G = 9.81
POCET = 50
M_MIN, M_MAX = 1, 100

def generuj_hmotnosti(n=POCET):
    return [round(random.uniform(M_MIN, M_MAX), 2) for _ in range(n)]

def zorad(hodnoty):
    return sorted(hodnoty)

def sila(hmotnost):
    return hmotnost * G


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gravitačná sila F = m·g")
        self.geometry("1100x620")
        self.minsize(1000, 560)

        self.hmotnosti = []
        self.sily = []

        self._vytvor_gui()
        self.generuj()
        
    def _vytvor_gui(self):
        panel = ttk.Frame(self, padding=10, width=320)
        panel.pack(side="left", fill="y")
        panel.pack_propagate(False)
        panel.grid_propagate(False)

        ttk.Label(panel, text="Gravitačná sila  F = m · g",
                  font=("Arial", 13, "bold")).grid(row=0, column=0, columnspan=2,
                                                   sticky="w", pady=(0, 10))

        ttk.Button(panel, text="Generovať nové hodnoty",
                   command=self.generuj).grid(row=1, column=0, columnspan=2,
                                              sticky="ew", pady=(0, 15))

        self.v_min_m = tk.StringVar()
        self.v_max_m = tk.StringVar()
        self.v_min_f = tk.StringVar()
        self.v_max_f = tk.StringVar()

        riadky = [
            ("Min. hmotnosť:", self.v_min_m),
            ("Max. hmotnosť:", self.v_max_m),
            ("Min. sila:", self.v_min_f),
            ("Max. sila:", self.v_max_f),
        ]
        for i, (text, var) in enumerate(riadky, start=2):
            ttk.Label(panel, text=text, width=16, anchor="w").grid(
                row=i, column=0, sticky="w", pady=2)
            ttk.Label(panel, textvariable=var, width=14, anchor="w",
                      font=("Arial", 10, "bold")).grid(row=i, column=1, sticky="w", pady=2)

        ttk.Separator(panel).grid(row=6, column=0, columnspan=2, sticky="ew", pady=15)

        ttk.Label(panel, text="Zadaj hmotnosť [kg]:").grid(
            row=7, column=0, columnspan=2, sticky="w")
        self.vstup = ttk.Entry(panel, width=20)
        self.vstup.grid(row=8, column=0, sticky="ew", pady=5)
        self.vstup.bind("<Return>", lambda e: self.vypocitaj())
        ttk.Button(panel, text="Vypočítať F",
                   command=self.vypocitaj).grid(row=8, column=1, sticky="ew",
                                                padx=(5, 0), pady=5)

        self.v_vysledok = tk.StringVar(value="F = –")
        ttk.Label(panel, textvariable=self.v_vysledok, width=32, anchor="w",
                  font=("Arial", 11, "bold")).grid(row=9, column=0, columnspan=2,
                                                   sticky="w", pady=5)

        panel.columnconfigure(0, weight=1)
        panel.columnconfigure(1, weight=1)

        self.fig = Figure(figsize=(7, 5), dpi=100)
        self.ax1 = self.fig.add_subplot(111)
        self.ax2 = self.ax1.twinx()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side="right", fill="both", expand=True)

    def generuj(self):
        self.hmotnosti = generuj_hmotnosti()
        self.sily = [sila(m) for m in self.hmotnosti]
        self._aktualizuj_statistiky()
        self._nakresli_graf()

    def _aktualizuj_statistiky(self):
        m = zorad(self.hmotnosti)
        f = zorad(self.sily)
        self.v_min_m.set(f"{m[0]:.2f} kg")
        self.v_max_m.set(f"{m[-1]:.2f} kg")
        self.v_min_f.set(f"{f[0]:.2f} N")
        self.v_max_f.set(f"{f[-1]:.2f} N")

    def _nakresli_graf(self):
        self.ax1.clear()
        self.ax2.clear()
        x = list(range(1, len(self.hmotnosti) + 1))

        l1, = self.ax1.plot(x, self.hmotnosti, color="tab:blue", marker="o",
                            markersize=4, label="Hmotnosť m [kg]")
        l2, = self.ax2.plot(x, self.sily, color="tab:red", marker="s",
                            markersize=4, label="Sila F [N]")

        self.ax1.set_title("Pôvodné hodnoty (m) a vypočítané hodnoty (F = m·g)")
        self.ax1.set_xlabel("Poradie merania")
        self.ax1.set_ylabel("Hmotnosť m [kg]", color="tab:blue")
        self.ax2.set_ylabel("Sila F [N]", color="tab:red")

        self.ax1.set_ylim(0, M_MAX * 1.1)
        self.ax2.set_ylim(0, M_MAX * 1.1 * G)
        self.ax1.set_xlim(0, POCET + 1)
        self.ax1.grid(True, alpha=0.3)

        self.ax1.legend(handles=[l1, l2], loc="upper left")

        self.fig.tight_layout()
        self.canvas.draw()

    def vypocitaj(self):
        text = self.vstup.get().strip().replace(",", ".")
        try:
            m = float(text)
        except ValueError:
            messagebox.showerror("Chyba", "Zadaj platné číslo (napr. 12.5).")
            return
        self.v_vysledok.set(f"F = {sila(m):.2f} N")

if __name__ == "__main__":
    App().mainloop()
