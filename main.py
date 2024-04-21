import pygame

from config import SCREEN, BG_IMAGE, FPS
from game import Game
from pipe import Pipe
from plot import plot, init_plot

if __name__ == '__main__':
    pygame.init()
    game = Game()
    clock = pygame.time.Clock()
    plot_scores = []
    init_plot()

    while True:
        SCREEN.blit(source=BG_IMAGE, dest=(0, 0))
        game.remove_off_screen_pipes()
        next_pipe = game.get_next_pipe()

        if game.frames_since_last_pipe >= game.frame_interval:
            game.pipes.append(Pipe())
            game.frames_since_last_pipe = 0

        for pipe in game.pipes:
            pipe.update()
            if not pipe.passed and any(bird.alive for bird in game.population.birds):
                if all(bird.x > pipe.x + pipe.width for bird in game.population.birds if bird.alive):
                    pipe.passed = True
                    game.score += 1

        if not game.population.extinct:
            game.population.update_birds(next_pipe)
        else:
            plot_scores.append(game.score)
            plot(plot_scores)
            game.generation += 1
            game.score = 0
            game.population.evolve()
            game.reset_pipes()

        game.frames_since_last_pipe += 1

        game.update_score()
        game.update_alive_count()
        game.update_gen_counter()
        pygame.display.update()
        clock.tick(FPS)
