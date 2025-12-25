import pygame
from pygame import SurfaceType, Surface
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.width = self.life.cols * cell_size
        self.height = self.life.rows * cell_size
        self.paused = False

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for row in range(self.life.rows):
            for column in range(self.life.cols):
                rect = pygame.Rect(column * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)

                color_name = "green" if self.life.curr_generation[row][column] else "white"
                color = pygame.Color(color_name)

                pygame.draw.rect(self.screen, color, rect)

    def run(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.paused = not self.paused
                if event.type == QUIT:
                    running = False
            if self.life.is_changing and not self.life.is_max_generations_exceeded and not self.paused:
                self.life.step()
            self.screen.fill(pygame.Color("white"))
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()


if __name__ == "__main__":
    game = GameOfLife((24, 80), True, 80)
    gui = GUI(game)
    gui.run()
