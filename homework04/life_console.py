def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

def draw_borders(self, screen) -> None:
    """Отобразить рамку."""
    rows, cols = self.life.rows, self.life.cols
    for col_number in range(1, cols - 1):
        screen.addstr(0, col_number, "-")
        screen.addstr(rows - 1, col_number, "-")
    for row_number in range(1, rows - 1):
        screen.addstr(row_number, 0, "|")
        screen.addstr(row_number, cols - 1, "|")
def draw_grid(self, screen) -> None:
    """Отобразить состояние клеток."""
    screen.clear()
    height, width = screen.getmaxyx()
    for i, row in enumerate(self.life.curr_generation):
        if i >= height - 1:
            break
        for j, cell in enumerate(row):
            if j >= width - 1:
                break
            screen.addch(i, j, "1" if cell else " ")
    screen.refresh()
def run(self) -> None:
    """
        Запуск консольной версии игры «Жизнь».
        Управление:
        - клавиша 'q' — выход из игры
        """
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    screen.nodelay(True)

    try:
        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            """
                Основной игровой цикл.
                Игра автоматически обновляет поколения клеток,
                пока состояние поля изменяется и не достигнут
                максимум поколений.
                """
            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)

            key = screen.getch()
            if key == ord("q"):
                """
                Завершение игры по нажатию клавиши 'q'.
                позволяет выйти из программы без закрытия терминала.
                """
                break

            self.life.step()
            curses.napms(150)

    finally:
        curses.nocbreak()
        curses.echo()
        curses.endwin()


if __name__ == "__main__":
    game = GameOfLife(size=(10, 40), randomize=True)
    ui = Console(game)
    ui.run()
    