import pygame

class Building:
    def __init__(self, matrix, textures, tile_size, pos_x, pos_y):
        self.matrix = matrix
        self.tile_size = tile_size
        self.x = pos_x
        self.y = pos_y
        self.textures = textures

    def is_player_inside(self, player_rect):
        
        """"Vérifie si le joueur est à l'intérieur du bâtiment"""
        """Vérifie si le joueur est sur une tuile qui constitue le toit du batiment"""
        for row in range(len(self.matrix)):
            for tile in range(len(self.matrix[row])):
                rect = pygame.Rect(self.x*self.tile_size+tile*self.tile_size,self.y*self.tile_size+row*self.tile_size,self.tile_size,self.tile_size)
                if player_rect.colliderect(rect):
                    return True
        return False
    
    
    def draw(self, surface, camera, player_rect):

        for r,row in enumerate(self.matrix):
            for c,tile in enumerate(row):
                if self.is_player_inside(player_rect):
                    break
                rect = pygame.Rect(self.x*64 + c*self.tile_size, self.y*64 + r*self.tile_size,
                                   self.tile_size, self.tile_size)
                
                if tile > -1:
                    img = self.textures[tile]
                    # if tile < 0:
                    #     self.obstacles.append((rect))
                    surface.blit(img, camera.apply(rect))
                # if tile==1:
                #     color=(150,0,0)
                # elif tile==2:
                #     
                #     color=(139,69,19)
                # else:
                #     color=(255,255,255)
                # pygame.draw.rect(surface, color, camera.apply(rect))