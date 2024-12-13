import pygame
import random

# Константы
WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 20

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class GameObject:
    """Базовый класс для всех объектов игры."""
    def __init__(self, position):
        self.position = position

    def draw(self, surface):
        pass

class Apple(GameObject):
    """Класс для яблока."""
    def __init__(self):
        super().__init__(self.randomize_position())
        self.body_color = RED

    def randomize_position(self):
        return (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        pygame.draw.rect(surface, self.body_color, pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

class Snake(GameObject):
    """Класс для змейки."""
    def __init__(self):
        self.length = 1
        self.positions = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (GRID_SIZE, 0)  # Движение вправо
        self.next_direction = None
        self.body_color = GREEN

    def update_direction(self, new_direction):
        """Обновляет направление змейки."""
        if new_direction:
            if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:  # Исключаем движение назад
                self.next_direction = new_direction

    def move(self):
        """Обновляет положение змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        head_x, head_y = self.positions[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # Проверяем на выход за границы и телепортируем змейку
        if new_head[0] < 0:
            new_head = (WIDTH - GRID_SIZE, new_head[1])
        elif new_head[0] >= WIDTH:
            new_head = (0, new_head[1])
        if new_head[1] < 0:
            new_head = (new_head[0], HEIGHT - GRID_SIZE)
        elif new_head[1] >= HEIGHT:
            new_head = (new_head[0], 0)

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        for segment in self.positions:
            pygame.draw.rect(surface, self.body_color, pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        self.length = 1
        self.positions = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (GRID_SIZE, 0)

    def check_collision(self):
        """Проверяет, не столкнулась ли змейка сама с собой."""
        head = self.get_head_position()
        return head in self.positions[1:]

def handle_keys(snake):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction((0, -GRID_SIZE))
            elif event.key == pygame.K_DOWN:
                snake.update_direction((0, GRID_SIZE))
            elif event.key == pygame.K_LEFT:
                snake.update_direction((-GRID_SIZE, 0))
            elif event.key == pygame.K_RIGHT:
                snake.update_direction((GRID_SIZE, 0))
    return True

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    running = True
    while running:
        screen.fill(BLACK)
        running = handle_keys(snake)

        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()

        if snake.check_collision():
            snake.reset()

        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
