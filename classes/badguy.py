import pygame
from utility.Apathfinding import astar  # your A* function

class Badguy(pygame.sprite.Sprite):
    def __init__(self, pos, speed=2, margin=4, path_update_interval=12):
        super().__init__()
        self.image = pygame.image.load("assets/pnj/ennemis/south.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-30, -20)  # for collisions
        self.life = 3
        self.speed = speed

        # Pathfinding
        self.path = []  
        self.target_index = 0
        self.path_timer = 0
        self.path_update_interval = path_update_interval

        # Internal float position for smooth movement
        self.pos = pygame.Vector2(self.rect.center)
        self.collision_margin = margin
        self.collision_rect = self.hitbox.inflate(-self.collision_margin*2, -self.collision_margin*2)

    # Convert position to tile coordinates
    def tile_from_pos(self, pos, tile_size):
        return int(pos[0] // tile_size), int(pos[1] // tile_size)

    # Convert tile to top-left position
    def pos_from_tile(self, tile, tile_size):
        return tile[0] * tile_size, tile[1] * tile_size

    def update(self, player_rect, obstacles, map_w, map_h, tile_size):
        if self.life <= 0:
            self.kill()
            return

        # --- Update path periodically ---
        self.path_timer += 1
        if self.path_timer >= self.path_update_interval:
            self.path_timer = 0
            self._update_path(player_rect, obstacles, map_w, map_h, tile_size)

        # --- Follow path ---
        self._follow_path(obstacles, tile_size)

        # --- Update hitbox & rect to match float position ---
        self.hitbox.center = (int(self.pos.x), int(self.pos.y))
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    # Internal path update
    def _update_path(self, player_rect, obstacles, map_w, map_h, tile_size):
        player_tile = self.tile_from_pos(player_rect.center, tile_size)
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
