import pygame

class healPad(pygame.sprite.Sprite):
    def __init__(self,path,pos,tile_size):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(pos[0]*tile_size,pos[1]*tile_size))
        self.hitbox = self.rect.inflate(-20,-10)
        self.last_time = 0
        self.interval = 800

        

        self.interaction_img = pygame.image.load("assets/pnj/interaction.png").convert_alpha()

    def update(self,screen,player,keys,camera):

        if self.rect.colliderect(player.hitbox):
            interaction_rect = self.interaction_img.get_rect(topright=self.hitbox.topright)
            screen.blit(self.interaction_img, camera.apply(interaction_rect))
            if keys[pygame.K_RETURN]:
                if player.max_life > player.life:
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_time >= self.interval:
                        player.life +=1
                        self.last_time = current_time

    