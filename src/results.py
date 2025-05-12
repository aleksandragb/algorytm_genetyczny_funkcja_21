import matplotlib.pyplot as plt
import numpy as np

# Ustawienie backendu w trybie bez GUI
import matplotlib
matplotlib.use("Agg")

def plot_results(fitness_values, generations):
    plt.figure(figsize=(12, 6))
    for idx, fitness in enumerate(fitness_values):
        # Dopasuj długość generations do długości fitness
        min_length = min(len(generations), len(fitness))
        plt.plot(generations[:min_length], fitness[:min_length], label=f'Run {idx+1}')
    plt.title("Fitness w kolejnych generacjach")
    plt.xlabel("Generacja")
    plt.ylabel("Fitness")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', ncol=2)
    plt.tight_layout()
    plt.savefig("fitness_plot.png")
    print("Wykres zapisany jako 'fitness_plot.png'.")

def print_results(solution, fitness):
    print(f"Najlepsze rozwiązanie: {solution}")
    print(f"Wartość funkcji celu: {1.0 / fitness}")