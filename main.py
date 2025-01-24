import sys
import pygame
from pathlib import Path

pygame.init()

SCREEN_WIDTH = 1200  # 623
SCREEN_HEIGHT = 400  # 150

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino")  # Add a window title


class Background:
    def __init__(self, x,) -> None:
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.x = x
        self.y = 0
        self.set_texture()
        self.show()

    def update(self, dx,):
        self.x += dx
        if self.x <= -SCREEN_WIDTH:
            self.x = SCREEN_WIDTH

    def show(self,):
        screen.blit(self.texture, (self.x, self.y))

    def set_texture(self,):
        path = Path("assets/images/bg.png")
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))


class Game:
    def __init__(self) -> None:
        self.background = [Background(x=0), Background(x=SCREEN_WIDTH)]
        self.speed = 8


def main():
    game = Game()

    clock = pygame.time.Clock()

    while True:
        for background in game.background:
            background.update(-game.speed)
            background.show()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(100)  # framerate
        # Update the display
        pygame.display.update()

main()
