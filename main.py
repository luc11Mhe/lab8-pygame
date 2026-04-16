import pygame
import random
import math

pygame.init()
MIN_SIZE = 10
MAX_SIZE = 50
MAX_SPEED = 200

WIDTH, HEIGHT = 1080, 920
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Squares")

clock = pygame.time.Clock()


class Square:
    def __init__(self):
        self.reset()

    def reset(self):
        self.size = random.randint(MIN_SIZE, MAX_SIZE)
        speed_fact = (MAX_SIZE - self.size) / (MAX_SIZE - MIN_SIZE + 1)
        self.max_speed = max(1, int(MAX_SPEED * speed_fact))

        self.x = random.randint(0, WIDTH - self.size)
        self.y = random.randint(0, HEIGHT - self.size)

        self.dx = random.choice([-1, 1]) * random.uniform(50, self.max_speed)
        self.dy = random.choice([-1, 1]) * random.uniform(50, self.max_speed)

        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )

        self.life = random.uniform(5, 15)

    def move(self, dt):
        if random.random() < 0.2:
            angle = random.uniform(-0.2, 0.2)
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)

            new_dx = self.dx * cos_a - self.dy * sin_a
            new_dy = self.dx * sin_a + self.dy * cos_a

            self.dx = new_dx
            self.dy = new_dy

        speed = math.sqrt(self.dx**2 + self.dy**2)
        if speed > 0:
            factor = min(self.max_speed, speed) / speed
            self.dx *= factor
            self.dy *= factor

        self.x += self.dx * dt
        self.y += self.dy * dt

        if self.x < 0:
            self.x = 0
            self.dx *= -1
        elif self.x > WIDTH - self.size:
            self.x = WIDTH - self.size
            self.dx *= -1

        if self.y < 0:
            self.y = 0
            self.dy *= -1
        elif self.y > HEIGHT - self.size:
            self.y = HEIGHT - self.size
            self.dy *= -1

    def flee(self, all_squares, dt):
        for other in all_squares:
            if other is self:
                continue

            if other.size > self.size:
                dx = self.x - other.x
                dy = self.y - other.y
                dist = math.hypot(dx, dy)

                if dist < 200 and dist > 0:
                    dx /= dist
                    dy /= dist

                    self.dx += dx * 0.5 * dt
                    self.dy += dy * 0.5 * dt

    def update_life(self, dt):
        self.life -= dt
        if self.life <= 0:
            self.reset()

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))


squares = []
for i in range(15):
    squares.append(Square())


running = True
while running:
    dt = clock.tick(72) / 1000

    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for square in squares:
        square.flee(squares, dt)

    for square in squares:
        square.move(dt)
        square.update_life(dt)

    for square in squares:
        square.draw(screen)

    pygame.display.flip()

pygame.quit()
