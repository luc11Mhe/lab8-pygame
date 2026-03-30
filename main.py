import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1080, 920
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Squares")

clock = pygame.time.Clock()


class Square:
    def __init__(self):
        self.size = 28
        self.x = random.randint(0, WIDTH - self.size)
        self.y = random.randint(0, HEIGHT - self.size)

        self.dx = random.choice([-3, -2, -1, 1, 2, 3])
        self.dy = random.choice([-3, -2, -1, 1, 2, 3])

        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )

    def move(self):
        self.x += self.dx
        self.y += self.dy

        if self.x <= 0 or self.x >= WIDTH - self.size:
            self.dx *= -1
        if self.y <= 0 or self.y >= HEIGHT - self.size:
            self.dy *= -1

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))


squares = []
for i in range(100):
    squares.append(Square())


running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for square in squares:
        square.move()

    for square in squares:
        square.draw(screen)

    pygame.display.flip()
    clock.tick(72)

pygame.quit()