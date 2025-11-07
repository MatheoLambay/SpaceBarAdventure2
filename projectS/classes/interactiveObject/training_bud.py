import pygame

class training_bud(pygame.sprite.Sprite):
    def __init__(self,frames,pos,tile_size):
        super().__init__()
        self.direction = "S"
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.direction][0]

        self.rect = self.image.get_rect(topleft=(pos[0]*tile_size,pos[1]*tile_size))
        self.hitbox = self.rect.inflate(-20,-10)
        self.in_animation = False
        self.animation_speed = 0.15
        

    def update(self,screen,player,keys,camera,inventory):

        
        if self.in_animation:
            
            currents_frames = self.frames[self.direction][1:]
            self.frame_index += self.animation_speed

            if self.frame_index >= len(currents_frames):
                self.frame_index = 0
                self.in_animation = False
                self.image = self.frames[self.direction][0]
            else:
                self.image = currents_frames[int(self.frame_index)]
            
            

        if pygame.mouse.get_pressed()[0] and self.in_animation == False:
            if player.crosshair_hitbox.colliderect(self.hitbox):
                self.in_animation = True
               
