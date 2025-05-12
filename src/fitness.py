import numpy as np
import benchmark_functions as bf

# Funkcja dekodująca osobnika binarnego na rzeczywiste wartości
def decode_solution(solution):
    x_bin = ''.join(map(str, solution[:20]))
    y_bin = ''.join(map(str, solution[20:40]))
    z_bin = ''.join(map(str, solution[40:60]))
    x = int(x_bin, 2) / (2**20) * 4 - 2
    y = int(y_bin, 2) / (2**20) * 4 - 2
    z = int(z_bin, 2) / (2**20) * 4 - 2
    return np.array([x, y, z])

# Funkcja celu (Hyperellipsoid)
def fitness_func(ga_instance, solution, solution_idx, decode_solution):
    ind = decode_solution(solution)
    func = bf.Hyperellipsoid(n_dimensions=3)
    result = func(ind)
    return 1.0 / (1.0 + result)