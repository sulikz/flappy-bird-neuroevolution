import random

from config import *


class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.width = PIPE_WIDTH
        self.speed = PIPE_SPEED
        self.top_pos = 0
        self.bot_pos = 0
        self.center_of_gap = 0
        self.top_img = TOP_IMAGE
        self.bot_img = BOT_IMAGE
        self.top_mask = TOP_MASK
        self.bot_mask = BOT_MASK
        self.gap = GAP
        self.set_height()
        self.passed = False

    def set_height(self) -> None:
        top_height = random.randint(*TOP_PIPE_HEIGHT_RANGE)
        self.top_pos = top_height - self.top_img.get_height()
        self.bot_pos = top_height + self.gap
        self.center_of_gap = (top_height + self.bot_pos) / 2

    def update(self) -> None:
        self.x -= self.speed
        SCREEN.blit(self.top_img, (self.x, self.top_pos))
        SCREEN.blit(self.bot_img, (self.x, self.bot_pos))
