import numpy as np

def tournament_selection(pop_fitness, num_parents):
    return np.random.choice(len(pop_fitness), size=num_parents)

def roulette_selection(pop_fitness, num_parents):
    total_fitness = np.sum(pop_fitness)
    probs = pop_fitness / total_fitness
    return np.random.choice(len(pop_fitness), size=num_parents, p=probs)

def random_selection(pop_fitness, num_parents):
    return np.random.choice(len(pop_fitness), size=num_parents)
