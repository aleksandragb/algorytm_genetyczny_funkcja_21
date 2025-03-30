import tkinter as tk
from tkinter import ttk
from ga import GeneticAlgorithm

class AppGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Algorytm Genetyczny")
        self._add_widgets()
        self.window.mainloop()

    def _add_widgets(self):
        labels = ["Liczba osobników:", "Liczba epok:", "Liczba zmiennych:"]
        defaults = ["20", "50", "2"]
        self.entries = []

        for i, (label, default) in enumerate(zip(labels, defaults)):
            ttk.Label(self.window, text=label).grid(row=i, column=0, sticky="w")
            entry = ttk.Entry(self.window)
            entry.grid(row=i, column=1)
            entry.insert(0, default)
            self.entries.append(entry)

        self.selection_method = self._add_combobox("Metoda selekcji:", ["elitist", "roulette", "tournament"], 3)
        self.crossover_method = self._add_combobox("Metoda krzyżowania:", ["one_point", "two_point", "uniform", "none"], 4)
        self.mutation_method = self._add_combobox("Metoda mutacji:", ["one_point", "two_point", "boundary", "none"], 5)

        self.inversion_var = tk.BooleanVar()
        ttk.Checkbutton(self.window, text="Użyj operatora inwersji", variable=self.inversion_var).grid(row=6, column=0, columnspan=2, sticky="w")

        ttk.Button(self.window, text="Start", command=self.run_algorithm).grid(row=7, column=0, columnspan=2, pady=10)

        self.result_label = ttk.Label(self.window, text="")
        self.result_label.grid(row=8, column=0, columnspan=2)

    def _add_combobox(self, text, options, row):
        ttk.Label(self.window, text=text).grid(row=row, column=0, sticky="w")
        box = ttk.Combobox(self.window, values=options)
        box.grid(row=row, column=1)
        box.current(0)
        return box

    def run_algorithm(self):
        try:
            pop_size = int(self.entries[0].get())
            generations = int(self.entries[1].get())
            selection = self.selection_method.get()
            crossover = self.crossover_method.get()
            mutation = self.mutation_method.get()
            inversion = self.inversion_var.get()

            ga = GeneticAlgorithm(pop_size, generations, selection, crossover, mutation, inversion)
            result = ga.run()
            self.result_label.config(text=f"Najlepszy wynik: {result}")
        except Exception as e:
            self.result_label.config(text=f"Błąd: {e}")
