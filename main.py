# Simple snake game made with Pygame library.
import sys, pygame, random

# Colors
WHITE = (255, 255, 255)
GRAY = pygame.Color("#cad2c5")
HEAD_COLOR = pygame.Color("#168AAD")
BODY_COLOR = pygame.Color("#34A0A4")
FRUIT_COLOR = pygame.Color("#76C893")
OCEAN_GREAN = pygame.Color("#52B69A")

# Screen Dimensions.
WIDTH = 992
HEIGHT = 480

# Framerate.
FPS = 8

# GRID Params.
GRID_SIZE = 32
NUM_OF_GRIDS_X = 31
NUM_OF_GRIDS_Y = 15

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


def spawn_head():
    x = random.randrange(
        BOUNDARIES["LeftX"] + GRID_SIZE * 2,
        BOUNDARIES["RightX"] - GRID_SIZE * 2,
        GRID_SIZE,
    )
    y = random.randrange(
        BOUNDARIES["TopY"] + GRID_SIZE * 2,
        BOUNDARIES["BottomY"] - GRID_SIZE * 2,
        GRID_SIZE,
    )
    return x, y


def spawn_fruit():
    x = random.randrange(
        BOUNDARIES["LeftX"], BOUNDARIES["RightX"] - GRID_SIZE, GRID_SIZE
    )
    y = random.randrange(
        BOUNDARIES["TopY"], BOUNDARIES["BottomY"] - GRID_SIZE, GRID_SIZE
    )
    return x, y


def quit_game():
    pygame.quit()
    sys.exit()


def draw_grid():
    for i in range(1, NUM_OF_GRIDS_X):
        pygame.draw.line(
            screen,
            GRAY,
            (i * GRID_SIZE, BOUNDARIES["TopY"]),
            (i * GRID_SIZE, BOUNDARIES["BottomY"]),
        )
    for j in range(1, NUM_OF_GRIDS_Y):
        pygame.draw.line(
            screen,
            GRAY,
            (BOUNDARIES["LeftX"], j * GRID_SIZE),
            (BOUNDARIES["RightX"], j * GRID_SIZE),
        )


def is_out(head):
    head_coor = head.rect
    if head_coor.x < BOUNDARIES["LeftX"] or head_coor.x >= BOUNDARIES["RightX"]:
        return True
    elif head_coor.y < BOUNDARIES["TopY"] or head_coor.y >= BOUNDARIES["BottomY"]:
        return True
    return False


class Snake:
    def __init__(self):
        super().__init__()
        self.body = []
        self.head = None
        self.vel = (0, 0)

    def draw(self, surface):
        for i, block in enumerate(self.body):
            if i == 0:
                block.image.fill(HEAD_COLOR)
            else:
                block.image.fill(BODY_COLOR)
            surface.blit(block.image, block.rect)

    def add_block(self, block):
        self.head = block
        self.body = [block] + self.body

    def update(self):
        x, y = self.head.rect.topleft
        x += self.vel[0] * GRID_SIZE  # The Xth value of vel.
        y += self.vel[1] * GRID_SIZE  # The Yth value of vel.
        new_head = Block((x, y))
        self.add_block(new_head)
        self.body.pop()
        self.eat()

    def eat(self):
        if self.head.rect == fruit.rect:
            x, y = fruit.rect.topleft
            x += self.vel[0] * GRID_SIZE
            y += self.vel[1] * GRID_SIZE
            block = Block((x, y))
            self.add_block(block)


class Block:
    def __init__(self, cor):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = cor[0]
        self.rect.y = cor[1]


class Fruit:
    def __init__(self, cor):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(FRUIT_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = cor[0]
        self.rect.y = cor[1]

    def draw(self, surface):
        surface.blit(self.image, self.rect)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pretty Snake!")

snake = Snake()

head = Block(spawn_head())
fruit = Fruit(spawn_fruit())

snake.add_block(head)


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
        snake.update()
        if is_out(snake.head):
            quit_game()
        # Draw
        screen.fill(WHITE)
        draw_grid()
        fruit.draw(screen)
        snake.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
