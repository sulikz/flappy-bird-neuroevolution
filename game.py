from typing import Optional, List

from config import *
from pipe import Pipe
from population import Population


class Game:
    def __init__(self):
        self.font = pygame.font.SysFont('arial', FONT_SIZE)
        self.population = Population(POPULATION_SIZE)
        self.frame_interval = PIPE_FRAME_INTERVAL
        self.frames_since_last_pipe = self.frame_interval
        self.pipes: List[Pipe] = []
        self.generation = 0
        self.score = 0

    def get_next_pipe(self) -> Optional[Pipe]:
        if len(self.pipes) > 0:
            for pipe in self.pipes:
                if pipe.x + pipe.width > self.population.birds[0].x:
                    return pipe
        return None

    def remove_off_screen_pipes(self):
        self.pipes = [pipe for pipe in self.pipes if pipe.x > - pipe.width]

    def reset_pipes(self) -> None:
        self.frames_since_last_pipe = self.frame_interval
        self.pipes = []

    def update_gen_counter(self) -> None:
        counter_surface = self.font.render(f"generation: {self.generation}", True, BLACK)
        counter_rect = counter_surface.get_rect(topleft=(10, 0))
        SCREEN.blit(counter_surface, counter_rect)

    def update_score(self) -> None:
        score_surface = self.font.render(f"score: {self.score}", True, BLACK)
        score_rect = score_surface.get_rect(topleft=(10, 50))
        SCREEN.blit(score_surface, score_rect)

    def update_alive_count(self) -> None:
        alive_count = sum(bird.alive for bird in self.population.birds)
        alive_count_surface = self.font.render(f"alive: {alive_count}", True, BLACK)
        alive_count_rect = alive_count_surface.get_rect(topleft=(10, 100))  # Adjust position as needed
        SCREEN.blit(alive_count_surface, alive_count_rect)
