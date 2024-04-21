import pygame

# COLORS
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# NN
INPUT_SIZE = 3  # excluding bias node
POPULATION_SIZE = 20
TOURNAMENT_SELECTION_SIZE = 5
ELITISM_SIZE = 2
ACTION_DECISION_THRESHOLD = 0.7
MUTATION_RATE = 0.4
INITIAL_MUTATION_STRENGTH = 0.4
MIN_MUTATION_STRENGTH = 0.05

# GAME
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FPS = 120
FONT_SIZE = 50

# PIPE
PIPE_SPEED = 10
PIPE_WIDTH = 80
PIPE_FRAME_INTERVAL = 70
TOP_PIPE_HEIGHT_RANGE = (150, 450)
GAP = 100

# BIRB
GRAVITY = 0.4
JUMP_FORCE = 8
ACTION_JUMP = 1
ACTION_NO_JUMP = 0
JUMP_COOLDOWN = 15

# IMAGES
BG_IMAGE = pygame.image.load("images/background.png")
BG_IMAGE = pygame.transform.scale(BG_IMAGE, (BG_IMAGE.get_width(), SCREEN_HEIGHT))
BIRD_IMAGE = pygame.transform.scale_by(pygame.image.load("images/bird.png"), 1.2)
BIRD_MASK = pygame.mask.from_surface(BIRD_IMAGE)
PIPE_IMAGE = pygame.image.load("images/pipe.png")
PIPE_IMAGE = pygame.transform.scale_by(PIPE_IMAGE, 1)
BOT_IMAGE = pygame.transform.scale(PIPE_IMAGE, (PIPE_WIDTH, 2*PIPE_IMAGE.get_height()))
TOP_IMAGE = pygame.transform.flip(BOT_IMAGE, False, True)
TOP_MASK = pygame.mask.from_surface(TOP_IMAGE)
BOT_MASK = pygame.mask.from_surface(BOT_IMAGE)
