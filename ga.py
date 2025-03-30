import random
from chromosome import Chromosome
from functions import HimmelblauFunction
from plot import plot_progress
from utils import save_results_to_csv

class GeneticAlgorithm:
    def __init__(self, pop_size, generations, selection="elitist", crossover="one_point", mutation="one_point", use_inversion=False):
        self.pop_size = pop_size
        self.generations = generations
        self.selection_method = selection
        self.crossover_method = crossover
        self.mutation_method = mutation
        self.use_inversion = use_inversion
        self.func = HimmelblauFunction()
        self.population = [Chromosome() for _ in range(pop_size)]
        self.progress = []

    def select(self):
        if self.selection_method == "elitist":
            return sorted(self.population, key=lambda c: c.fitness(self.func))
        elif self.selection_method == "roulette":
            fitnesses = [1 / (c.fitness(self.func) + 1e-6) for c in self.population]
            total = sum(fitnesses)
            probs = [f / total for f in fitnesses]
            return random.choices(self.population, weights=probs, k=len(self.population))
        elif self.selection_method == "tournament":
            return [min(random.sample(self.population, 5), key=lambda c: c.fitness(self.func)) for _ in range(len(self.population))]
        else:
            raise ValueError("Unknown selection method")

    def crossover(self, p1, p2):
        if self.crossover_method == "one_point":
            pt = random.randint(1, Chromosome.LENGTH - 1)
            return Chromosome(p1.genes[:pt] + p2.genes[pt:]), Chromosome(p2.genes[:pt] + p1.genes[pt:])
        elif self.crossover_method == "two_point":
            p1_, p2_ = sorted(random.sample(range(Chromosome.LENGTH), 2))
            return Chromosome(p1.genes[:p1_] + p2.genes[p1_:p2_] + p1.genes[p2_:]), Chromosome(p2.genes[:p1_] + p1.genes[p1_:p2_] + p2.genes[p2_:])
        elif self.crossover_method == "uniform":
            g1, g2 = "", ""
            for a, b in zip(p1.genes, p2.genes):
                if random.random() < 0.5:
                    g1 += a
                    g2 += b
                else:
                    g1 += b
                    g2 += a
            return Chromosome(g1), Chromosome(g2)
        else:
            return p1, p2

    def run(self):
        best = None
        best_fit = float('inf')

        for _ in range(self.generations):
            selected = self.select()
            new_pop = selected[:2]

            while len(new_pop) < self.pop_size:
                parent1, parent2 = random.sample(selected[:10], 2)
                child1, child2 = self.crossover(parent1, parent2)
                child1.mutate(method=self.mutation_method)
                child2.mutate(method=self.mutation_method)

                if self.use_inversion:
                    child1.inversion()
                    child2.inversion()

                new_pop.extend([child1, child2])

            self.population = new_pop[:self.pop_size]
            best_in_gen = min(self.population, key=lambda c: c.fitness(self.func))
            best_fitness = best_in_gen.fitness(self.func)
            self.progress.append(best_fitness)

            if best_fitness < best_fit:
                best = best_in_gen
                best_fit = best_fitness

        x, y = best.decode()
        plot_progress(self.progress)
        save_results_to_csv(self.progress)
        return f"x = {x:.4f}, y = {y:.4f}, f(x,y) = {best_fit:.4f}"
