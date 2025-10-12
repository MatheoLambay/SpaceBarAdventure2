import pygame

class PNJ(pygame.sprite.Sprite):
    def __init__(self, frames, tile_pos, tile_size,talk):
        """
        frames : liste d'images pour l'animation
        tile_pos : (colonne, ligne) sur la matrice
        tile_size : taille d'une tuile en pixels
        """
        super().__init__()
      
        self.image = pygame.image.load(frames).convert_alpha()
        self.interaction_img = pygame.image.load("assets/pnj/interaction.png").convert_alpha()

        self.talk=talk
        # position en pixels centrée sur la tuile
        col, row = tile_pos
        x = col * tile_size + tile_size // 2
        y = row * tile_size + tile_size // 2
        self.rect = self.image.get_rect(center=(x, y))


        self.animation_speed = 0.15

    def update(self,player,screen,camera,keys):
        if self.rect.colliderect(player.hitbox):
            if keys[pygame.K_RETURN]:
                print("PNJ :" + self.talk)
        
            #affiche le bouton d'interaction sur le pnj
            interaction_rect = self.interaction_img.get_rect(topright=self.rect.topright)
            screen.blit(self.interaction_img, camera.apply(interaction_rect))