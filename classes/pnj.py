import pygame

class PNJ(pygame.sprite.Sprite):
    def __init__(self, frames, tile_pos, tile_size):
        """
        frames : liste d'images pour l'animation
        tile_pos : (colonne, ligne) sur la matrice
        tile_size : taille d'une tuile en pixels
        """
        super().__init__()
      
        self.image = pygame.image.load(frames).convert_alpha()
        

        # position en pixels centrée sur la tuile
        col, row = tile_pos
        x = col * tile_size + tile_size // 2
        y = row * tile_size + tile_size // 2
        self.rect = self.image.get_rect(center=(x, y))

        self.animation_speed = 0.15

    def update(self,player):
        if self.rect.colliderect(player.hitbox):
            print("Collision avec le PNJ !")