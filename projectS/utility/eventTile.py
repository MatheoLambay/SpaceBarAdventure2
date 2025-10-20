import pygame

class eventTile(pygame.sprite.Sprite):
    def __init__(self,tile,new_map):
        super().__init__()
        self.tile = tile
        self.new_map = new_map
       
    def update(self,current_tile):
        if current_tile == self.tile:
            return self.new_map
        return False
        
           