import pygame


class eventTile(pygame.sprite.Sprite):
    def __init__(self,tile,new_map):
        super().__init__()
        self.tile = tile
        self.is_started = 0
        self.new_map = new_map

    
            

    def update(self,current_tile,map):
        if current_tile == self.tile and not self.is_started:
            self.is_started = 1
            map.new_map_data(self.new_map)
           