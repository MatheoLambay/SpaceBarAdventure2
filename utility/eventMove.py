

import pygame

class MoveEvent:
    def __init__(self, player, dir_x, dir_y, distance, speed=2):
        self.player = player
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.distance = distance
        self.speed = speed
        self.moved = 0
        self.done = False
        self.frame_timer = 0

        # 🔹 Déterminer la direction du joueur (pour les frames)
        if dir_x > 0:
            self.player.direction = "east"
        elif dir_x < 0:
            self.player.direction = "west"
        elif dir_y > 0:
            self.player.direction = "south"
        elif dir_y < 0:
            self.player.direction = "north"

    def update(self,dt):
        if self.done:
            return True

        # Avancer
        move_x = self.dir_x * self.speed
        move_y = self.dir_y * self.speed
        self.player.rect.x += move_x
        self.player.rect.y += move_y
        self.player.hitbox.x += move_x
        self.player.hitbox.y += move_y
        self.moved += abs(move_x) + abs(move_y)

        # 🔹 Gestion de l’animation
        self.frame_timer += 1
        if self.frame_timer % 8 == 0:  # changer toutes les 8 frames
            self.player.frame_index += 1
            if self.player.frame_index >= len(self.player.walk_frames):
                self.player.frame_index = 0
            self.player.image = self.player.walk_frames[int(self.player.frame_index)]

        # Si on a fini de bouger
        if self.moved >= self.distance:
            self.done = True
            # 🔹 remettre l’image idle à la fin
            self.player.frame_index = 0
            self.player.image = self.player.idle_image
            return True

        return False
