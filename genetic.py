import numpy as np
import random
from network import INIT_SCALE


class GeneticAlgorithm:
    def __init__(self, population_size=300, mutation_rate=0.15, mutation_strength=0.5, elitism=15):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.mutation_strength = mutation_strength
        self.elitism = elitism
        self.generation = 0

    def next_generation(self, agents):
        """agents need: .fitness, .brain, and optionally .score, .frames_alive"""
        agents.sort(key=lambda a: a.fitness, reverse=True)
        self.generation += 1

        best = agents[0]
        print(f"Gen {self.generation} | Best Score: {getattr(best, 'score', 0):.0f} "
              f"| Best Time: {getattr(best, 'frames_alive', 0)} frames "
              f"| Best fitness: {best.fitness:.1f} "
              f"| Avg fitness: {np.mean([a.fitness for a in agents]):.1f}")

        # 1. Elitism
        elite_n = min(self.elitism, len(agents), self.population_size)
        next_weights = [agents[i].brain.get_weights().copy() for i in range(elite_n)]

        # 2. Breed 90% of population
        target_len = int(self.population_size * 0.9)
        while len(next_weights) < target_len:
            p1 = self.tournament(agents)
            p2 = self.tournament(agents)
            c1, c2 = self.crossover(p1.brain.get_weights(), p2.brain.get_weights())
            next_weights.append(self.mutate(c1))
            if len(next_weights) < target_len:
                next_weights.append(self.mutate(c2))

        # 3. Random immigrants, same scale as network init
        genome_len = len(next_weights[0])
        while len(next_weights) < self.population_size:
            next_weights.append(INIT_SCALE * np.random.randn(genome_len))

        return next_weights

    def tournament(self, agents, k=10):
        k = min(k, len(agents))
        return max(random.sample(agents, k), key=lambda a: a.fitness)

    def crossover(self, w1, w2):
        mask = np.random.rand(len(w1)) < 0.5
        return np.where(mask, w1, w2), np.where(mask, w2, w1)

    def mutate(self, weights):
        w = weights.copy()
        mask = np.random.rand(len(w)) < self.mutation_rate
        w[mask] += np.random.normal(0, self.mutation_strength, mask.sum())
        return np.clip(w, -5, 5)