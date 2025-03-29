def binary_to_real(binary_str, min_val, max_val, bits):
    int_val = int(binary_str, 2)
    max_int = 2**bits - 1
    return min_val + (int_val / max_int) * (max_val - min_val)

import csv

def save_results_to_csv(progress, filename="results.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Generation", "Best Fitness"])
        for i, fitness in enumerate(progress):
            writer.writerow([i + 1, fitness])