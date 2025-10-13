import pygame
import os
from classes.player import Player
from classes.camera import Camera
from classes.map import Map
from classes.pnj import PNJ
from classes.building import Building
from utility.eventManager import EventManager
from utility.eventMove import MoveEvent
from utility.eventWait import WaitEvent
from classes.badguy import Badguy
from classes.items import items
from utility.eventTile import eventTile


def load_frames(folder_path):
    frames = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".png"):
            frame = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
            frames.append(frame)
    return frames

def load_tileset_as_dict(path, tile_size, positive_ids_only=True):
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

class game_manager:
    def __init__(self,screen):
        self.screen = screen
        self.tile_size = 64
        self.map_data = [
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,-4,-4,-4,-4,-4,-4,-4,-4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3,-4,-4, 0, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3,-4,-4,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-4,-4, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3,-4,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-4,-4, 3, 3, 3, 3, 3, 3],
            [3, 3,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3],
            [3,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3],
            [3,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0,-12,-13,-13,-13,-13,-13,-14, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3],
            [3,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0,-22, 2, 1, 1, 1, 1,-24, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3],
            [3,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0,-22, 1, 1, 1, 1, 1,-24, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3],
            [3,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0,-22, 1, 1, 1, 1, 1,-24, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3],
            [3,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0,-22, 1, 1, 1, 1, 1,-24, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3],
            [3,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0,-22, 1, 1, 1, 1, 1,-24, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3],
            [3,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0,-32,-33,-33,1,-33,-33,-34, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3],
            [3,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3],
            [3, 3,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3, 3],
            [3, 3, 3,-4,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-4,-4,-4, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3,-4,-4,-4,-4,-4,-4,-4,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,-4, 0, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,-4,-4,-4,-4,-4,-4,-4,-4,-4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],

        ]
        nohitbox_tiles = load_tileset_as_dict("assets/map/tileset.png", 64)
        hitbox_tiles = load_tileset_as_dict("assets/map/tilesethitbox.png", 64,False)
        roofs_tiles = load_tileset_as_dict("assets/map/tileset_roof.png", 64)
        textures = {**nohitbox_tiles, **hitbox_tiles}

        frames_south = load_frames("assets/player/animations/walk-1/south")  # 1.png = repos, 2.png+ = marche
        frames_north = load_frames("assets/player/animations/walk-1/north")
        frames_east = load_frames("assets/player/animations/walk-1/east")
        frames_west = load_frames("assets/player/animations/walk-1/west")
        frames = {"S":frames_south, "N":frames_north, "E":frames_east, "W":frames_west}
        frames_fight_south = load_frames("assets/player/animations/cross-punch/south")
        frames_fight_north = load_frames("assets/player/animations/cross-punch/north")
        frames_fight_east = load_frames("assets/player/animations/cross-punch/east")
        frames_fight_west = load_frames("assets/player/animations/cross-punch/west")
        frames_fight = {"S":frames_fight_south, "N":frames_fight_north, "E":frames_fight_east, "W":frames_fight_west}

        self.player = Player(frames,frames_fight, pos=(14*64, 4*64))
        self.inventory = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)

        badguy_south = load_frames("assets\pnj\ennemis\scary-walk\south")
        badguy_north = load_frames("assets/pnj/ennemis/scary-walk/north")
        badguy_east = load_frames("assets/pnj/ennemis/scary-walk/east")
        badguy_west = load_frames("assets/pnj/ennemis/scary-walk/west")
        badguy_frames = {"S":badguy_south, "N":badguy_north, "E":badguy_east, "W":badguy_west}
        badguy_fight_south = load_frames("assets\pnj\ennemis\cross-punch\south")
        badguy_fight_north = load_frames("assets/pnj/ennemis/cross-punch/north")
        badguy_fight_east = load_frames("assets/pnj/ennemis/cross-punch/east")
        badguy_fight_west = load_frames("assets/pnj/ennemis/cross-punch/west")
        badguy_fight_frames = {"S":badguy_fight_south, "N":badguy_fight_north, "E":badguy_fight_east, "W":badguy_fight_west}
        badguy2 = Badguy(badguy_frames,badguy_fight_frames,pos=(15*self.tile_size, 10*self.tile_size))
        self.all_ennemis = pygame.sprite.Group()
        self.all_ennemis.add(badguy2)


        pnj_positions = [(6,6)]
        self.pnjs = []
        test=1
        for tile_pos in pnj_positions:
            self.pnjs.append(PNJ("assets/player/animations/walk-1/south/frame_000.png", tile_pos, self.tile_size, str(test)))
            test+=1

        self.buildings = []
        b1_matrix = [
            [0,1,1,1,1,1,2],
            [10,11,11,11,11,11,12],
            [10,11,11,11,11,11,12],
            [10,11,11,11,11,11,12],
            [10,11,11,11,11,11,12,12],
            [10,11,11,11,11,11,12],
            [20,21,21,21,21,21,22] 
        ]

        b1 = Building(b1_matrix,roofs_tiles, self.tile_size, pos_x=11, pos_y=9)
        self.buildings.append(b1)
        
        self.game_map = Map(self.map_data, self.tile_size,textures)

        # ev = eventTile(2,new_map)
        # event_tiles = pygame.sprite.Group(ev)

        self.map_width = len(self.map_data[0]) * self.tile_size
        self.map_height = len(self.map_data) * self.tile_size
        self.camera = Camera(self.map_width, self.map_height, 800, 600)

    def open(self,screen):
        pass

    def update(self,keys,screen,dt):
        
        obstacles = self.game_map.get_obstacles()
    
        self.all_sprites.update(keys, obstacles, self.game_map,self.all_ennemis) # Pass game_map

        
        self.all_ennemis.update(self.player, obstacles,self.map_width,self.map_height,self.tile_size)
        
        self.camera.update(self.player)

        # --- Rendu ---
        self.game_map.draw(self.screen, self.camera)

        # # dessiner obstacles avec offset caméra
        # for obs,color in obstacles:
        #     pygame.draw.rect(screen, color, camera.apply(obs))

        # dessiner joueur
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))
            # pygame.draw.rect(screen, (0,255,0), camera.apply(sprite.hitbox), 2)
        
        for ennemie in self.all_ennemis:
            # ennemie.update(keys, obstacles, game_map,player)
            self.screen.blit(ennemie.image,self.camera.apply(ennemie.rect))
            pygame.draw.rect(self.screen,'red',self.camera.apply(ennemie.hitbox),1)
        
        # print(game_map.get_tile(player.hitbox.center)) # Update current_tile)
        

        for pnj in self.pnjs:
            pnj.update(self.player,self.screen,self.camera,keys,self.inventory)
            self.screen.blit(pnj.image, self.camera.apply(pnj.rect))
        

        for b in self.buildings:
            b.draw(self.screen, self.camera, self.player.hitbox)


        self.player.draw_crosshair(self.screen, self.camera)
        self.player.draw_life(self.screen, self.camera)
        # pygame.draw.rect(screen,'green',camera.apply(player.hitbox),1)

        # event_tiles.update(game_map.get_tile(player.hitbox.center),game_map)
        # events.update(dt)