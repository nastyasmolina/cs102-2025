"""
Графический интерфейс для игры "Жизнь" (Conway's Game of Life) на pygame.
Реализовано:
- отрисовка клеток
- сетка
- пауза/возобновление игры
- редактирование клеток на паузе
"""

import pygame
from pygame.locals import K_ESCAPE, K_SPACE, KEYDOWN, MOUSEBUTTONDOWN, QUIT, K_r

from life import GameOfLife
from ui import UI


class GUI(UI):
    """Графический интерфейс игры «Жизнь» с pygame."""

    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        """
        Инициализация графического интерфейса.
        """
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed

        self.width = life.cols * cell_size
        self.height = life.rows * cell_size

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game of Life")

        self.paused = False
        self.running = True

    def draw_lines(self) -> None:
        """Нарисовать линии сетки."""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(
                self.screen,
                pygame.Color("black"),
                (x, 0),
                (x, self.height),
                1,
            )
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(
                self.screen,
                pygame.Color("black"),
                (0, y),
                (self.width, y),
                1,
            )

    def draw_grid(self) -> None:
        """Нарисовать текущее состояние клеток."""
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                color = (
                    pygame.Color("green")
                    if self.life.curr_generation[row][col] == 1
                    else pygame.Color("white")
                )
                rect = pygame.Rect(
                    col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(self.screen, color, rect)

    def handle_events(self) -> None:
        """Обработка событий."""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False

            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.paused = not self.paused
                elif event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_r:
                    self.life.curr_generation = self.life.create_grid(randomize=True)
                    self.life.generations = 1

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    col = mouse_x // self.cell_size
                    row = mouse_y // self.cell_size
                    if 0 <= row < self.life.rows and 0 <= col < self.life.cols:
                        self.life.curr_generation[row][col] ^= 1

    def run(self) -> None:
        """Запустить игру."""
        clock = pygame.time.Clock()

        while self.running:
            self.handle_events()

            self.screen.fill(pygame.Color("white"))
            self.draw_grid()
            self.draw_lines()

            font = pygame.font.SysFont(None, 24)
            status_text = f"Поколение: {self.life.generations}"
            if self.life.max_generations != float("inf"):
                status_text += f" / {self.life.max_generations}"

            status_text += f" | {'ПАУЗА' if self.paused else 'ИГРА'}"
            text_surface = font.render(status_text, True, pygame.Color("black"))
            self.screen.blit(text_surface, (10, 10))

            if self.paused:
                info_text = "ПРОБЕЛ - продолжить | ЛКМ - изменить клетку | R - перезапуск | ESC - выход"
                info_surface = font.render(info_text, True, pygame.Color("darkred"))
                self.screen.blit(info_surface, (10, self.height - 30))

            if not self.paused:
                if self.life.is_max_generations_exceeded:
                    self.paused = True
                    continue

                if not self.life.is_changing:
                    self.paused = True
                    continue

                self.life.step()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()


if __name__ == "__main__":
    game = GameOfLife(size=(40, 60), randomize=True, max_generations=1000)
    gui = GUI(game, cell_size=15, speed=10)
    gui.run()
