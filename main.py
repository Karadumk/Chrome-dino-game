import random
import sys
import pygame
import math
from pathlib import Path

pygame.init()

SCREEN_WIDTH = 623
SCREEN_HEIGHT = 150

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino")  # Add a window title


class Dino:
    def __init__(self) -> None:
        self.width = 44
        self.height = 44
        self.x = 10
        self.y = 80
        self.texture_num = 0
        self.dy = 3
        self.gravity = 1.2
        self.onground = True
        self.jumping = False
        self.jump_stop = 10
        self.falling = False
        self.fall_stop = self.y
        self.set_texture()
        self.show()

    def update(self, loops):
        # jumping
        if self.jumping:
            self.y -= self.dy
            if self.y <= self.jump_stop:
                self.fall()
        # falling
        elif self.falling:
            self.y += self.gravity * self.dy
            if self.y >= self.fall_stop:
                self.stop()
        # walking
        elif self.onground and loops % 4 == 0:  # adding delay to the method
            self.texture_num = (self.texture_num + 1) % 3
            self.set_texture()

    def show(
        self,
    ):
        screen.blit(self.texture, (self.x, self.y))

    def set_texture(
        self,
    ):
        path = Path(f"assets/images/dino{self.texture_num}.png")
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

    # these methods controls booleans not responsible for physics
    def jump(self):
        self.jumping = True
        self.onground = False

    def fall(self):
        self.jumping = False
        self.falling = True

    def stop(self):
        self.falling = False
        self.onground = True


class Background:
    def __init__(
        self,
        x,
    ) -> None:
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.x = x
        self.y = 0
        self.set_texture()
        self.show()

    def update(
        self,
        dx,
    ):
        self.x += dx
        if self.x <= -SCREEN_WIDTH:
            self.x = SCREEN_WIDTH

    def show(
        self,
    ):
        screen.blit(self.texture, (self.x, self.y))

    def set_texture(
        self,
    ):
        path = Path("assets/images/bg.png")
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))


class Cactus:
    def __init__(self, x) -> None:
        self.width = 34
        self.height = 44
        self.x = x
        self.y = 80
        self.set_texture()
        self.show()

    def update(self, dx):
        self.x += dx

    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    def set_texture(self):
        path = Path("assets/images/cactus.png")
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))


class Collision:
    def between(self, dino, object):
        distance = math.sqrt((dino.x - object.x) ** 2 + (dino.y - object.y) ** 2)
        return distance < 35
    
    
class Game:
    def __init__(self) -> None:
        self.background = [Background(x=0), Background(x=SCREEN_WIDTH)]
        self.dino = Dino()
        self.obstacles = []
        self.collision = Collision()
        self.speed = 6
        self.playing = False
        
    def start(self):
        self.playing = True

    def over(self):
        self.playing = False

    def tospawn(self, loops):  # responsible for time to spawn cactus
        return loops % 80 == 0

    def spawn_cactus(self):
        # list with cactus objects
        if len(self.obstacles) > 0:
            last_cactus = self.obstacles[-1]
            # Make sure to always spawn ahead of the screen
            min_gap = 200
            max_gap = 400
            x = max(last_cactus.x, SCREEN_WIDTH) + random.randint(min_gap, max_gap)
        else:
            x = SCREEN_WIDTH + random.randint(100, 400)

        # create new cactus object
        cactus = Cactus(x)
        self.obstacles.append(cactus)


def main():

    # objects
    game = Game()
    dino = game.dino

    clock = pygame.time.Clock()

    loops = 0

    # main loop
    while True:
        
        if game.playing:
            loops += 1

            # for background
            for background in game.background:
                background.update(-game.speed)
                background.show()

            # for dino
            dino.update(loops)
            dino.show()

            # for cactus
            if game.tospawn(loops):
                game.spawn_cactus()

            for cactus in game.obstacles:
                cactus.update(-game.speed)
                cactus.show()
                
                # collision
                if game.collision.between(dino, cactus):
                    game.over()
        
            # cleanup
            game.obstacles = [c for c in game.obstacles if c.x + c.width > 0]

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if dino.onground:
                        dino.jump()
                        
                    if not game.playing:
                        game.start()

        clock.tick(80)  # framerate
        # Update the display
        pygame.display.update()


main()
