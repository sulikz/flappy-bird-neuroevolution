import random
from typing import List

from bird import Bird
from config import TOURNAMENT_SELECTION_SIZE, ELITISM_SIZE
from network import Network
from pipe import Pipe


class Population:
    def __init__(self, size: int):
        self.generation = 1
        self.species = []
        self.size = size
        self.birds = [Bird() for _ in range(self.size)]

    def update_birds(self, next_pipe: Pipe) -> None:
        for bird in self.birds:
            bird.update(next_pipe)

    @property
    def extinct(self) -> bool:
        return all(not bird.alive for bird in self.birds)

    def selection(self) -> List[Bird]:
        best_bird = max(self.birds, key=lambda bird: bird.fitness)
        new_generation = [Bird.clone_bird(best_bird) for _ in range(ELITISM_SIZE)]
        while len(new_generation) < self.size:
            tournament = random.sample(self.birds, TOURNAMENT_SELECTION_SIZE)
            winner = max(tournament, key=lambda bird: bird.fitness)
            cloned_net = Network.clone_network(winner.net)
            cloned_bird = Bird.clone_bird(winner)
            cloned_bird.net = cloned_net
            new_generation.append(cloned_bird)
        return new_generation

    def evolve(self) -> None:
        selected_birds = self.selection()
        new_generation = []
        if len(selected_birds) % 2 != 0:
            selected_birds.append(selected_birds[random.randint(0, len(selected_birds) - 1)])
        random.shuffle(selected_birds)
        for i in range(0, len(selected_birds), 2):
            bird1 = selected_birds[i]
            bird2 = selected_birds[i + 1]
            offspring1 = Population.crossbreed(bird1, bird2)
            offspring2 = Population.crossbreed(bird2, bird1)
            new_generation.extend([offspring1, offspring2])
        new_generation = new_generation[:self.size]
        for bird in new_generation:
            bird.net.mutate(self.generation)
        self.birds = new_generation

    @staticmethod
    def crossbreed(bird1: Bird, bird2: Bird) -> Bird:
        offspring = Bird.clone_bird(bird1)
        for idx, conn in enumerate(offspring.net.connections):
            parent_choice = random.choice([bird1.net.connections[idx], bird2.net.connections[idx]])
            conn.weight = parent_choice.weight
        return offspring
