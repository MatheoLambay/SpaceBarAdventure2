import pygame
from utility.button import Button
from classes.game_manager import game_manager

class mainMenu:
    def __init__(self,screen):
        self.screen = screen
        self.image = pygame.image.load("assets\pnj\interaction.png").convert_alpha()
        # self.rect = self.image.get_rect(center=(400,300))
        self.btn = Button(screen,400,300,self.image)

    def open(self,screen):
        pass

    def close(self):
        pass

    def update(self,keys,menu_manager,dt):
        self.screen.fill((255,255,255))
        self.btn.draw()
        if self.btn.detect():
            menu_manager.push_menu(game_manager(self.screen))
        