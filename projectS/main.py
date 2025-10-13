import pygame
import os
from utility.menu_manager import menuManager
from classes.menus.main_menu import mainMenu


pygame.init()
# pygame.mouse.set_visible(False) 
# pygame.event.set_grab(True)
pygame.font.init()
clock = pygame.time.Clock()
menu_manager = menuManager()
menu_manager.push_menu(mainMenu(menu_manager.screen))

running = True
while running:
    dt = clock.tick(60)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_menu = menu_manager.get_current_menu()
    if current_menu:
        current_menu.update(keys,menu_manager,dt)

    pygame.display.flip()