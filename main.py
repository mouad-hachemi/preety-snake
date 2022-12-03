# Simple snake game made with Pygame library.
import pygame

# Colors
WHITE = (255, 255, 255)
GRAY = pygame.Color('#cad2c5')

# Screen Dimensions.
WIDTH = 992
HEIGHT = 480

# Framerate.
FPS = 30

# GRID Params.
GRID_SIZE = 32
NUM_OF_GRIDS_X = 30
NUM_OF_GRIDS_Y = 14

# Initializing pygame, and creating game window.
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pretty Snake!')

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

        # Update
        # Draw
        screen.fill(WHITE)
        draw_grid()
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    main()

