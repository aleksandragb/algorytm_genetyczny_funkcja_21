import tkinter as tk
from tkinter import ttk
from ga import run_algorithm

def start_algorithm():
    try:
        population = int(pop_entry.get())
        generations = int(gen_entry.get())
        variables = int(var_entry.get())
        method = selection_method.get()
        cross_method = crossover_method.get()

        result = run_algorithm(population, generations, variables, method, cross_method)
        result_label.config(text=f"Najlepszy wynik: {result}")
    except Exception as e:
        result_label.config(text=f"Błąd: {e}")

def create_gui():
    window = tk.Tk()
    window.title("Algorytm Genetyczny")

    ttk.Label(window, text="Liczba osobników:").grid(row=0, column=0, sticky="w")
    global pop_entry
    pop_entry = ttk.Entry(window)
    pop_entry.grid(row=0, column=1)
    pop_entry.insert(0, "20")

    ttk.Label(window, text="Liczba epok:").grid(row=1, column=0, sticky="w")
    global gen_entry
    gen_entry = ttk.Entry(window)
    gen_entry.grid(row=1, column=1)
    gen_entry.insert(0, "50")

    ttk.Label(window, text="Liczba zmiennych:").grid(row=2, column=0, sticky="w")
    global var_entry
    var_entry = ttk.Entry(window)
    var_entry.grid(row=2, column=1)
    var_entry.insert(0, "2")

    ttk.Label(window, text="Metoda selekcji:").grid(row=3, column=0, sticky="w")
    global selection_method
    selection_method = ttk.Combobox(window, values=["elitist", "roulette", "tournament"])
    selection_method.grid(row=3, column=1)
    selection_method.current(0)

    ttk.Label(window, text="Metoda krzyżowania:").grid(row=4, column=0, sticky="w")
    global crossover_method
    crossover_method = ttk.Combobox(window, values=["one_point", "two_point", "uniform", "none"])
    crossover_method.grid(row=4, column=1)
    crossover_method.current(0)

    start_btn = ttk.Button(window, text="Start", command=start_algorithm)
    start_btn.grid(row=5, column=0, columnspan=2, pady=10)

    global result_label
    result_label = ttk.Label(window, text="")
    result_label.grid(row=6, column=0, columnspan=2)

    window.mainloop()
