# Simple snake game made with Pygame library.
import sys, pygame, random
from pygame.math import Vector2

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
        2,
        NUM_OF_GRIDS_X - 2,
    )
    y = random.randrange(
        2,
        NUM_OF_GRIDS_Y - 2,
    )
    return Vector2(x, y)


def spawn_fruit():
    x = random.randrange(1, NUM_OF_GRIDS_X - 1)
    y = random.randrange(1, NUM_OF_GRIDS_Y - 1)
    return Vector2(x, y)


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
    if head.x < 1 or head.x >= NUM_OF_GRIDS_X - 1:
        return True
    elif head.y < 1 or head.y >= NUM_OF_GRIDS_Y - 1:
        return True
    return False


class Snake:
    def __init__(self):
        super().__init__()
        self.body = [spawn_head()]
        self.head = self.body[0]
        self.vel = Vector2(0, 0)
        self.new_block = False

    def draw(self, surface):
        for i, block in enumerate(self.body):
            image = pygame.Surface((GRID_SIZE, GRID_SIZE))
            rect = image.get_rect()
            rect.x = block.x * GRID_SIZE
            rect.y = block.y * GRID_SIZE
            if i == 0:
                image.fill(HEAD_COLOR)
            else:
                image.fill(BODY_COLOR)
            surface.blit(image, rect)

    def move_body(self):
        new_head = self.head + self.vel
        self.head = new_head
        self.body = [new_head] + self.body
        self.body.pop()

    def update(self):
        self.check_collision()
        # The attribute new_block to avoid moving the snake double time after eating.
        # (Actually it's not moving it double time it's like escaping a draw call).
        if not self.new_block:
            self.move_body()
        else:
            self.eat()

    def eat(self):
        new_head = fruit.pos + self.vel
        self.body = [new_head] + self.body
        self.head = self.body[0]
        self.new_block = False

    def check_collision(self):
        if self.head == fruit.pos:
            self.new_block = True

class Fruit:
    def __init__(self, cor):
        super().__init__()
        self.pos = cor
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(FRUIT_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = cor.x * GRID_SIZE
        self.rect.y = cor.y * GRID_SIZE

    def draw(self, surface):
        surface.blit(self.image, self.rect)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pretty Snake!")

snake = Snake()

fruit = Fruit(spawn_fruit())


def main():
    while True:
        # Process Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                snake.vel = {
                    pygame.K_UP: Vector2(0, -1),
                    pygame.K_RIGHT: Vector2(1, 0),
                    pygame.K_DOWN: Vector2(0, 1),
                    pygame.K_LEFT: Vector2(-1, 0),
                }.get(event.key, Vector2(0, 0))

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
        clock.tick(FPS)


if __name__ == "__main__":
    main()
