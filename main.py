import pygame
import random
import math
from typing import List, Optional, Tuple

pygame.init()

MIN_SIZE: int = 10
MAX_SIZE: int = 50
MAX_SPEED: int = 120

WIDTH: int = 1080
HEIGHT: int = 920

screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Squares")

clock: pygame.time.Clock = pygame.time.Clock()


class Square:
    def __init__(self) -> None:
        self.reset()

    def move(self, dt: float) -> None:

        if random.random() < 0.02:
            angle: float = random.uniform(-0.2, 0.2)
            cos_a: float = math.cos(angle)
            sin_a: float = math.sin(angle)

            new_dx: float = self.dx * cos_a - self.dy * sin_a
            new_dy: float = self.dx * sin_a + self.dy * cos_a

            self.dx, self.dy = new_dx, new_dy

        speed: float = math.hypot(self.dx, self.dy)
        if speed > 0:
            factor: float = min(self.max_speed, speed) / speed
            self.dx *= factor
            self.dy *= factor

        self.x += self.dx * dt
        self.y += self.dy * dt

        # Bouncing walls
        # if self.x < 0:
        #   self.x = 0
        #  self.dx *= -1
        # elif self.x > WIDTH - self.size:
        #   self.x = WIDTH - self.size
        #   self.dx *= -1

        # if self.y < 0:
        #   self.y = 0
        #  self.dy *= -1
        # elif self.y > HEIGHT - self.size:
        #   self.y = HEIGHT - self.size
        #  self.dy *= -1

        # wrap horizontally
        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0

        # wrap vertically
        if self.y < 0:
            self.y = HEIGHT
        elif self.y > HEIGHT:
            self.y = 0

    def check_collision(self, other: "Square") -> bool:
        rect1 = pygame.Rect(self.x, self.y, self.size, self.size)
        rect2 = pygame.Rect(other.x, other.y, other.size, other.size)
        return rect1.colliderect(rect2)

    def eat(self, all_squares: List["Square"]) -> None:
        for other in all_squares:
            if other is self:
                continue

            if self.size > other.size and self.check_collision(other):
                other.reset()

    def flee(self, all_squares: List["Square"], dt: float) -> None:
        for other in all_squares:
            if other is self:
                continue

            if other.size > self.size:
                dx: float = (self.x + self.size / 2) - (other.x + other.size / 2)
                dy: float = (self.y + self.size / 2) - (other.y + other.size / 2)
                dist: float = math.hypot(dx, dy)

                if 0 < dist < 200:
                    dx /= dist
                    dy /= dist

                    strength: float = (200 - dist) / 200
                    self.dx += dx * 500 * strength * dt
                    self.dy += dy * 500 * strength * dt

    def chasing(self, all_squares: List["Square"], dt: float) -> None:
        closest: Optional[Tuple[float, float, float]] = None
        closest_dist: float = float("inf")

        for other in all_squares:
            if other is self or other.size >= self.size:
                continue

            dx: float = (other.x + other.size / 2) - (self.x + self.size / 2)
            dy: float = (other.y + other.size / 2) - (self.y + self.size / 2)
            dist: float = math.hypot(dx, dy)

            if dist < closest_dist:
                closest_dist = dist
                closest = (dx, dy, dist)

        if closest and 0 < closest_dist < 200:
            dx, dy, dist = closest

            dx /= dist
            dy /= dist

            strength: float = (200 - dist) / 200
            self.dx += dx * 600 * strength * dt
            self.dy += dy * 600 * strength * dt

    def update_life(self, dt: float) -> None:
        self.life -= dt
        if self.life <= 0:
            self.reset()

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))

    def reset(self) -> None:
        self.size: int = random.randint(MIN_SIZE, MAX_SIZE)

        speed_fact: float = (MAX_SIZE - self.size) / (MAX_SIZE - MIN_SIZE + 1)
        self.max_speed: float = max(1.0, MAX_SPEED * speed_fact)

        self.x: float = float(random.randint(0, WIDTH - self.size))
        self.y: float = float(random.randint(0, HEIGHT - self.size))

        self.dx: float = random.choice([-1, 1]) * random.uniform(50, self.max_speed)
        self.dy: float = random.choice([-1, 1]) * random.uniform(50, self.max_speed)

        self.color: Tuple[int, int, int] = (
            random.randint(10, 255),
            random.randint(10, 255),
            random.randint(10, 255),
        )

        self.life: float = random.uniform(5, 15)


squares: List[Square] = []

# 5 squares with a size of 25
for _ in range(5):
    s = Square()
    s.size = 25
    squares.append(s)

# 10 squares with a size of 10
for _ in range(10):
    s = Square()
    s.size = 10
    squares.append(s)

# 30 squares with a size of 4
for _ in range(30):
    s = Square()
    s.size = 4
    squares.append(s)

running: bool = True
while running:
    dt: float = clock.tick(72) / 1000.0

    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for square in squares:
        square.flee(squares, dt)
        square.eat(squares)

    for square in squares:
        square.chasing(squares, dt)

    for square in squares:
        square.move(dt)
        square.check_collision(square)
        square.update_life(dt)
        square.reset()

    for square in squares:
        square.draw(screen)

    pygame.display.flip()

pygame.quit()
