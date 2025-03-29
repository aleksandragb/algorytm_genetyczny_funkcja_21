import random
from functions import himmelblau
from utils import binary_to_real
from plot import plot_progress
from utils import save_results_to_csv

MIN_VAL = -5
MAX_VAL = 5
BITS_PER_VAR = 16
CHROMOSOME_LENGTH = BITS_PER_VAR * 2  # x + y

def generate_chromosome():
    return ''.join(random.choice('01') for _ in range(CHROMOSOME_LENGTH))

def decode_chromosome(chrom):
    x_bin = chrom[:BITS_PER_VAR]
    y_bin = chrom[BITS_PER_VAR:]
    x = binary_to_real(x_bin, MIN_VAL, MAX_VAL, BITS_PER_VAR)
    y = binary_to_real(y_bin, MIN_VAL, MAX_VAL, BITS_PER_VAR)
    return [x, y]

def calculate_fitness(chrom):
    x, y = decode_chromosome(chrom)
    return himmelblau([x, y])

def selection(population, method="elitist", tournament_size=5):
    if method == "elitist":
        return sorted(population, key=lambda c: calculate_fitness(c))

    elif method == "roulette":
        fitnesses = [1 / (calculate_fitness(c) + 1e-6) for c in population]
        total = sum(fitnesses)
        probs = [f / total for f in fitnesses]
        selected = random.choices(population, weights=probs, k=len(population))
        return selected

    elif method == "tournament":
        selected = []
        for _ in range(len(population)):
            contenders = random.sample(population, tournament_size)
            winner = min(contenders, key=lambda c: calculate_fitness(c))
            selected.append(winner)
        return selected

    else:
        raise ValueError(f"Unknown selection method: {method}")


def crossover(parent1, parent2):
    point = random.randint(1, CHROMOSOME_LENGTH - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(chrom, mutation_rate=0.01):
    chrom_list = list(chrom)
    for i in range(len(chrom_list)):
        if random.random() < mutation_rate:
            chrom_list[i] = '1' if chrom_list[i] == '0' else '0'
    return ''.join(chrom_list)


def run_algorithm(pop_size, generations, variables=None, selection_method="elitist"):
    population = [generate_chromosome() for _ in range(pop_size)]
    best_solution = None
    best_fitness = float('inf')
    progress = []

    for _ in range(generations):
        sorted_pop = selection(population, method=selection_method)  # tymczasowo, później z GUI
        new_population = sorted_pop[:2]  # elitarna strategia

        while len(new_population) < pop_size:
            parent1, parent2 = random.sample(sorted_pop[:10], 2)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            new_population.extend([child1, child2])

        population = new_population[:pop_size]

        current_best = selection(population)[0]
        current_fitness = calculate_fitness(current_best)
        progress.append(current_fitness)

        if current_fitness < best_fitness:
            best_fitness = current_fitness
            best_solution = current_best

    x, y = decode_chromosome(best_solution)

    plot_progress(progress)
    save_results_to_csv(progress)

    return f"x = {x:.4f}, y = {y:.4f}, f(x,y) = {best_fitness:.4f}"

