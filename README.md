# Genetic Algorithm for Financial Pattern Detection

## Project Overview
This project implements a genetic algorithm to detect 2-day chart patterns in financial data. It predicts future stock movements based on historical data from the S&P 500. The algorithm utilizes various genetic operations such as selection, crossover, and mutation to evolve a population of candidate solutions (chromosomes).

## How to Run
To execute the program, use the following command in the terminal:
python "Genetics-Algorithm.py" --population 100 --generations 50 --mutation 0.01 --crossover uniform --selection elitist --data "genAlgData1.txt"

### Command Line Arguments
- `--population`: Set the initial population size (default: 100).
- `--generations`: Set the number of generations to run (default: 50).
- `--mutation`: Set the mutation rate (default: 0.01).
- `--crossover`: Choose the crossover type: `uniform` or `1-point` (default: `uniform`).
- `--selection`: Choose the selection method: `elitist` or `tournament` (default: `elitist`).
- `--data`: Specify the data file to use (default: `genAlgData1.txt`).

## Data Format
The input data files (`genAlgData1.txt` and `genAlgData2.txt`) should be structured as follows:
- Each line contains three values:
  1. Percentage price change from day 1 to day 2.
  2. Percentage price change from day 2 to day 3.
  3. Profit or loss in dollars for a one-day hold.

## Genetic Algorithm Details
- **Chromosome Encoding**: Each chromosome consists of 5 genes:
  - The first two genes represent the first day's price change range.
  - The next two genes represent the second day's price change range.
  - The last gene indicates a buy (1) or short (0) recommendation.
  
- **Fitness Function**: The fitness of each chromosome is calculated based on its performance against the historical data, measuring the total profit/loss if the recommendations were followed.

- **Selection Methods**: The algorithm supports both elitist selection (preserving the best chromosomes) and tournament selection (randomly selecting winners).

- **Crossover Methods**: The algorithm implements both uniform crossover (mixing genes from two parents) and 1-point crossover (taking segments from each parent).

## Output
After every 10 generations, the program outputs the maximum, minimum, and average fitness of the population. At the end of the execution, the best chromosome and its fitness
