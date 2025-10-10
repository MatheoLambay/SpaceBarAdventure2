import pygame

class Building:
    def __init__(self, matrix, tile_size, pos_x, pos_y):
        self.matrix = matrix
        self.tile_size = tile_size
        self.x = pos_x
        self.y = pos_y
        

        # self.roof_tiles = []
        # self.obstacles = []
        # for r,row in enumerate(matrix):
        #     for c,tile in enumerate(row):
        #         rect = pygame.Rect(pos_x + c*tile_size, pos_y + r*tile_size, tile_size, tile_size)
        #         if tile == 2: self.roof_tiles.append(rect)
        #         if tile == 1: self.obstacles.append(rect)

    def is_player_inside(self, player_rect):
        
        print(self.matrix)
        for row in range(len(self.matrix)):
            for tile in range(len(self.matrix[row])):
                rect = pygame.Rect(self.x*self.tile_size+tile*self.tile_size,self.y*self.tile_size+row*self.tile_size,self.tile_size,self.tile_size)
                if player_rect.colliderect(rect):
                    return True
        return False
        # for row,col in self.entrances:
        #     rect = pygame.Rect(self.x*64 + col*self.tile_size, self.y*64 + row*self.tile_size, self.tile_size, self.tile_size)
        #     if player_rect.colliderect(rect):
        #         return True
        # return False

    def draw(self, surface, camera, player_rect):


        for r,row in enumerate(self.matrix):
            for c,tile in enumerate(row):
                rect = pygame.Rect(self.x*64 + c*self.tile_size, self.y*64 + r*self.tile_size,
                                   self.tile_size, self.tile_size)
               
                if tile==1:
                    color=(150,0,0)
                elif tile==2:
                    # Masquer toit si joueur dedans
                    if self.is_player_inside(player_rect):
                        continue
                    color=(139,69,19)
                else:
                    color=(255,255,255)
                pygame.draw.rect(surface, color, camera.apply(rect))