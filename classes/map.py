import pygame

class Map:
    def __init__(self, map_data, tile_size):
        """
        map_data : liste de listes avec les tuiles
        tile_size : taille d'une tuile en pixels
        """
        self.map_data = map_data
        self.tile_size = tile_size
        self.height = len(map_data) * tile_size
        self.width = len(map_data[0]) * tile_size

        # créer la liste des obstacles automatiquement
        self.obstacles = []
        for row_idx, row in enumerate(map_data):
            for col_idx, tile in enumerate(row):
                x = col_idx * tile_size
                y = row_idx * tile_size
                rect = pygame.Rect(x, y, tile_size, tile_size)
                if tile == 1: 
                    self.obstacles.append((rect,"red"))
                if tile == 2:  # murs ou rivière = obstacles
                    self.obstacles.append((rect,"blue"))

    def get_obstacles(self):
        """Retourne la liste des obstacles pour collisions"""
        return self.obstacles

    def draw(self, surface, camera):
        """Dessine la map sur l'écran avec la caméra"""
        for row_idx, row in enumerate(self.map_data):
            for col_idx, tile in enumerate(row):
                x = col_idx * self.tile_size
                y = row_idx * self.tile_size
                rect = pygame.Rect(x, y, self.tile_size, self.tile_size)

                # choisir la couleur selon le type de tuile
                if tile == 0:
                    img = pygame.image.load("assets\map\grass.png").convert_alpha()
                elif tile == 1:
                    color = (0,0,255)      # mur
                elif tile == 2:
                    color = (255,0,0)      # rivière
                    
                elif tile == 3:
                    color = (139,69,19)    # pont
                
                elif tile == 4:
                    rect = pygame.Rect(x,y,10,self.tile_size)
                    self.obstacles.append((rect,"purple"))

                else:
                    color = (255,255,255)  # autre

                if tile != 0 and tile !=4:  
                   
                    pygame.draw.rect(surface, color, camera.apply(rect))
                    
                else:
                    
                    surface.blit(img, camera.apply(rect))

    def get_tile(self, position):
        """Retourne le type de tuile à la position donnée"""
        tile_x = position[0] // self.tile_size
        tile_y = position[1] // self.tile_size

        if 0 <= tile_y < len(self.map_data) and 0 <= tile_x < len(self.map_data[0]):
            return self.map_data[tile_y][tile_x]
        else:
            return None  # Retourne None si hors de la map