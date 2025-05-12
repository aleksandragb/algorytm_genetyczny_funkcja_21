import numpy as np

def random_mutation(offspring, ga_instance):
    for idx in range(offspring.shape[0]):
        gene = np.random.randint(0, offspring.shape[1])
        offspring[idx, gene] = 1 - offspring[idx, gene]
    return offspring

def swap_mutation(offspring, ga_instance):
    for idx in range(offspring.shape[0]):
        gene1, gene2 = np.random.choice(offspring.shape[1], size=2, replace=False)
        offspring[idx, gene1], offspring[idx, gene2] = offspring[idx, gene2], offspring[idx, gene1]
    return offspring

def gauss_mutation(offspring, ga_instance):
    for idx in range(offspring.shape[0]):
        gene = np.random.randint(0, offspring.shape[1])
        offspring[idx, gene] += np.random.normal(0, 0.1)
    return offspring