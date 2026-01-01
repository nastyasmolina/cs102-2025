"""
Графический интерфейс для игры "Жизнь" (Conway's Game of Life) на pygame.
Реализовано:
- отрисовка клеток
- сетка
- пауза/возобновление игры
- редактирование клеток на паузе
"""

import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.paused = False

        self.width = self.life.cols * cell_size
        self.height = self.life.rows * cell_size

        self.screen = pygame.display.set_mode((self.width, self.height))

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
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                color = (
                    pygame.Color("green")
                    if self.life.curr_generation[i][j] == 1
                    else pygame.Color("white")
                )

                pygame.draw.rect(
                    self.screen,
                    color,
                    (
                        j * self.cell_size,
                        i * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    ),
                )

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")

        paused = False

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        paused = not paused
                elif event.type == MOUSEBUTTONDOWN and paused:
                    mx, my = pygame.mouse.get_pos()
                    x = mx // self.cell_size
                    y = my // self.cell_size
                    self.life.curr_generation[y][x] ^= 1

            self.screen.fill(pygame.Color("white"))
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()

            if not paused:
                self.life.step()

            pygame.time.Clock().tick(self.speed)

    def toggle_cell(self, pos) -> None:
        x, y = pos
        col = x // self.cell_size
        row = y // self.cell_size

        if 0 <= row < self.life.rows and 0 <= col < self.life.cols:
            self.life.curr_generation[row][col] ^= 1


if __name__ == "__main__":
    game = GameOfLife(size=(50, 50), randomize=True)
    gui = GUI(life=game, cell_size=20, speed=10)
    gui.run()
