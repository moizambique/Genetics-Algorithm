import numpy as np
import random
import argparse

# Constants
MUTATION_RATE = 0.01
INITIAL_POPULATION_SIZE = 100
NUM_GENERATIONS = 50
CROSSOVER_TYPE = "uniform"  # or "1-point"
SELECTION_TYPE = "elitist"  # or "tournament"
DATA_FILE = "genAlgData1.txt"  # Default data file

# Chromosome structure
class Chromosome:
    def __init__(self):
        self.genes = [0] * 5
        self.fitness = 0

    def randomize(self):
        while True:
            self.genes[0], self.genes[1] = np.random.normal(0, 1.15, 2)
            self.genes[2], self.genes[3] = np.random.normal(0, 1.15, 2)
            if self.genes[0] < self.genes[1] and self.genes[2] < self.genes[3]:
                break
        self.genes[4] = random.randint(0, 1)

def read_data(file_name):
    data = np.loadtxt(file_name)
    return data

def calculate_fitness(chromosome, data):
    total_profit = 0
    matches = 0

    for change in data:
        if chromosome.genes[0] <= change[0] < chromosome.genes[1] and \
           chromosome.genes[2] <= change[1] < chromosome.genes[3]:
            matches += 1
            if chromosome.genes[4] == 1:  # BUY
                total_profit += change[2]
            else:  # SHORT
                total_profit -= change[2]

    if matches == 0:
        return -5000  # Penalize if no matches
    return total_profit

def initialize_population(size):
    return [Chromosome() for _ in range(size)]

def elitist_selection(population, num_select):
    population.sort(key=lambda x: x.fitness, reverse=True)
    return population[:num_select]

def tournament_selection(population, num_select):
    selected = []
    for _ in range(num_select):
        competitors = random.sample(population, 2)
        winner = max(competitors, key=lambda x: x.fitness)
        selected.append(winner)
    return selected

def uniform_crossover(parent1, parent2):
    child = Chromosome()
    for i in range(5):
        child.genes[i] = parent1.genes[i] if random.random() < 0.5 else parent2.genes[i]
    # Ensure validity
    if child.genes[0] > child.genes[1]:
        child.genes[0], child.genes[1] = child.genes[1], child.genes[0]
    if child.genes[2] > child.genes[3]:
        child.genes[2], child.genes[3] = child.genes[3], child.genes[2]
    return child

def one_point_crossover(parent1, parent2):
    child = Chromosome()
    child.genes[0:2] = parent1.genes[0:2]
    child.genes[2:5] = parent2.genes[2:5]
    return child

def mutate(chromosome):
    for i in range(4):
        if random.random() < MUTATION_RATE:
            chromosome.genes[i] = np.random.normal(0, 1.15)
    if chromosome.genes[0] > chromosome.genes[1]:
        chromosome.genes[0], chromosome.genes[1] = chromosome.genes[1], chromosome.genes[0]
    if chromosome.genes[2] > chromosome.genes[3]:
        chromosome.genes[2], chromosome.genes[3] = chromosome.genes[3], chromosome.genes[2]
    chromosome.genes[4] = random.randint(0, 1)

def main():
    global MUTATION_RATE, INITIAL_POPULATION_SIZE, NUM_GENERATIONS, CROSSOVER_TYPE, SELECTION_TYPE, DATA_FILE

    parser = argparse.ArgumentParser(description='Genetic Algorithm for Financial Pattern Detection')
    parser.add_argument('--population', type=int, default=INITIAL_POPULATION_SIZE, help='Initial population size')
    parser.add_argument('--generations', type=int, default=NUM_GENERATIONS, help='Number of generations to run')
    parser.add_argument('--mutation', type=float, default=MUTATION_RATE, help='Mutation rate')
    parser.add_argument('--crossover', type=str, default=CROSSOVER_TYPE, help='Crossover type (uniform or 1-point)')
    parser.add_argument('--selection', type=str, default=SELECTION_TYPE, help='Selection type (elitist or tournament)')
    parser.add_argument('--data', type=str, default=DATA_FILE, help='Data file to use')

    args = parser.parse_args()

    MUTATION_RATE = args.mutation
    INITIAL_POPULATION_SIZE = args.population
    NUM_GENERATIONS = args.generations
    CROSSOVER_TYPE = args.crossover
    SELECTION_TYPE = args.selection
    DATA_FILE = args.data

    data = read_data(DATA_FILE)
    population = initialize_population(INITIAL_POPULATION_SIZE)

    for generation in range(NUM_GENERATIONS):
        for chromosome in population:
            chromosome.fitness = calculate_fitness(chromosome, data)

        if generation % 10 == 0:
            max_fit = max(chromosome.fitness for chromosome in population)
            min_fit = min(chromosome.fitness for chromosome in population)
            avg_fit = sum(chromosome.fitness for chromosome in population) / len(population)
            print(f"Generation {generation}: Max Fit: {max_fit}, Min Fit: {min_fit}, Avg Fit: {avg_fit}")

        if SELECTION_TYPE == "elitist":
            selected = elitist_selection(population, int(0.4 * INITIAL_POPULATION_SIZE))
        else:
            selected = tournament_selection(population, int(0.4 * INITIAL_POPULATION_SIZE))

        new_population = selected.copy()

        while len(new_population) < INITIAL_POPULATION_SIZE:
            parent1, parent2 = random.sample(selected, 2)
            if CROSSOVER_TYPE == "uniform":
                child = uniform_crossover(parent1, parent2)
            else:
                child = one_point_crossover(parent1, parent2)
            mutate(child)
            new_population.append(child)

        population = new_population

    # Final fitness evaluation
    for chromosome in population:
        chromosome.fitness = calculate_fitness(chromosome, data)

    best_chromosome = max(population, key=lambda x: x.fitness)
    print("Best Chromosome:", best_chromosome.genes, "Fitness:", best_chromosome.fitness)

if __name__ == "__main__":
    main()
