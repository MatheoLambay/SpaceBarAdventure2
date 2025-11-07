import pygame

class decoObj:
    def __init__(self,path,pos,tile_size,has_hitbox=False):
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (pos[0]*tile_size,pos[1]*tile_size))
        self.has_hitbox = has_hitbox
    