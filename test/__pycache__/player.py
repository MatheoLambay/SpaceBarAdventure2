# ========== player.py ==========
import pygame
TILE = 64

class Player:
    def __init__(self, x, y, speed, walls):
        self.rect = pygame.Rect(x, y, TILE, TILE)
        self.speed = speed
        self.walls = walls

    def handle_input(self):
        keys = pygame.key.get_pressed()
        move_x = move_y = 0
        if keys[pygame.K_z]: move_y = -self.speed
        if keys[pygame.K_s]: move_y = self.speed
        if keys[pygame.K_q]: move_x = -self.speed
        if keys[pygame.K_d]: move_x = self.speed
        self.move(move_x, move_y)

    def move(self, dx, dy):
        if dx != 0:
            new_rect = self.rect.move(dx, 0)
            if not any(new_rect.colliderect(w) for w in self.walls):
                self.rect = new_rect
        if dy != 0:
            new_rect = self.rect.move(0, dy)
            if not any(new_rect.colliderect(w) for w in self.walls):
                self.rect = new_rect


