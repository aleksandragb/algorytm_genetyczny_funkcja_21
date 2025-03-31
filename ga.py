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

#selekcja - wybieranie najlepszych do rozmnażania (które osobniki będą rodzicami):
# elitist: sortujesz i wybierasz najlepszych 
# roulette: losujesz z szansą zależną od fitness (czyli mierzenie jak dobre jest rozwiązanie - wynik funkcji dla danego x i y, żeby wiedzieć które chromosomy są "lepsze", u nas im mniejszy wynik tym lepszy bo szukamy minimum funkcji)
# tournament: kilka osobników walczy, wygrywa najlepszy - losowanie grupek i wybieranie z każdej najlepszego osobnika
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

# Krzyżowanie - łączenie dwóch rodziców, żeby stworzyć dwoje dzieci z ich „genów” (czyli bitów w chromosomie).
# Z wybranych osobników robimy dzieci:
# one_point - tniemy w jednym punkcie i mieszamy końcówki
# two_point - tniemy w dwóch miejscach i mieszamy tylko środek
# uniform - mieszamy losowo bit po bicie - powstają kompletnie inne od rodziców dzieci 
# granular - mieszamy losowo małe grupki bitów (u nas np. po 4 bity na raz)
# none - kopiowanie rodziców bez zmian
# Cel to tworzenie nowych rozwiązań będących połączeniem starych - czasem lepsze (tworzenie dzieci z 2 rodziców)
def crossover(parent1, parent2, method="one_point"):
    if method == "one_point":
        point = random.randint(1, CHROMOSOME_LENGTH - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]

    elif method == "two_point":
        point1 = random.randint(1, CHROMOSOME_LENGTH - 2)
        point2 = random.randint(point1 + 1, CHROMOSOME_LENGTH - 1)
        child1 = (parent1[:point1] + parent2[point1:point2] + parent1[point2:])
        child2 = (parent2[:point1] + parent1[point1:point2] + parent2[point2:])

    elif method == "uniform":
        child1 = ""
        child2 = ""
        for i in range(CHROMOSOME_LENGTH):
            if random.random() < 0.5:
                child1 += parent1[i]
                child2 += parent2[i]
            else:
                child1 += parent2[i]
                child2 += parent1[i]

    elif method == "granular":
        grain_size = 4
        child1 = ""
        child2 = ""
        for i in range(0, CHROMOSOME_LENGTH, grain_size):
            if random.random() < 0.5:
                child1 += parent1[i:i+grain_size]
                child2 += parent2[i:i+grain_size]
            else:
                child1 += parent2[i:i+grain_size]
                child2 += parent1[i:i+grain_size]


    elif method == "none":
        child1 = parent1
        child2 = parent2

    else:
        raise ValueError(f"Unknown crossover method: {method}")

    return child1, child2

# Mutacja - losowe zmiany bitów:
# 3 metody:
# one_point - losowy bit zmienia się
# two_point - dwa bity 
# boundary - pierwszy i ostatni bit 
# Cel to wprowadzenie odrobinę chaosu - czasem taki przypadek daje genialne rozwiązanie
def mutate(chrom, mutation_rate=0.01, method="one_point"):
    chrom_list = list(chrom)

    if method == "none":
        return ''.join(chrom_list)

    if method == "one_point":
        for i in range(len(chrom_list)):
            if random.random() < mutation_rate:
                chrom_list[i] = '1' if chrom_list[i] == '0' else '0'

    elif method == "two_point":
        indices = random.sample(range(len(chrom_list)), 2)
        for i in indices:
            if random.random() < mutation_rate:
                chrom_list[i] = '1' if chrom_list[i] == '0' else '0'

    elif method == "boundary":
        if random.random() < mutation_rate:
            chrom_list[0] = '1' if chrom_list[0] == '0' else '0'
        if random.random() < mutation_rate:
            chrom_list[-1] = '1' if chrom_list[-1] == '0' else '0'

    else:
        raise ValueError(f"Unknown mutation method: {method}")

    return ''.join(chrom_list)


# inwersja - odwracanie fragmentu chromosomu:
# Dodatkowa operacja, która obraca wybrany fragment DNA
# Cel to, aby jeszcze bardziej mieszać kombinacje - to może pomóc wydostać się z "lokalnego minimum"
def inversion(chrom):
    chrom_list = list(chrom)
    start = random.randint(0, len(chrom_list) - 2)
    end = random.randint(start + 1, len(chrom_list) - 1)
    chrom_list[start:end + 1] = chrom_list[start:end + 1][::-1]
    return ''.join(chrom_list)


def run_algorithm(pop_size, generations, variables=None, selection_method="elitist", crossover_method="one_point", mutation_method="one_point", use_inversion=False, use_elitism=True ):
    population = [generate_chromosome() for _ in range(pop_size)]
    best_solution = None
    best_fitness = float('inf')
    progress = []

    for _ in range(generations):
        # selekcja: wybieramy osobniki, które będą rodzicami, sortujemy całą populację od najlepszego do najgorszego
        sorted_pop = selection(population, method=selection_method)
        # strategia elitarna: zabieramy najlepszych 2 osobników z poprzedniego pokolenia i przenosimy ich bez zmian, czyli ci byli najlepsi - niech żyją dalej, nie ryzykujemy ich mutacją
        # new_population = sorted_pop[:2]  # elitarna strategia Zabieramy 2 najlepsze osobniki i wkładamy je do nowej populacji bez zmian. To zapewnia, że najlepsze rozwiązania nie zginą w losowości.
        if use_elitism:
            new_population = sorted_pop[:2]
        else:
            new_population = []


        while len(new_population) < pop_size:
            parent1, parent2 = random.sample(sorted_pop[:10], 2)
            child1, child2 = crossover(parent1, parent2, method=crossover_method)
            child1 = mutate(child1, method=mutation_method)
            child2 = mutate(child2, method=mutation_method)

            if use_inversion:
                child1 = inversion(child1)
                child2 = inversion(child2)

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

