import tkinter as tk
from tkinter import ttk
from ga import run_algorithm

def start_algorithm():
    try:
        population = int(pop_entry.get())
        generations = int(gen_entry.get())
        variables = int(var_entry.get())
        min_val = float(min_val_entry.get())
        max_val = float(max_val_entry.get())
        uniform_prob = float(uniform_prob_entry.get())
        use_inversion_flag = inversion_var.get()
        elitism = elitism_enabled.get()

        method_map = {
            "najlepszych osobników": "elitist",
            "ruletki": "roulette",
            "turniejowa": "tournament"
        }
        crossover_map = {
            "jednopunktowe": "one_point",
            "dwupunktowe": "two_point",
            "jednorodne": "uniform",
            "ziarniste": "granular",
            "żadne": "none"
        }
        mutation_map = {
            "jednopunktowe": "one_point",
            "dwupunktowe": "two_point",
            "brzegowe": "boundary",
            "żadne": "none"
        }

        method = method_map.get(selection_method.get(), "elitist")
        cross_method = crossover_map.get(crossover_method.get(), "one_point")
        mutation = mutation_map.get(mutation_method.get(), "one_point")

        result = run_algorithm(population, generations, variables, method, cross_method, mutation,
                               use_inversion_flag, elitism, min_val=min_val, max_val=max_val,
                               uniform_prob=uniform_prob)

        result_label.config(text=f"Najlepszy wynik: {result}")
    except Exception as e:
        result_label.config(text=f"Błąd: {e}")

def create_gui():
    window = tk.Tk()
    window.title("Algorytm Genetyczny")
    window.geometry("400x400")

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

    ttk.Label(window, text="Początek zakresu:").grid(row=3, column=0, sticky="w")
    global min_val_entry
    min_val_entry = ttk.Entry(window)
    min_val_entry.grid(row=3, column=1)
    min_val_entry.insert(0, "-5")

    ttk.Label(window, text="Koniec zakresu:").grid(row=4, column=0, sticky="w")
    global max_val_entry
    max_val_entry = ttk.Entry(window)
    max_val_entry.grid(row=4, column=1)
    max_val_entry.insert(0, "5")

    ttk.Label(window, text="Metoda selekcji:").grid(row=5, column=0, sticky="w")
    global selection_method
    selection_method = ttk.Combobox(window, values=["najlepszych osobników", "ruletki", "turniejowa"])
    selection_method.grid(row=5, column=1)
    selection_method.current(0)

    ttk.Label(window, text="Metoda krzyżowania:").grid(row=6, column=0, sticky="w")
    global crossover_method
    crossover_method = ttk.Combobox(window, values=["jednopunktowe", "dwupunktowe", "jednorodne", "ziarniste", "żadne"])
    crossover_method.grid(row=6, column=1)
    crossover_method.current(0)

    ttk.Label(window, text="Metoda mutacji:").grid(row=7, column=0, sticky="w")
    global mutation_method
    mutation_method = ttk.Combobox(window, values=["jednopunktowe", "dwupunktowe", "brzegowe", "żadne"])
    mutation_method.grid(row=7, column=1)
    mutation_method.current(0)

    ttk.Label(window, text="Prawdopodobieństwo krzyżowania (p):").grid(row=8, column=0, sticky="w")
    global uniform_prob_entry
    uniform_prob_entry = ttk.Entry(window)
    uniform_prob_entry.grid(row=8, column=1)
    uniform_prob_entry.insert(0, "0.5")

    global inversion_var
    inversion_var = tk.BooleanVar()
    inversion_check = ttk.Checkbutton(window, text="Użyj operatora inwersji", variable=inversion_var)
    inversion_check.grid(row=9, column=0, columnspan=2, sticky="w")

    global elitism_enabled
    elitism_enabled = tk.BooleanVar()
    elitism_enabled.set(True)
    elitism_checkbox = ttk.Checkbutton(window, text="Użyj strategii elitarnej", variable=elitism_enabled)
    elitism_checkbox.grid(row=10, column=0, columnspan=2, sticky="w")

    start_btn = ttk.Button(window, text="Start", command=start_algorithm)
    start_btn.grid(row=11, column=0, columnspan=2, pady=10)

    global result_label
    result_label = ttk.Label(window, text="")
    result_label.grid(row=12, column=0, columnspan=2)

    window.mainloop()
