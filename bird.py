import random

from config import *
from network import Network
from pipe import Pipe


class Bird:
    def __init__(self):
        self.x = 30
        self.y = SCREEN_HEIGHT // 2
        self.image = BIRD_IMAGE
        self.mask = BIRD_MASK
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.center_y = 0  # Used for visualisation / feeding the model
        self.alive = True
        self.jump_cooldown = JUMP_COOLDOWN
        self.jump_cooldown_counter = 0
        self.movement = 0
        self.lifespan = 0
        self.next_pipe = None
        self.decision = None
        self.fitness = 0
        self.net = Network()
        self.vision_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    @classmethod
    def clone_bird(cls, bird: "Bird"):
        cloned_bird = Bird()
        cloned_bird.fitness = bird.fitness
        cloned_bird.net = Network.clone_network(bird.net)
        return cloned_bird

    def update(self, next_pipe: Pipe):
        if self.alive:
            self.think()
            self.move()
            self.draw()
            self.center_y = self.y + self.height / 2
            self.jump_cooldown_counter -= 1
            if next_pipe:
                self.next_pipe = next_pipe
                self.draw_model_vision()
                self.check_collision()
            self.fitness += 1

    def draw(self) -> None:
        SCREEN.blit(self.image, (self.x, self.y))

    def move(self) -> None:
        self.movement += GRAVITY
        self.y += self.movement

    def jump(self) -> None:
        if self.jump_cooldown_counter <= 0:
            self.movement = -JUMP_FORCE
            self.jump_cooldown_counter = self.jump_cooldown

    def check_collision(self) -> None:
        top_offset = (self.next_pipe.x - self.x, self.next_pipe.top_pos - self.y)
        collision_top = self.mask.overlap(self.next_pipe.top_mask, top_offset)
        bottom_offset = (self.next_pipe.x - self.x, self.next_pipe.bot_pos - self.y)
        collision_bottom = self.mask.overlap(self.next_pipe.bot_mask, bottom_offset)
        out_of_bounds = self.y > SCREEN_HEIGHT - self.height or self.y < 0
        self.alive = not (collision_top or collision_bottom or out_of_bounds)

    def draw_model_vision(self) -> None:
        pygame.draw.line(SCREEN, self.vision_color, (self.x + self.width, self.center_y),
                         (self.next_pipe.x, self.next_pipe.center_of_gap), 2)
        pygame.draw.line(SCREEN, self.vision_color, (self.x + self.width, self.center_y),
                         (self.next_pipe.x, self.center_y), 2)

    def think(self):
        inputs = [
            (self.y / SCREEN_HEIGHT) * 2 - 1,
            (self.next_pipe.x / SCREEN_WIDTH) * 2 - 1 if self.next_pipe else 0,
            (self.next_pipe.center_of_gap / SCREEN_HEIGHT) * 2 - 1 if self.next_pipe else 0
        ]
        self.decision = self.net.feed_forward(inputs)
        if self.decision > ACTION_DECISION_THRESHOLD:
            self.jump()

    def clone(self):
        cloned_bird = Bird()
        cloned_bird.fitness = self.fitness
        cloned_bird.net = Network.clone_network(self.net)
        return cloned_bird
