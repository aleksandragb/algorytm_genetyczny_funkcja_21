import numpy as np

def single_point_crossover(parents, offspring_size, ga_instance):
    offspring = []
    for k in range(offspring_size[0]):
        parent1 = parents[k % parents.shape[0]].copy()
        parent2 = parents[(k + 1) % parents.shape[0]].copy()
        crossover_point = np.random.randint(1, offspring_size[1])
        offspring.append(np.concatenate((parent1[:crossover_point], parent2[crossover_point:])))
    return np.array(offspring)

def two_points_crossover(parents, offspring_size, ga_instance):
    offspring = []
    for k in range(offspring_size[0]):
        parent1 = parents[k % parents.shape[0]].copy()
        parent2 = parents[(k + 1) % parents.shape[0]].copy()
        point1 = np.random.randint(1, offspring_size[1] // 2)
        point2 = np.random.randint(offspring_size[1] // 2, offspring_size[1])
        child = np.concatenate((parent1[:point1], parent2[point1:point2], parent1[point2:]))
        offspring.append(child)
    return np.array(offspring)

def uniform_crossover(parents, offspring_size, ga_instance):
    offspring = []
    for k in range(offspring_size[0]):
        parent1 = parents[k % parents.shape[0]].copy()
        parent2 = parents[(k + 1) % parents.shape[0]].copy()
        mask = np.random.randint(0, 2, offspring_size[1])
        child = np.where(mask, parent1, parent2)
        offspring.append(child)
    return np.array(offspring)

def custom_crossover(parents, offspring_size, ga_instance):
    offspring = []
    idx = 0
    while len(offspring) != offspring_size[0]:
        parent1 = parents[idx % parents.shape[0]].copy()
        parent2 = parents[(idx + 1) % parents.shape[0]].copy()
        random_split_point = np.random.choice(range(offspring_size[1]))
        parent1[random_split_point:] = parent2[random_split_point:]
        offspring.append(parent1)
        idx += 1
    return np.array(offspring)