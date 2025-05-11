import random
from functions import himmelblau
from utils import binary_to_real
from plot import plot_progress
from utils import save_results_to_csv
import time
from functions import himmelblau


def generate_chromosome(min_val, max_val, variables):
    return [random.uniform(min_val, max_val) for _ in range(variables)]

def calculate_fitness(chrom, objective_function):
    return objective_function(chrom)

def selection(population, method="elitist", tournament_size=5, objective_function=None):
    if method == "elitist":
        return sorted(population, key=lambda c: calculate_fitness(c, objective_function))

    elif method == "roulette":
        fitnesses = [1 / (calculate_fitness(c, objective_function) + 1e-6) for c in population]
        total = sum(fitnesses)
        probs = [f / total for f in fitnesses]
        selected = random.choices(population, weights=probs, k=len(population))
        return selected

    elif method == "tournament":
        selected = []
        for _ in range(len(population)):
            contenders = random.sample(population, tournament_size)
            winner = min(contenders, key=lambda c: calculate_fitness(c, objective_function))
            selected.append(winner)
        return selected


def crossover(parent1, parent2, method="one_point", alpha=0.5):
    if method == "one_point":
        point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]

    elif method == "two_point":
        point1 = random.randint(1, len(parent1) - 2)
        point2 = random.randint(point1 + 1, len(parent1) - 1)
        child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
        child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]

    elif method == "uniform":
        child1 = [p1 if random.random() < 0.5 else p2 for p1, p2 in zip(parent1, parent2)]
        child2 = [p2 if random.random() < 0.5 else p1 for p1, p2 in zip(parent1, parent2)]

    elif method == "arithmetic":
            child1 = [alpha * p1 + (1 - alpha) * p2 for p1, p2 in zip(parent1, parent2)]
            child2 = [(1 - alpha) * p1 + alpha * p2 for p1, p2 in zip(parent1, parent2)]
    
    elif method == "alpha_beta":
        beta = 1 - alpha  # lub dowolna inna wartość z GUI, jeżeli dodasz wejście dla beta
        child1 = [alpha * p1 + beta * p2 for p1, p2 in zip(parent1, parent2)]
        child2 = [beta * p1 + alpha * p2 for p1, p2 in zip(parent1, parent2)]

    elif method == "linear":
        child1 = [(p1 + p2) / 2 for p1, p2 in zip(parent1, parent2)]
        child2 = [2 * p1 - p2 for p1, p2 in zip(parent1, parent2)]

    elif method == "averaging":
        child = [(p1 + p2) / 2 for p1, p2 in zip(parent1, parent2)]
        return child, child  # zwracamy dwa takie same dzieci

    elif method == "none":
        child1 = parent1[:]
        child2 = parent2[:]

    else:
        raise ValueError(f"Unknown crossover method: {method}")

    return child1, child2

def uniform_mutation(chrom, mutation_rate):
    return [x + random.uniform(-mutation_rate, mutation_rate) for x in chrom]

def gaussian_mutation(chrom, mutation_rate):
    return [x + random.gauss(0, mutation_rate) for x in chrom]

def mutate(chrom, mutation_rate=0.1, method="one_point"):
    if method == "none":
        return chrom[:]
    
    mutated = chrom[:]
    if method == "one_point":
        index = random.randint(0, len(mutated) - 1)
        mutated[index] += random.uniform(-mutation_rate, mutation_rate)
    
    elif method == "two_point":
        indices = random.sample(range(len(mutated)), 2)
        for index in indices:
            mutated[index] += random.uniform(-mutation_rate, mutation_rate)
    
    elif method == "boundary":
        mutated[0] += random.uniform(-mutation_rate, mutation_rate)
        mutated[-1] += random.uniform(-mutation_rate, mutation_rate)

    elif method == "uniform":
        chrom = uniform_mutation(chrom, mutation_rate)
    
    elif method == "gaussian":
        chrom = gaussian_mutation(chrom, mutation_rate)

    else:
        raise ValueError(f"Unknown mutation method: {method}")

    return mutated


def inversion(chrom):
    chrom_list = list(chrom)
    start = random.randint(0, len(chrom_list) - 2)
    end = random.randint(start + 1, len(chrom_list) - 1)
    chrom_list[start:end + 1] = chrom_list[start:end + 1][::-1]
    return ''.join(chrom_list)


def run_algorithm(pop_size, generations, variables=2, selection_method="elitist", crossover_method="one_point", mutation_method="one_point", use_elitism=True, min_val=-5, max_val=5, objective_function=himmelblau, alpha = 0.5):
    if objective_function is None:
        raise ValueError("Objective function must be provided.")

    population = [generate_chromosome(min_val, max_val, variables) for _ in range(pop_size)]
    best_solution = None
    best_fitness = float('inf')
    progress = []

    for _ in range(generations):
        sorted_pop = selection(population, method=selection_method, objective_function=objective_function)

        if use_elitism:
            new_population = sorted_pop[:2]
        else:
            new_population = []

        while len(new_population) < pop_size:
            parent1, parent2 = random.sample(sorted_pop[:10], 2)
            child1, child2 = crossover(parent1, parent2, method=crossover_method, alpha=alpha)
            child1 = mutate(child1, method=mutation_method)
            child2 = mutate(child2, method=mutation_method)
            new_population.extend([child1, child2])

        population = new_population[:pop_size]
        # current_best = selection(population)[0]
        current_best = selection(population, method=selection_method, objective_function=objective_function)[0]
        current_fitness = calculate_fitness(current_best, objective_function)
        progress.append(current_fitness)

        if current_fitness < best_fitness:
            best_fitness = current_fitness
            best_solution = current_best
    
    plot_progress(progress)
    save_results_to_csv(progress)

    return best_solution, best_fitness, progress


