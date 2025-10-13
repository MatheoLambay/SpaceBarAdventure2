import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, frames,frames_fight, pos):
        super().__init__()
        self.frames = frames
        self.frame_index = 0
        self.frames_fight = frames_fight
        self.frame_fight_index = 0
        self.direction = "S"
        self.image = self.frames[self.direction][0]  # Default to south idle frame
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-30, -20)  # hitbox plus petite que le sprite
        self.animation_speed = 0.15
        self.current_tile = None 
        self.control_enabled = True 
        self.show_crosshair = True
        self.crosshair_image = pygame.image.load("assets/player/crossair.png").convert_alpha()
        self.rect_crosshair = self.crosshair_image.get_rect()
        self.crosshair_hitbox = self.rect_crosshair.inflate(-20, -20) 
        self.crosshair_radius = 50
        self.last_click_state = 0
        self.life = 10
        self.max_life = 10
        self.is_punching = 0
        
  

    def draw_crosshair(self, surface, camera):
        mx, my = pygame.mouse.get_pos()
        
        px, py = self.rect.center

        dx = mx - camera.apply(self.rect).centerx
        dy = my - camera.apply(self.rect).centery

        angle = math.atan2(dy, dx)  

        chx = px + math.cos(angle) * self.crosshair_radius
        chy = py + math.sin(angle) * self.crosshair_radius
        self.rect_crosshair.center = (chx, chy)
        self.crosshair_hitbox.center = (chx, chy)

        #pygame.draw.rect(surface, (255, 0, 0), camera.apply(self.crosshair_hitbox), 1)
        surface.blit(self.crosshair_image, camera.apply(self.rect_crosshair))
        
    def draw_life(self,screen,camera):
        if self.life < self.max_life:
            ratio = self.life / self.max_life
            x = camera.apply(self.rect).topleft[0]
            y = camera.apply(self.rect).topleft[1]
            pygame.draw.rect(screen,"red",(x,y,64,5))
            pygame.draw.rect(screen,"green",(x,y,64*ratio,5))


    def update(self, keys, obstacles, game_map,ennemis): # Add game_map as argument
        if not self.control_enabled:
            return
        
        if self.life < 1:
            print("DEAD")
        
       


        dx, dy = 0, 0

        # --- Déplacements ---
        if keys[pygame.K_z]:
            dy = -4
            self.direction = "N"
        if keys[pygame.K_s]:
            dy = 4
            self.direction = "S"
        if keys[pygame.K_q]:
            dx = -4
            self.direction = "W"
        if keys[pygame.K_d]:
            dx = 4
            self.direction = "E"

        moving = dx != 0 or dy != 0

        # --- Animation ---
        if moving and self.is_punching == 0:
            currents_frames = self.frames[self.direction][1:]
            self.frame_index += self.animation_speed
           
            if self.frame_index >= len(currents_frames):
                self.frame_index = 0
            self.image = currents_frames[int(self.frame_index)]

        elif self.is_punching == 1:
            currents_frames = self.frames_fight[self.direction]
            self.frame_fight_index += self.animation_speed
           
            if self.frame_fight_index >= len(currents_frames):
                self.frame_fight_index = 0
                self.is_punching = 0
                
            self.image = currents_frames[int(self.frame_fight_index)]

        else:
            self.frame_index = 0
            self.frame_fight_index = 0
            self.image = self.frames[self.direction][0]
        
       

        # --- Collision X ---
        self.rect.x += dx
        self.hitbox.x += dx  # Update hitbox position
        for obs in obstacles:
            if self.hitbox.colliderect(obs):
                if dx > 0:
                    self.hitbox.right = obs.left
                    self.rect.right = self.hitbox.right + (self.rect.width - self.hitbox.width) / 2
                elif dx < 0:
                    self.hitbox.left = obs.right
                    self.rect.left = self.hitbox.left - (self.rect.width - self.hitbox.width) / 2

        # --- Collision Y ---
        self.rect.y += dy
        self.hitbox.y += dy  # Update hitbox position
        for obs in obstacles:
            if self.hitbox.colliderect(obs):
                if dy > 0:
                    self.hitbox.bottom = obs.top
                    self.rect.bottom = self.hitbox.bottom + (self.rect.height - self.hitbox.height) / 2
                elif dy < 0:
                    self.hitbox.top = obs.bottom
                    self.rect.top = self.hitbox.top - (self.rect.height - self.hitbox.height) / 2

        # --- Tile Detection ---
        self.current_tile = game_map.get_tile(self.hitbox.center)

        # --- Mouse Click Detection ---
        
        if pygame.mouse.get_pressed()[0] and self.last_click_state == 0 and self.is_punching == 0:
            self.is_punching = 1
            print("ici")
            
            if self.rect_crosshair.centerx < self.rect.centerx:
                self.direction = "W"
            elif self.rect_crosshair.centerx > self.rect.centerx:
                self.direction = "E"
            elif self.rect_crosshair.centery < self.rect.centery:
                self.direction = "N"
            else:
                self.direction = "S"
                
            for ennemi in ennemis:
                if self.crosshair_hitbox.colliderect(ennemi.hitbox):
                    ennemi.life -= 1
            
            self.last_click_state = 1
            

        elif not pygame.mouse.get_pressed()[0] and self.last_click_state == 1 and self.is_punching == 0:
            self.last_click_state = 0

 