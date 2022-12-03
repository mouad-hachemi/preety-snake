# Simple snake game made with Pygame library.
import sys, pygame, random

# Colors
WHITE = (255, 255, 255)
GRAY = pygame.Color("#cad2c5")
WARM_BLUE = pygame.Color("#1e6091")
OCEAN_GREAN = pygame.Color("#52B69A")

# Screen Dimensions.
WIDTH = 992
HEIGHT = 480

# Framerate.
FPS = 8

# GRID Params.
GRID_SIZE = 32
NUM_OF_GRIDS_X = 30
NUM_OF_GRIDS_Y = 14

BOUNDARIES = {
    "LeftX": GRID_SIZE,
    "RightX": WIDTH - GRID_SIZE,
    "TopY": GRID_SIZE,
    "BottomY": HEIGHT - GRID_SIZE,
}

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
        self.rect.x = random.randrange(
            BOUNDARIES["LeftX"] + GRID_SIZE * 2,
            BOUNDARIES["RightX"] - GRID_SIZE * 2,
            GRID_SIZE,
        )
        self.rect.y = random.randrange(
            BOUNDARIES["TopY"] + GRID_SIZE * 2,
            BOUNDARIES["BottomY"] - GRID_SIZE * 2,
            GRID_SIZE,
        )
        self.vel = (0, 0)

    def update(self):
        self.rect.x += self.vel[0] * GRID_SIZE  # The Xth value of vel.
        self.rect.y += self.vel[1] * GRID_SIZE  # The Yth value of vel.


class Fruit(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(OCEAN_GREAN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(
            BOUNDARIES["LeftX"], BOUNDARIES["RightX"] - GRID_SIZE, GRID_SIZE
        )
        self.rect.y = random.randrange(
            BOUNDARIES["TopY"], BOUNDARIES["BottomY"] - GRID_SIZE, GRID_SIZE
        )


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pretty Snake!")

all_sprites = pygame.sprite.Group()

snake = Snake()
fruit = Fruit()

all_sprites.add(fruit)
all_sprites.add(snake)


def quit_game():
    pygame.quit()
    sys.exit()


def draw_grid():
    for i in range(1, NUM_OF_GRIDS_X + 1):
        pygame.draw.line(
            screen,
            GRAY,
            (i * GRID_SIZE, BOUNDARIES["TopY"]),
            (i * GRID_SIZE, BOUNDARIES["BottomY"]),
        )
    for j in range(1, NUM_OF_GRIDS_Y + 1):
        pygame.draw.line(
            screen,
            GRAY,
            (BOUNDARIES["LeftX"], j * GRID_SIZE),
            (BOUNDARIES["RightX"], j * GRID_SIZE),
        )


def is_out(player):
    if player.x < BOUNDARIES["LeftX"] or player.x >= BOUNDARIES["RightX"]:
        return True
    elif player.y < BOUNDARIES["TopY"] or player.y >= BOUNDARIES["BottomY"]:
        return True
    return False


def main():
    while True:
        clock.tick(FPS)
        # Process Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                snake.vel = {
                    pygame.K_UP: (0, -1),
                    pygame.K_RIGHT: (1, 0),
                    pygame.K_DOWN: (0, 1),
                    pygame.K_LEFT: (-1, 0),
                }.get(event.key, (0, 0))

        # Update
        all_sprites.update()
        if is_out(snake.rect):
            quit_game()
        # Draw
        screen.fill(WHITE)
        draw_grid()
        all_sprites.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
