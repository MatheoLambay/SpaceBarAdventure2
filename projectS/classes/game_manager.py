import pygame
import os
import json
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
from utility.eventChangeTile import eventChangeTile
from classes.bartender import Bartender



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

def read_data(link):
    with open(link,"r", encoding='utf-8') as r:
        return json.load(r)

class game_manager:
    def __init__(self,screen):
        self.screen = screen
        self.tile_size = 64

        data = read_data("projectS\data\map1.json")
        
        
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

        x,y = data["player_coord"]
        self.player = Player(frames,frames_fight, pos=(x*self.tile_size, y*self.tile_size))
        self.inventory = []
        self.all_sprites = pygame.sprite.Group(self.player)
        
        self.load_game(data)
        #eventChangeTile(-4, 1, data["map_data"])
        self.test = []

        

        

        # self.event_tiles = pygame.sprite.Group(ev)

       



    def load_game(self,data):
        self.map_data = data["map_data"]

        nohitbox_tiles = load_tileset_as_dict("assets/map/tilesetSpace.png", 64)
        hitbox_tiles = load_tileset_as_dict("assets/map/tilesetSpaceHitbox.png", 64,False)
        roofs_tiles = load_tileset_as_dict("assets/map/tileset_roof.png", 64)
        textures = {**nohitbox_tiles, **hitbox_tiles}
        x,y = data["player_coord"]

        self.player.set_position((x*self.tile_size-self.tile_size//2,y*self.tile_size-self.tile_size//2))

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
        
        self.all_ennemis = pygame.sprite.Group()
        ennemis_position = data["ennemis"]
        for e in ennemis_position:
            self.all_ennemis.add(Badguy(badguy_frames,badguy_fight_frames,pos=(e[0]*self.tile_size, e[1]*self.tile_size)))
        
    
        pnj_data= data["pnjs"]
        self.pnjs = pygame.sprite.Group()
        for p in pnj_data:
            self.pnjs.add(PNJ("assets/player/animations/walk-1/south/frame_000.png", p[0], self.tile_size, p[1],p[2],badguy_frames,badguy_fight_frames))
            
            

        # for tile_pos in pnj_positions:
        #     self.pnjs.append(PNJ("assets/player/animations/walk-1/south/frame_000.png", tile_pos, self.tile_size, str(test)))
            

        self.buildings = []
        self.roofs = data["building"]
        for roof in self.roofs:
        
            
            self.buildings.append(Building(roof[0],roofs_tiles, self.tile_size, pos_x=roof[1][0], pos_y=roof[1][1]))
        
        
        self.game_map = Map(self.map_data, self.tile_size,textures)

        
        self.map_width = len(self.map_data[0]) * self.tile_size
        self.map_height = len(self.map_data) * self.tile_size

        self.camera = Camera(self.map_width, self.map_height, 800, 600)
        self.event_tiles = pygame.sprite.Group()
        for e in data["TPtile"]:
            path = "projectS\data\%s.json"%(e[1])
            ev = eventTile(e[0],path)
            self.event_tiles.add(ev)

        self.obstacles = self.game_map.get_obstacles()

        self.great_pnj = pygame.sprite.Group()
        for gp in data["greatpnj"]:
          # Conversion des clés en int
            nd = {int(k): v for k, v in gp[0].items()}
            self.great_pnj.add(Bartender(gp[1],nd))
            

            
    def load_map(self,new_map):
        self.game = new_map
        self.obstacles = self.game_map.get_obstacles()


    def open(self,screen):
        pass

    def update(self,keys,screen,dt):

        # if keys[pygame.K_b]:
        #     self.inventory.append("caca")
            
            
        
        obstacles = self.game_map.get_obstacles()
    
        self.all_sprites.update(keys, obstacles, self.game_map,self.all_ennemis,self.pnjs) # Pass game_map

        
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
            pygame.draw.rect(self.screen, (0,255,0), self.camera.apply(sprite.hitbox), 2)
        
        for ennemie in self.all_ennemis:
            # ennemie.update(keys, obstacles, game_map,player)
            self.screen.blit(ennemie.image,self.camera.apply(ennemie.rect))
            pygame.draw.rect(self.screen,'red',self.camera.apply(ennemie.hitbox),1)
        
        # print(game_map.get_tile(player.hitbox.center)) # Update current_tile)
        
        self.pnjs.update(self.player,self.screen,self.camera,keys,self.obstacles,self.map_width,self.map_height)
        for p in self.pnjs:
            self.screen.blit(p.image,self.camera.apply(p.rect))
        

        for b in self.buildings:
            b.draw(self.screen, self.camera, self.player.hitbox)

        for e in self.event_tiles:
            event = e.detect(self.game_map.get_tile(self.player.hitbox.center)) 
            if event != 0:
                data = read_data(event)
                
                self.load_game(data)

        for t in range(len(self.test)):
            new = self.test[t].switch_tile()
            self.game_map.new_map_data(new)
            self.test.pop(t)
               
        self.great_pnj.update(self.player,keys,self.screen,self.camera,self.inventory,self.test,self.game_map.get_map_data())
        for g in self.great_pnj:
            self.screen.blit(g.image,self.camera.apply(g.rect))

        # self.event_tiles.update(self.game_map.get_tile(self.player.hitbox.center),self.game_map)

        self.player.draw_crosshair(self.screen, self.camera)
        self.player.draw_life(self.screen, self.camera)

        print(self.inventory)
        # pygame.draw.rect(screen,'green',camera.apply(player.hitbox),1)

        # event_tiles.update(game_map.get_tile(player.hitbox.center),game_map)
        # events.update(dt)