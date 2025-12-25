import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        screen.border(0)

    def draw_grid(self, screen) -> None:
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                symbol = str(int(bool(self.life.curr_generation[row][col])))
                try:
                    screen.addch(row + 1, col + 1, symbol)
                except Exception as e:
                    print(e)

    def run(self) -> None:
        screen = curses.initscr()
        try:
            while self.life.is_changing and not self.life.is_max_generations_exceeded:
                self.draw_borders(screen)
                self.draw_grid(screen)
                screen.getch()
                self.life.step()
        finally:
            curses.endwin()


if __name__ == "__main__":
    c = Console(GameOfLife((24, 80), True, 80))
    c.run()
