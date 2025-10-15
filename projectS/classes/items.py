import pygame

class items(pygame.sprite.Sprite):
    def __init__(self,path,pos,tile_size):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(pos[0]*tile_size,pos[1]*tile_size))
        self.last_talk = 0
        self.hitbox = self.rect.inflate(-20,-10)
        
        # self.hitbox = pygame.Rect(pos[0]*tile_size+20,pos[1]*tile_size+tile_size,tile_size-40,tile_size)

        self.interaction_img = pygame.image.load("assets/pnj/interaction.png").convert_alpha()

    def update(self,screen,player,keys,camera):
        if self.rect.colliderect(player.hitbox):
            interaction_rect = self.interaction_img.get_rect(topright=self.hitbox.topright)
            screen.blit(self.interaction_img, camera.apply(interaction_rect))
            if keys[pygame.K_RETURN] and self.last_talk == 0:
                player.control_enabled = False
                self.in_talk = 1

            elif not keys[pygame.K_RETURN] and self.last_talk == 1:
                self.last_talk = 0

    