import pygame

class menuManager:
    def __init__(self):
        self.current_menu = []
        self.screen = pygame.display.set_mode((800,600))
        

    def push_menu(self, menu):
        """Ajouter un nouveau menu au fil d'Ariane."""
        if self.current_menu:
            self.current_menu[-1].close()
        self.current_menu.append(menu)
        menu.open(self.screen)

    def pop_menu(self):
        """Retourner au menu précédent."""
        if len(self.current_menu) != 1:
            self.current_menu.pop().close()
            self.current_menu[-1].open(self.screen)

    def go_home(self):
        """Revenir au menu principal."""
        while len(self.current_menu) > 2:
            self.current_menu.pop().close()
        self.current_menu[-1].open(self.screen)

    def get_current_menu(self):
        """Obtenir le menu actuel."""
        return self.current_menu[-1] if self.current_menu else None