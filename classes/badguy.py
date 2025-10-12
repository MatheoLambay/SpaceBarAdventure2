import pygame
from utility.Apathfinding import a_star # 

class Badguy(pygame.sprite.Sprite):
    def __init__(self, pos, speed=2):
        super().__init__()
        self.image = pygame.image.load("assets/pnj/ennemis/south.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-30, -20)
        self.life = 3
        self.speed = speed

    def update(self, player_rect, obstacles):
        if self.life <= 0:
            self.kill()
            return

  