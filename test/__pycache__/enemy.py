import pygame
from pathfinding import astar, TILE, tile_blocked

class Enemy:
    def __init__(self, x, y, speed, walls, map_w, map_h, margin=4, path_update_interval=12):
        """
        margin: pixels to shrink collision rectangle inside the visible TILE
        path_update_interval: frames between path recalculations
        """
        self.rect = pygame.Rect(x, y, TILE, TILE)  # visible rect
        self.collision_size = TILE - margin * 2     # shrink for collisions
        self.collision_offset = margin
        self.pos = pygame.Vector2(self.rect.center)  # float position
        self.speed = speed
        self.walls = walls
        self.path = []
        self.target_index = 0
        self.map_w = map_w
        self.map_h = map_h

        # Pathfinding timing
        self.path_timer = 0
        self.path_update_interval = path_update_interval

    def tile_from_pos(self, pos):
        return int(pos[0] // TILE), int(pos[1] // TILE)

    def pos_from_tile(self, tile):
        return tile[0] * TILE, tile[1] * TILE

    # --- Update function called every frame ---
    def update(self, player_pos):
        # --- Update path periodically ---
        self.path_timer += 1
        if self.path_timer >= self.path_update_interval:
            self.path_timer = 0
            self._update_path(player_pos)

        # --- Move along current path ---
        self._follow_path()

    # --- Internal path update ---
    def _update_path(self, player_pos):
        player_tile = self.tile_from_pos(player_pos)
        enemy_tile = self.tile_from_pos(self.pos)

        # Ensure goal tile is reachable with shrinked collision
        if tile_blocked(player_tile[0], player_tile[1], self.walls, self.map_w, self.map_h, size=self.collision_size):
            found = False
            for dx, dy in [(0,0),(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)]:
                cand = (player_tile[0]+dx, player_tile[1]+dy)
                if 0 <= cand[0] < self.map_w and 0 <= cand[1] < self.map_h:
                    if not tile_blocked(cand[0], cand[1], self.walls, self.map_w, self.map_h, size=self.collision_size):
                        player_tile = cand
                        found = True
                        break
            if not found:
                self.path = []
                self.target_index = 0
                return

        path = astar(enemy_tile, player_tile, self.walls, self.map_w, self.map_h, size=self.collision_size)
        if path:
            self.path = path
            self.target_index = 1 if len(path) > 1 else 0
        else:
            self.path = []
            self.target_index = 0

    # --- Internal path-following with small-step sliding ---
    def _follow_path(self):
        if not self.path or self.target_index >= len(self.path):
            return

        target_tile = self.path[self.target_index]
        target_center = pygame.Vector2(self.pos_from_tile(target_tile)) + pygame.Vector2(TILE/2, TILE/2)
        vec = target_center - self.pos

        if vec.length() < 1.5:
            self.pos = target_center
            self.rect.center = (int(self.pos.x), int(self.pos.y))
            self.target_index += 1
            return

        move = vec.normalize() * self.speed

        max_step = 2.0
        steps = max(int(move.length() / max_step), 1)
        step_vec = move / steps

        for _ in range(steps):
            # Full diagonal
            new_pos = self.pos + step_vec
            new_rect = pygame.Rect(
                int(new_pos.x - self.collision_size/2),
                int(new_pos.y - self.collision_size/2),
                self.collision_size,
                self.collision_size
            )
            if not any(new_rect.colliderect(w) for w in self.walls):
                self.pos = new_pos
                continue

            # Slide X
            new_pos_x = pygame.Vector2(self.pos.x + step_vec.x, self.pos.y)
            new_rect.center = (int(new_pos_x.x), int(new_pos_x.y))
            if not any(new_rect.colliderect(w) for w in self.walls):
                self.pos.x = new_pos_x.x

            # Slide Y
            new_pos_y = pygame.Vector2(self.pos.x, self.pos.y + step_vec.y)
            new_rect.center = (int(new_pos_y.x), int(new_pos_y.y))
            if not any(new_rect.colliderect(w) for w in self.walls):
                self.pos.y = new_pos_y.y

        self.rect.center = (int(self.pos.x), int(self.pos.y))
