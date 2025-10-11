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

        
        self.nohitbox_tiles = self.load_tileset_as_dict("assets/map/tileset.png", tile_size)
        self.hitbox_tiles = self.load_tileset_as_dict("assets/map/tilesethitbox.png", tile_size,False)
        self.textures = {**self.nohitbox_tiles, **self.hitbox_tiles}
        print(self.textures)
        # self.textures = {
        #     0: pygame.image.load("assets\map\grass.png").convert_alpha(),
        #     1: pygame.image.load("assets/map/rock.png").convert_alpha(),
        #     -4: pygame.image.load("assets/map/rock.png").convert_alpha(),
        #     -1: pygame.image.load("assets/map/river1.png").convert_alpha(),
        #     -2: pygame.image.load("assets/map/river2.png").convert_alpha(),
        #     -3: pygame.image.load("assets/map/leftwall.png").convert_alpha(),
        # }

        self.obstacles = []
    


    def load_tileset_as_dict(self,path, tile_size, positive_ids_only=True):
        image = pygame.image.load(path).convert_alpha()
        tiles = {}
        if positive_ids_only:
            id_counter = 0
        else:
            id_counter = -1

        for y in range(0, image.get_height(), tile_size):
            for x in range(0, image.get_width(), tile_size):
                tile = image.subsurface((x, y, tile_size, tile_size))
                tiles[id_counter] = tile
                if positive_ids_only:
                    id_counter += 1
                else:
                    id_counter -= 1

        return tiles

    def get_obstacles(self):
        """Retourne la liste des obstacles pour collisions"""
        return self.obstacles

    def draw(self, surface, camera):
        """Dessine la map sur l'écran avec la caméra"""
        for row_idx, row in enumerate(self.map_data):
            for col_idx, tile in enumerate(row):
                x = col_idx * self.tile_size
                y = row_idx * self.tile_size

                if tile == -1:
                    rect = pygame.Rect(x, y, 9, self.tile_size)
                else:
                    rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                
                img = self.textures[tile]
                if tile < 0:
                    self.obstacles.append((rect))
                

                surface.blit(img, camera.apply(rect))
                


    def get_tile(self, position):
        """Retourne le type de tuile à la position donnée"""
        tile_x = position[0] // self.tile_size
        tile_y = position[1] // self.tile_size

        if 0 <= tile_y < len(self.map_data) and 0 <= tile_x < len(self.map_data[0]):
            return self.map_data[tile_y][tile_x]
        else:
            return None  # Retourne None si hors de la map
        
   