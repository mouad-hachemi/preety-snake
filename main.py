# Simple snake game made with Pygame library.
import pygame
import random

# Colors
WHITE = (255, 255, 255)
GRAY = pygame.Color('#cad2c5')
WARM_BLUE = pygame.Color('#1e6091')

# Screen Dimensions.
WIDTH = 992
HEIGHT = 480

# Framerate.
FPS = 8

# GRID Params.
GRID_SIZE = 32
NUM_OF_GRIDS_X = 30
NUM_OF_GRIDS_Y = 14

# Initializing pygame, and creating game window.
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(WARM_BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(GRID_SIZE, WIDTH - 3 * GRID_SIZE, GRID_SIZE)
        self.rect.y = random.randrange(GRID_SIZE, HEIGHT - 3 * GRID_SIZE, GRID_SIZE)
        self.vel = (0, 0)
    
    def update(self):
        self.rect.x += self.vel[0] * GRID_SIZE # The Xth value of vel.
        self.rect.y += self.vel[1] * GRID_SIZE # The Yth value of vel.

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pretty Snake!')

all_sprites = pygame.sprite.Group()

snake = Snake()

all_sprites.add(snake)

def draw_grid():
    for i in range(1, NUM_OF_GRIDS_X + 1):
            pygame.draw.line(screen, GRAY, (i * GRID_SIZE, GRID_SIZE), (i * GRID_SIZE, HEIGHT - GRID_SIZE))
    for j in range(1, NUM_OF_GRIDS_Y + 1):
        pygame.draw.line(screen, GRAY, (GRID_SIZE, j * GRID_SIZE), (WIDTH - GRID_SIZE, j * GRID_SIZE))

def main():
    running = True
    while running:
        clock.tick(FPS)
        # Process Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                snake.vel = {
                    pygame.K_UP: (0, -1),
                    pygame.K_RIGHT: (1, 0),
                    pygame.K_DOWN: (0, 1),
                    pygame.K_LEFT: (-1, 0)
                }.get(event.key, (0, 0))

        # Update
        all_sprites.update()
        # Draw
        screen.fill(WHITE)
        draw_grid()
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    main()

