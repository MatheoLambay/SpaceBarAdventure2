import pygame
from utility.Apathfinding import astar  # your A* function

class PNJ(pygame.sprite.Sprite):
    def __init__(self, frames, tile_pos, tile_size,talk,can_attack,frames_walk,frame_fight,drop):
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
        self.text= talk
        
        # position en pixels centrée sur la tuile
        col, row = tile_pos
        x = col * tile_size + tile_size // 2
        y = row * tile_size + tile_size // 2
        self.rect = self.image.get_rect(center=(x, y))

        self.text_index = 0
        self.current_displayed_text = ""
        self.talk_index = 0
        self.last_talk = 0
        self.in_talk = 0

        self.last_frame_time = 0
        self.frame_interval = 40

        self.index = 0
        
        self.can_attack = can_attack
        self.life = 3
        self.max_life = 3
        self.frames_walk = frames_walk
        self.frame_walk_index = 0
        self.frames_fight = frame_fight
        self.frames_fight_index = 0
        self.animation_speed = 0.15
        self.speed = 2
        self.pos = pygame.Vector2(self.rect.center)
        self.collision_margin = 2
        self.collision_rect = self.rect.inflate(-self.collision_margin*2, -self.collision_margin*2)
        self.direction = "S"
        # Pathfinding
        self.path = []  
        self.target_index = 0
        self.path_timer = 0
        self.path_update_interval = 12
        self.hitbox = self.rect.inflate(-30, -20)  # for collisions
        self.drop = drop
        
        


        # self.animation_speed = 0.15

    # Convert position to tile coordinates
    def tile_from_pos(self, pos, tile_size):
        return int(pos[0] // tile_size), int(pos[1] // tile_size)

    # Convert tile to top-left position
    def pos_from_tile(self, tile, tile_size):
        return tile[0] * tile_size, tile[1] * tile_size

    def attack(self,cible):
        cible.life -=1

    def update(self,player,screen,camera,keys,obstacles,map_w, map_h,inventory):

        if self.life == 0 and self.can_attack:
            if self.drop != "None":
                if self.drop not in inventory:
                    inventory.append(self.drop)
            self.kill()
            return

        if self.life < self.max_life and self.can_attack:

            if self.hitbox.colliderect(player.hitbox):
                currents_frames = self.frames_fight[self.direction][1:]
                self.frames_fight_index += self.animation_speed
                if self.frames_fight_index >= len(currents_frames):
                    self.frames_fight_index = 0
                    self.attack(player)
                self.image = currents_frames[int(self.frames_fight_index)]
            else:
                # --- Update path periodically ---
                self.path_timer += 1
                if self.path_timer >= self.path_update_interval:
                    self.path_timer = 0
                    self._update_path(player.hitbox, obstacles, map_w, map_h, 64)

                # --- Follow path ---
                self._follow_path(obstacles, 64)

                # --- Update rect & rect to match float position ---
                
                self.rect.center = (int(self.pos.x), int(self.pos.y))
                self.hitbox.center = (int(self.pos.x), int(self.pos.y))

                currents_frames = self.frames_walk[self.direction][1:]
                self.frame_walk_index += self.animation_speed
                if self.frame_walk_index >= len(currents_frames):
                    self.frame_walk_index = 0
                self.image = currents_frames[int(self.frame_walk_index)]

        else:
    
            if self.index == 0 and len(self.text) > 0:
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
                self.text_index = 0



            if self.in_talk:
                screen.blit(self.panel,self.panel_rect)
                my_font = pygame.font.SysFont('Comic Sans MS', 20)
                text_surface = my_font.render(self.current_displayed_text, False, (0, 0, 0))
                screen.blit(text_surface, (self.panel_rect.topleft[0]+20,self.panel_rect.topleft[1]+10))
        
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
                        

                        self.text_index +=1
                        
                                
                        
                        self.current_displayed_text = ""
                        self.talk_index = 0
                    
                    self.last_talk = 1

                elif not keys[pygame.K_RETURN] and self.last_talk == 1:
                    self.last_talk = 0
            
            
    # Internal path update
    def _update_path(self, player, obstacles, map_w, map_h, tile_size):
        player_tile = self.tile_from_pos(player.center, tile_size)
        enemy_tile = self.tile_from_pos(self.pos, tile_size)

        # Ensure target tile is free
        if any(pygame.Rect(player_tile[0]*tile_size, player_tile[1]*tile_size, tile_size, tile_size).colliderect(o) for o in obstacles):
            found = False
            for dx, dy in [(0,0),(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)]:
                cand = (player_tile[0]+dx, player_tile[1]+dy)
                if 0 <= cand[0] < map_w and 0 <= cand[1] < map_h:
                    rect = pygame.Rect(cand[0]*tile_size, cand[1]*tile_size, tile_size, tile_size)
                    if not any(rect.colliderect(o) for o in obstacles):
                        player_tile = cand
                        found = True
                        break
            if not found:
                self.path = []
                self.target_index = 0
                return

        # Use your astar function to get path
        path = astar(enemy_tile, player_tile, obstacles, map_w, map_h, size=tile_size - self.collision_margin*2)
        if path:
            self.path = path
            self.target_index = 1 if len(path) > 1 else 0
        else:
            self.path = []
            self.target_index = 0

    # Internal path following
    def _follow_path(self, obstacles, tile_size):
        if not self.path or self.target_index >= len(self.path):
            return

        target_tile = self.path[self.target_index]
        target_center = pygame.Vector2(self.pos_from_tile(target_tile, tile_size)) + pygame.Vector2(tile_size/2, tile_size/2)
        vec = target_center - self.pos
        if abs(vec.x) > abs(vec.y):
            self.direction = "E" if vec.x > 0 else "W"
        else:
            self.direction = "S" if vec.y > 0 else "N"

        # Snap if close
        if vec.length() < 1.5:
            self.pos = target_center
            self.target_index += 1
            return

        move = vec.normalize() * self.speed

        # Small-step sliding
        max_step = 2.0
        steps = max(int(move.length() / max_step), 1)
        step_vec = move / steps

        for _ in range(steps):
            # Full move
            new_pos = self.pos + step_vec
            new_rect = self.hitbox.copy()
            new_rect.center = (int(new_pos.x), int(new_pos.y))
            if not any(new_rect.colliderect(o) for o in obstacles):
                self.pos = new_pos
                continue

            # Slide X
            new_pos_x = pygame.Vector2(self.pos.x + step_vec.x, self.pos.y)
            new_rect.center = (int(new_pos_x.x), int(new_pos_x.y))
            if not any(new_rect.colliderect(o) for o in obstacles):
                self.pos.x = new_pos_x.x

            # Slide Y
            new_pos_y = pygame.Vector2(self.pos.x, self.pos.y + step_vec.y)
            new_rect.center = (int(new_pos_y.x), int(new_pos_y.y))
            if not any(new_rect.colliderect(o) for o in obstacles):
                self.pos.y = new_pos_y.y