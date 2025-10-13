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
        self.text= ["salut","tu vas bien ?","moi ça va"]
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


        self.animation_speed = 0.15

    def update(self,player,screen,camera,keys,first_plan_event):

       
            
        if self.index == 0:
            if self.rect.colliderect(player.hitbox):
                interaction_rect = self.interaction_img.get_rect(topright=self.rect.topright)
                screen.blit(self.interaction_img, camera.apply(interaction_rect))
                if keys[pygame.K_RETURN] and self.last_talk == 0:
                    player.control_enabled = False
                    self.index = 1
                elif not keys[pygame.K_RETURN] and self.last_talk == 1:
                    self.last_talk = 0

        elif self.index == 1:
            screen.blit(self.panel,self.panel_rect)
            my_font = pygame.font.SysFont('Comic Sans MS', 30)
            text_surface = my_font.render(self.current_displayed_text, False, (0, 0, 0))
            screen.blit(text_surface, self.panel_rect.topleft)
            self.index = 2

        elif self.index == 2:
            screen.blit(self.panel,self.panel_rect)
            my_font = pygame.font.SysFont('Comic Sans MS', 30)
            text_surface = my_font.render(self.current_displayed_text, False, (0, 0, 0))
            screen.blit(text_surface, self.panel_rect.topleft)

            current_time = pygame.time.get_ticks()
            if current_time - self.last_frame_time >= self.frame_interval:
                if self.talk_index != len(self.text[self.text_index]):
                    self.current_displayed_text += self.text[self.text_index][self.talk_index]
                    self.talk_index+=1
                
                self.last_frame_time = current_time

            if self.talk_index == len(self.text[self.text_index]):
                if keys[pygame.K_RETURN]:
                    self.index = 3
                    self.text_index +=1
                    self.current_displayed_text = ""
                    self.talk_index = 0

        elif self.index == 3:
            screen.blit(self.panel,self.panel_rect)
            my_font = pygame.font.SysFont('Comic Sans MS', 30)
            text_surface = my_font.render(self.current_displayed_text, False, (0, 0, 0))
            screen.blit(text_surface, self.panel_rect.topleft)

            current_time = pygame.time.get_ticks()
            if current_time - self.last_frame_time >= self.frame_interval:
                if self.talk_index != len(self.text[self.text_index]):
                    self.current_displayed_text += self.text[self.text_index][self.talk_index]
                    self.talk_index+=1
                
                self.last_frame_time = current_time

            if self.talk_index == len(self.text[self.text_index]):
                if keys[pygame.K_RETURN]:
                    self.index = 4
                    self.text_index +=1
                    self.current_displayed_text = ""
                    self.talk_index = 0

        elif self.index == 4:
            screen.blit(self.panel,self.panel_rect)
            my_font = pygame.font.SysFont('Comic Sans MS', 30)
            text_surface = my_font.render(self.current_displayed_text, False, (0, 0, 0))
            screen.blit(text_surface, self.panel_rect.topleft)

            current_time = pygame.time.get_ticks()
            if current_time - self.last_frame_time >= self.frame_interval:
                if self.talk_index != len(self.text[self.text_index]):
                    self.current_displayed_text += self.text[self.text_index][self.talk_index]
                    self.talk_index+=1
                
                self.last_frame_time = current_time

            if self.talk_index == len(self.text[self.text_index]):
                if keys[pygame.K_RETURN]:
                    self.index = 5
                    self.last_talk = 1
            
        elif self.index == 5:
            print("fin")
            player.control_enabled = True
            self.index = 0
            self.text_index = 0
            self.current_displayed_text = ""
            self.talk_index = 0
            
            self.in_talk = 0
            
            

        # if self.in_talk:
        #     screen.blit(self.panel,self.panel_rect)
        #     my_font = pygame.font.SysFont('Comic Sans MS', 30)
        #     text_surface = my_font.render(self.current_displayed_text, False, (0, 0, 0))
        #     screen.blit(text_surface, self.panel_rect.topleft)

        #     current_time = pygame.time.get_ticks()
        #     if current_time - self.last_frame_time >= self.frame_interval:

        #         if self.talk_index != len(self.text[self.text_index]):
        #             self.current_displayed_text += self.text[self.text_index][self.talk_index]
        #             self.talk_index += 1
        #         # else:
        #         #     self.text_index+=1
                

        #         self.last_frame_time = current_time

            
            

        # if self.rect.colliderect(player.hitbox):
        #     if keys[pygame.K_RETURN] and self.last_talk == 0 and not self.in_talk:
        #         player.control_enabled = False

                
        #         if self.text_index < len(self.text):
        #             self.talk_index = 0
        #             self.current_displayed_text = ""
        #             self.in_talk = 1
                    
        #         else:
        #             print("fin")
        #             self.in_talk = 0
        #             self.current_displayed_text = ""
        #             self.talk_index = 0
        #             player.control_enabled = True
        #             self.text_index=0
                    
                    
        #         self.last_talk = 1
        #     elif not keys[pygame.K_RETURN] and self.last_talk == 1 and not self.in_talk:
        #         self.last_talk = 0
        
        #     #affiche le bouton d'interaction sur le pnj
        #     interaction_rect = self.interaction_img.get_rect(topright=self.rect.topright)
        #     screen.blit(self.interaction_img, camera.apply(interaction_rect))


            