
import pygame

class Badguy(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.image.load("assets\pnj\ennemis\south.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-30, -20)
        self.life = 3

    def update(self,keys, obstacles, game_map):
        if self.life <= 0:
            self.kill()