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
        self.panel = pygame.image.load("assets/pnj/talkpanel.png").convert_alpha()
        self.panel_rect = self.panel.get_rect(center = (400,450))
        self.text= ["salut","j'ai besoin de caca","tu as le caca ?"]
        self.needs = ["argent"]
        self.text_index = 0
        self.current_displayed_text = ""
        self.talk_index = 0
        self.last_talk = 0
        self.in_talk = 0

        self.last_frame_time = 0
        self.frame_interval = 40

        self.index = 0
        
        # position en pixels centrée sur la tuile
        col, row = tile_pos
        x = col * tile_size + tile_size // 2
        y = row * tile_size + tile_size // 2
        self.rect = self.image.get_rect(center=(x, y))


        # self.animation_speed = 0.15

    def update(self,player,screen,camera,keys,inventory):
    
        if self.index == 0:
            if self.rect.colliderect(player.hitbox):
                interaction_rect = self.interaction_img.get_rect(topright=self.rect.topright)
                screen.blit(self.interaction_img, camera.apply(interaction_rect))
                if keys[pygame.K_RETURN] and self.last_talk == 0:
                    player.control_enabled = False
                    self.in_talk = 1
                    self.index = self.text_index

                elif not keys[pygame.K_RETURN] and self.last_talk == 1:
                    self.last_talk = 0

        
        elif self.index == len(self.text):
            self.in_talk = 0
            
            player.control_enabled = True
            self.index = 0
            self.current_displayed_text = ""
            self.talk_index = 0
            self.in_talk = 0



        if self.in_talk:
            screen.blit(self.panel,self.panel_rect)
            my_font = pygame.font.SysFont('Comic Sans MS', 30)
            text_surface = my_font.render(self.current_displayed_text, False, (0, 0, 0))
            screen.blit(text_surface, self.panel_rect.topleft)
       
            # --- display letter one by one
            current_time = pygame.time.get_ticks()
            if current_time - self.last_frame_time >= self.frame_interval:
                if self.talk_index != len(self.text[self.text_index]):
                    self.current_displayed_text += self.text[self.text_index][self.talk_index]
                    self.talk_index+=1
                
                self.last_frame_time = current_time

            # --- skip animation
            if keys[pygame.K_RETURN] and self.last_talk == 0:
                if self.talk_index != len(self.text[self.text_index]):
                    self.current_displayed_text = self.text[self.text_index]
                    self.talk_index = len(self.text[self.text_index])
                else: # ---
                    self.index += 1
                    
                    if self.text_index != len(self.text)-1:
                        self.text_index +=1
                    else: 
                        for i in inventory:
                            if i.name in self.needs:
                                print("merci gros")
                            
                    
                    self.current_displayed_text = ""
                    self.talk_index = 0
                
                self.last_talk = 1

            elif not keys[pygame.K_RETURN] and self.last_talk == 1:
                self.last_talk = 0
            
            
            