import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, frames, pos):
        super().__init__()
        self.frames = frames
        self.idle_image = self.frames[0]
        self.walk_frames = self.frames[1:]
        self.frame_index = 0
        self.image = self.idle_image
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-30, -20)  # hitbox plus petite que le sprite
        self.animation_speed = 0.15

    def update(self, keys, obstacles):
        dx, dy = 0, 0

        # --- Déplacements ---
        if keys[pygame.K_UP]:
            dy = -4
        if keys[pygame.K_DOWN]:
            dy = 4
        if keys[pygame.K_LEFT]:
            dx = -4
        if keys[pygame.K_RIGHT]:
            dx = 4

        moving = dx != 0 or dy != 0

        # --- Animation ---
        if moving:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.walk_frames):
                self.frame_index = 0
            self.image = self.walk_frames[int(self.frame_index)]
        else:
            self.frame_index = 0
            self.image = self.idle_image

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
        