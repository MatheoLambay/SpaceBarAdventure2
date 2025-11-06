import pygame
from utility.filesTools import load_frames, load_character_sprites

class skinSelect(pygame.sprite.Sprite):
    def __init__(self,path,pos,tile_size):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(pos[0]*tile_size,pos[1]*tile_size))
        self.last_talk = 0
        self.hitbox = self.rect.inflate(-20,-10)
        self.skin1_rect = pygame.Rect(self.rect.topleft[0],self.rect.topleft[1],tile_size,tile_size*2)
        self.skin2_rect = pygame.Rect(self.skin1_rect.topright[0],self.skin1_rect.topright[1],tile_size,tile_size*2)
        self.skin3_rect = pygame.Rect(self.skin2_rect.topright[0],self.skin2_rect.topright[1],tile_size,tile_size*2)
        self.skin1 = load_character_sprites("assets/player/animations/walk_green.png")
        self.skin2 = load_character_sprites("assets/player/animations/walk_blue.png")
        self.skin3 = load_character_sprites("assets/player/animations/walk_red.png")
        
        self.interaction_img = pygame.image.load("assets/pnj/interaction.png").convert_alpha()

    def update(self,screen,player,keys,camera):
        pygame.draw.rect(screen, (0, 255, 0), camera.apply(self.skin1_rect), 1)
        pygame.draw.rect(screen, (255, 255, 0), camera.apply(self.skin2_rect), 1)
        pygame.draw.rect(screen, (0, 255, 255), camera.apply(self.skin3_rect), 1)

        if self.rect.colliderect(player.hitbox):
            if self.skin1_rect.colliderect(player.hitbox):
                n_rect = self.skin1_rect.topright
                skin = self.skin1
            elif self.skin2_rect.colliderect(player.hitbox):
                n_rect = self.skin2_rect.topright
                skin = self.skin2
            elif self.skin3_rect.colliderect(player.hitbox):
                n_rect = self.skin3_rect.topright
                skin = self.skin3
                
            interaction_rect = self.interaction_img.get_rect(topright=n_rect)
            screen.blit(self.interaction_img, camera.apply(interaction_rect))

            if keys[pygame.K_RETURN] and self.last_talk == 0:
                frames_fight_south = load_frames("assets/player/animations/cross-punch/south")
                frames_fight_north = load_frames("assets/player/animations/cross-punch/north")
                frames_fight_east = load_frames("assets/player/animations/cross-punch/east")
                frames_fight_west = load_frames("assets/player/animations/cross-punch/west")
                frames_fight = {"S":frames_fight_south, "N":frames_fight_north, "E":frames_fight_east, "W":frames_fight_west}

                player.change_skin(skin,frames_fight)
                 

            elif not keys[pygame.K_RETURN] and self.last_talk == 1:
                self.last_talk = 0

    