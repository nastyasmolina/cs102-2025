"""
Графический интерфейс для игры "Жизнь" (Conway's Game of Life) на pygame.
Реализовано:
- отрисовка клеток
- сетка
- пауза/возобновление игры
- редактирование клеток на паузе
"""

"""
Графический интерфейс для игры "Жизнь" (Conway's Game of Life) на pygame.
Реализовано:
- отрисовка клеток
- сетка
- пауза/возновление игры
- редактирование клеток на паузе
"""

import pygame
from pygame.locals import (
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    MOUSEBUTTONDOWN,
    QUIT,
    K_r,
)

from life import GameOfLife
from ui import UI


class GUI(UI):
    """Графический интерфейс игры «Жизнь» с pygame."""

    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
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
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (x, 0), (x, self.height)
            )
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (0, y), (self.width, y)
            )

    def draw_grid(self) -> None:
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                color = (
                    pygame.Color("green")
                    if self.life.curr_generation[row][col]
                    else pygame.Color("white")
                )
                pygame.draw.rect(
                    self.screen,
                    color,
                    (
                        col * self.cell_size,
                        row * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    ),
                )

    def handle_events(self) -> None:
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
                    self.life.generations = 0
            elif event.type == MOUSEBUTTONDOWN and self.paused and event.button == 1:
                x, y = event.pos
                col = x // self.cell_size
                row = y // self.cell_size
                if 0 <= row < self.life.rows and 0 <= col < self.life.cols:
                    self.life.curr_generation[row][col] ^= 1

    def run(self) -> None:
        clock = pygame.time.Clock()

        while self.running:
            self.handle_events()

            self.screen.fill(pygame.Color("white"))
            self.draw_grid()
            self.draw_lines()

            font = pygame.font.SysFont(None, 30)
            text = font.render(
                f"Поколение: {self.life.generations} | {'ПАУЗА' if self.paused else 'ИГРА'}",
                True,
                pygame.Color("black"),
            )
            self.screen.blit(text, (10, 10))

            if self.paused:
                hint = font.render(
                    "ПРОБЕЛ - играть | ЛКМ - редактировать | R - рестарт | ESC - выход",
                    True,
                    pygame.Color("darkred"),
                )
                self.screen.blit(hint, (10, self.height - 40))

            if not self.paused:
                self.life.step()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()


if __name__ == "__main__":
    game = GameOfLife((40, 60), randomize=True, max_generations=1000)
    gui = GUI(game, cell_size=15, speed=10)
    gui.run()
