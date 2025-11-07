

import pygame

class LookAtEvent:
    def __init__(self, player,direction):
        self.player = player
        self.direction = direction


    def update(self,dt):
        self.player.image = self.player.frames[self.direction][0]
        return True

        
