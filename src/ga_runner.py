import pygad
from config import *
from fitness import fitness_func, decode_solution
from crossover import single_point_crossover, two_points_crossover, uniform_crossover, custom_crossover
from mutation import random_mutation, swap_mutation, gauss_mutation
from results import plot_results, print_results
import numpy as np
import logging

def get_logger(name='results.log', level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    file_handler = logging.FileHandler(name)
    file_handler.setLevel(level)
    logger.addHandler(file_handler)
    return logger

def run_tests():
    logger = get_logger()
    fitness_history = []
    for representation in ["binary", "real"]:
        if representation == "real":
            local_gene_type = float
            local_init_range_low = -2.0
            local_init_range_high = 2.0
            local_decode_solution = lambda x: x[:3]
            local_num_genes = 3
        else:
            local_gene_type = int
            local_init_range_low = 0
            local_init_range_high = 2
            local_decode_solution = decode_solution
            local_num_genes = 60

        for sel_method in parent_selection_methods:
            for cross_method in crossover_methods:
                for mut_method in mutation_methods:
                    ga_instance = pygad.GA(
                        num_generations=num_generations,
                        sol_per_pop=sol_per_pop,
                        num_parents_mating=num_parents_mating,
                        num_genes=local_num_genes,
                        fitness_func=lambda ga, sol, idx: fitness_func(ga, sol, idx, local_decode_solution),
                        init_range_low=local_init_range_low,
                        init_range_high=local_init_range_high,
                        gene_type=local_gene_type,
                        parent_selection_type=sel_method,
                        crossover_type=cross_method if isinstance(cross_method, str) else cross_method,
                        mutation_type=mut_method if mut_method != "gauss" else gauss_mutation,
                        mutation_percent_genes=mutation_percent_genes,
                        keep_elitism=keep_elitism,
                        K_tournament=K_tournament,
                        random_mutation_max_val=random_mutation_max_val,
                        random_mutation_min_val=random_mutation_min_val,
                        parallel_processing=parallel_processing
                    )
                    ga_instance.run()
                    solution, fitness, _ = ga_instance.best_solution()
                    logger.info(f"Reprezentacja: {representation}, Selekcja: {sel_method}, Krzyżowanie: {cross_method}, Mutacja: {mut_method}, Fitness: {fitness}")
                    print(f"Reprezentacja: {representation}, Selekcja: {sel_method}, Krzyżowanie: {cross_method}, Mutacja: {mut_method}, Fitness: {fitness}")
                    print_results(solution, fitness)
                    fitness_history.append(ga_instance.best_solutions_fitness)
    plot_results(np.array(fitness_history), np.arange(1, num_generations + 1))