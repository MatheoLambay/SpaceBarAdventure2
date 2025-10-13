import pygame

class items(pygame.sprite.Sprite):
    def __init__(self,name):
        super().__init__()
        self.name = name

    