"""
Прототип игры "Жизнь" (Conway's Game of Life) на pygame.

Демонстрирует:
- создание сетки клеток
- генерацию нового поколения
- отрисовку клеток и сетки
"""

import random
import typing as tp

import pygame
from pygame.locals import QUIT

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    """Прототип графической игры 'Жизнь' с базовой сеткой и логикой поколений."""

    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.speed = speed

        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        self.grid: Grid = self.create_grid(randomize=True)

    def create_grid(self, randomize: bool = False) -> Grid:
        """Создание сетки клеток (1 — живая, 0 — мёртвая)."""
        grid = [[0 for _ in range(self.cell_width)] for _ in range(self.cell_height)]
        if randomize:
            for i in range(self.cell_height):
                for j in range(self.cell_width):
                    grid[i][j] = random.randint(0, 1)
        return grid

    def draw_lines(self) -> None:
        """Отрисовать сетку."""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (x, 0), (x, self.height)
            )
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (0, y), (self.width, y)
            )

    def draw_grid(self) -> None:
        """Отрисовать клетки."""
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                color = pygame.Color("green") if cell else pygame.Color("white")
                rect = pygame.Rect(
                    j * self.cell_size,
                    i * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(self.screen, color, rect)

    def get_neighbours(self, cell: Cell) -> Cells:
        """Вернуть список значений соседних клеток для клетки (i, j)."""
        row, col = cell
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                new_row, new_col = row + i, col + j
                if 0 <= new_row < self.cell_height and 0 <= new_col < self.cell_width:
                    neighbours.append(self.grid[new_row][new_col])
        return neighbours

    def get_next_generation(self) -> Grid:
        """Вычислить следующее поколение клеток."""
        new_grid = self.create_grid(randomize=False)
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                alive_neighbours = sum(self.get_neighbours((i, j)))
                if self.grid[i][j] == 1:
                    new_grid[i][j] = 1 if alive_neighbours in (2, 3) else 0
                else:
                    new_grid[i][j] = 1 if alive_neighbours == 3 else 0
        return new_grid

    def run(self) -> None:
        """Запустить прототип игры."""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life Prototype")
        self.screen.fill(pygame.Color("white"))

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.screen.fill(pygame.Color("white"))
            self.draw_grid()
            self.draw_lines()

            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()
        print("Прототип игры завершён.")


if __name__ == "__main__":
    game = GameOfLife(width=400, height=300, cell_size=10, speed=5)
    game.run()
