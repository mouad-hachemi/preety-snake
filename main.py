# Simple snake game made with Pygame library.
import sys, pygame, random
from pygame.math import Vector2
from os import path

# Paths
fonts_dir = path.join(path.dirname(__file__), "fonts")
sounds_dir = path.join(path.dirname(__file__), "sounds")

# Colors
WHITE = (255, 255, 255)
GRAY = pygame.Color("#cad2c5")
DARK_GRAY = pygame.Color("#4C4E52")
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


def draw_go_text(surface):
    text = font48.render("You Loose! Press Space to play again.", False, DARK_GRAY)
    text_rect = text.get_rect()
    text_rect.centerx = WIDTH // 2
    text_rect.centery = HEIGHT // 2
    surface.blit(text, text_rect)
    pygame.display.flip()


def draw_score(surface, text):
    text = font.render(text, False, DARK_GRAY)
    text_rect = text.get_rect()
    text_rect.x = 8
    text_rect.y = 8
    surface.blit(text, text_rect)


class Snake:
    def __init__(self):
        super().__init__()
        self.body = [self.spawn_head()]
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

    def spawn_head(self):
        x = random.randrange(
            2,
            NUM_OF_GRIDS_X - 2,
        )
        y = random.randrange(
            2,
            NUM_OF_GRIDS_Y - 2,
        )
        return Vector2(x, y)

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
        eat_sfx.play()
        new_head = fruit.pos + self.vel
        self.body = [new_head] + self.body
        self.head = self.body[0]
        self.new_block = False
        fruit.spawn_fruit()

    def check_collision(self):
        if self.head == fruit.pos:
            self.new_block = True

    def check_fail(self):
        if self.head in self.body[1:]:
            return True
        if self.head.x < 1 or self.head.x >= NUM_OF_GRIDS_X - 1:
            return True
        elif self.head.y < 1 or self.head.y >= NUM_OF_GRIDS_Y - 1:
            return True
        return False

    def reset(self):
        self.body = [self.spawn_head()]
        self.head = self.body[0]
        self.vel = Vector2(0, 0)
        self.new_block = False


class Fruit:
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(FRUIT_COLOR)
        self.rect = self.image.get_rect()
        self.spawn_fruit()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def spawn_fruit(self):
        x = random.randrange(1, NUM_OF_GRIDS_X - 1)
        y = random.randrange(1, NUM_OF_GRIDS_Y - 1)
        self.pos = Vector2(x, y)
        while self.pos in snake.body:
            x = random.randrange(1, NUM_OF_GRIDS_X - 1)
            y = random.randrange(1, NUM_OF_GRIDS_Y - 1)
            self.pos = Vector2(x, y)
        self.rect.x = self.pos.x * GRID_SIZE
        self.rect.y = self.pos.y * GRID_SIZE


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pretty Snake!")

# Loading fonts.
font = pygame.font.Font(path.join(fonts_dir, "KenneyHighSquare.ttf"), 22)
font48 = pygame.font.Font(path.join(fonts_dir, "KenneyHighSquare.ttf"), 48)

# Loading sounds.
death_sfx = pygame.mixer.Sound(path.join(sounds_dir, 'death_sfx.wav'))
eat_sfx = pygame.mixer.Sound(path.join(sounds_dir, 'eat_sfx.wav'))

snake = Snake()

fruit = Fruit()


def main():
    game_over = False
    while True:
        clock.tick(FPS)
        # Process Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                snake.vel = {
                    pygame.K_UP: Vector2(0, -1)
                    if snake.vel != Vector2(0, 1)
                    else snake.vel,
                    pygame.K_RIGHT: Vector2(1, 0)
                    if snake.vel != Vector2(-1, 0)
                    else snake.vel,
                    pygame.K_DOWN: Vector2(0, 1)
                    if snake.vel != Vector2(0, -1)
                    else snake.vel,
                    pygame.K_LEFT: Vector2(-1, 0)
                    if snake.vel != Vector2(1, 0)
                    else snake.vel,
                }.get(event.key, Vector2(0, 0))
                break
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    game_over = False
        if game_over:
            draw_go_text(screen)
            continue
        # Update
        snake.update()
        if snake.check_fail():
            death_sfx.play()
            snake.reset()
            game_over = True
            continue
        # Draw
        screen.fill(WHITE)
        draw_grid()
        fruit.draw(screen)
        snake.draw(screen)
        draw_score(screen, f"Score: {str(len(snake.body) - 1)}")
        pygame.display.flip()


if __name__ == "__main__":
    main()
