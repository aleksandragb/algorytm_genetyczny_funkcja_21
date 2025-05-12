from crossover import custom_crossover

# Parametry algorytmu genetycznego
num_generations = 60
sol_per_pop = 80
num_parents_mating = 50
num_genes = 60
init_range_low = 0
init_range_high = 2
gene_type = int

# Ustawienia mutacji
mutation_percent_genes = 10
random_mutation_max_val = 1
random_mutation_min_val = 0

# Metody selekcji, krzyżowania i mutacji
parent_selection_methods = ["tournament", "rws", "random"]
crossover_methods = ["single_point", "two_points", "uniform", custom_crossover]
mutation_methods = ["random", "swap", "gauss"]
keep_elitism = 1
K_tournament = 3
parallel_processing = ['thread', 4]