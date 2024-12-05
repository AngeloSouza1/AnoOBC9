import pygame
import random
import sys

# Configurações iniciais
WIDTH, HEIGHT = 800, 600
FPS = 60

# Configuração de cores
COLORS = [
    (165, 104, 246),
    (230, 61, 135),
    (0, 199, 228),
    (253, 214, 126)
]

SHAPES = ['circle', 'square', 'triangle', 'line']

class Particle:
    def __init__(self, x, y, size, color, shape, speed, direction, rotation=False):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.shape = shape
        self.speed = speed
        self.direction = direction
        self.rotation = rotation
        self.angle = random.uniform(0, 360)  # Apenas para rotação

    def update(self):
        self.y += self.speed * self.direction
        if self.rotation:
            self.angle += self.speed / 10  # Atualiza ângulo para rotação

    def draw(self, screen):
        if self.shape == 'circle':
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))
        elif self.shape == 'square':
            rect = pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)
            pygame.draw.rect(screen, self.color, rect)
        elif self.shape == 'triangle':
            points = [
                (self.x, self.y - self.size),
                (self.x - self.size // 2, self.y + self.size // 2),
                (self.x + self.size // 2, self.y + self.size // 2)
            ]
            pygame.draw.polygon(screen, self.color, points)
        elif self.shape == 'line':
            start_pos = (self.x, self.y)
            end_pos = (self.x, self.y + self.size * 3)
            pygame.draw.line(screen, self.color, start_pos, end_pos, int(self.size / 2))

def particle_factory(max_particles, width, height):
    particles = []
    for _ in range(max_particles):
        x = random.randint(0, width)
        y = random.randint(-height, 0)
        size = random.randint(3, 8)
        color = random.choice(COLORS)
        shape = random.choice(SHAPES)
        speed = random.uniform(2, 5)
        direction = 1  # Sentido de queda
        particles.append(Particle(x, y, size, color, shape, speed, direction))
    return particles

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Confetti Effect")
    clock = pygame.time.Clock()

    max_particles = 100
    particles = particle_factory(max_particles, WIDTH, HEIGHT)

    running = True
    while running:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Atualiza e desenha as partículas
        for particle in particles:
            particle.update()
            particle.draw(screen)
            # Reinicia partículas fora da tela
            if particle.y > HEIGHT:
                particle.y = random.randint(-HEIGHT, 0)
                particle.x = random.randint(0, WIDTH)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
