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
from utility.eventTile import eventTile
from utility.eventChangeTile import eventChangeTile
from classes.bartender import Bartender
from classes.decoObject import decoObj
from classes.interactiveObject.healpad import healPad
from classes.interactiveObject.informations_panel import infoPanel
from classes.interactiveObject.skinSelect import skinSelect
from utility.filesTools import read_data, load_tileset_as_dict, load_frames, load_character_sprites, make_blur





class game_manager:
    def __init__(self,screen):
        self.screen = screen
        self.tile_size = 64

        data = read_data("projectS\data\map1.json")
        
        # frames_south = load_frames("assets/player/animations/walk-1/south")  # 1.png = repos, 2.png+ = marche
        # frames_north = load_frames("assets/player/animations/walk-1/north")
        # frames_east = load_frames("assets/player/animations/walk-1/east")
        # frames_west = load_frames("assets/player/animations/walk-1/west")
        # frames = {"S":frames_south, "N":frames_north, "E":frames_east, "W":frames_west}
        frames_fight_south = load_frames("assets/player/animations/cross-punch/south")
        frames_fight_north = load_frames("assets/player/animations/cross-punch/north")
        frames_fight_east = load_frames("assets/player/animations/cross-punch/east")
        frames_fight_west = load_frames("assets/player/animations/cross-punch/west")
        frames_fight = {"S":frames_fight_south, "N":frames_fight_north, "E":frames_fight_east, "W":frames_fight_west}

       

        x,y = data["player_coord"]
        frames = load_character_sprites("assets/player/animations/walk.png")
        self.player = Player(frames,frames_fight, pos=(x*self.tile_size, y*self.tile_size))
        self.inventory = []
        self.all_sprites = pygame.sprite.Group(self.player)
        
        self.load_game(data)
        #eventChangeTile(-4, 1, data["map_data"])
        self.event_change_tile = []
        self.event_change_map = []

        self.pause_flag = 0
        self.pause = False
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        

        

        # self.event_tiles = pygame.sprite.Group(ev)


    def load_game(self,data):
        self.map_data = data["map_data"]

        nohitbox_tiles = load_tileset_as_dict("assets/map/tilesetSpace.png", 64)
        hitbox_tiles = load_tileset_as_dict("assets/map/tilesetSpaceHitbox.png", 64,False)
        roofs_tiles = load_tileset_as_dict("assets/map/tileset_roof.png", 64)
        textures = {**nohitbox_tiles, **hitbox_tiles}
        x,y = data["player_coord"]

        self.player.set_position((x*self.tile_size-self.tile_size//2,y*self.tile_size-self.tile_size//2))
        self.game_map = Map(self.map_data, self.tile_size,textures)

        # self.events = EventManager(self.player)

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
        self.windrose = ["S","N","E","W"]
        for p in pnj_data:
            temp_dict = {}
            for i in range(len(p["running_path"])):
                temp_dict[self.windrose[i]] = load_frames(p["running_path"][i])
            
            
            self.pnjs.add(PNJ(p["neutral_path"], p["coord"], self.tile_size, p["text"],p["can_attack"],temp_dict,badguy_fight_frames,p["quest_flag"]))
            
        self.decoObj_first_plan = []
        self.decoObj_second_plan = []
        for do in data["decoObject"]:
            if do[0] == "first_plan":
                self.decoObj_first_plan.append(decoObj(do[1],do[2],self.tile_size))
            elif do[0] == "second_plan":
                self.decoObj_second_plan.append(decoObj(do[1],do[2],self.tile_size))

        
        # for tile_pos in pnj_positions:
        #     self.pnjs.append(PNJ("assets/player/animations/walk-1/south/frame_000.png", tile_pos, self.tile_size, str(event_change_tile)))
            

        self.buildings = []
        self.roofs = data["building"]
        for roof in self.roofs:
            self.buildings.append(Building(roof[0],roofs_tiles, self.tile_size, pos_x=roof[1][0], pos_y=roof[1][1]))
        
        self.map_width = len(self.map_data[0]) * self.tile_size
        self.map_height = len(self.map_data) * self.tile_size

        self.camera = Camera(self.map_width, self.map_height, 800, 600)
        self.event_tiles = pygame.sprite.Group()
        for e in data["TPtile"]:
            path = "projectS\data\%s.json"%(e[1])
            ev = eventTile(e[0],path)
            self.event_tiles.add(ev)

        self.obstacles = self.game_map.get_obstacles()


        self.map_objects = pygame.sprite.Group()
        for d in data["object"]:
            if d[0] == "map_indiquateur":
                new_d = infoPanel(d[1],d[2],self.tile_size)
            elif d[0] == "healpad":
                new_d = healPad(d[1],d[2],self.tile_size)
            elif d[0] == "skin_select":
                new_d = skinSelect(d[1],d[2],self.tile_size)
            else:
                break
            self.map_objects.add(new_d)
            self.game_map.add_obstacles(new_d.hitbox)

        self.great_pnj = pygame.sprite.Group()
        for gp in data["greatpnj"]:
          # Conversion des clés en int
            nd = {int(k): v for k, v in gp[0].items()}
            print(gp[2])
            sprt = load_character_sprites(gp[2]) 

            self.great_pnj.add(Bartender(sprt,gp[1],nd))
                

            
    def load_map(self,new_map):
        self.game = new_map
        self.obstacles = self.game_map.get_obstacles()


    def open(self,screen):
        pass

    def update(self,keys,screen,dt):

        if keys[pygame.K_ESCAPE] and self.pause_flag == 0:
            if self.pause:
                self.pause = False
                pygame.event.set_grab(True)
                pygame.mouse.set_visible(False)
            else:
                snapshot = self.screen.copy()
                blurred = make_blur(snapshot, intensity=0.05)
                self.screen.blit(blurred, (0, 0))
                self.pause = True
                pygame.event.set_grab(False)
                pygame.mouse.set_visible(True)
            self.pause_flag = 1
        elif not keys[pygame.K_ESCAPE] and self.pause_flag == 1:
            self.pause_flag = 0

        if self.pause:
            
            return 

        # if keys[pygame.K_b] and self.i ==0 :
        #     print("spawner")
        #     badguy_south = load_frames("assets\pnj\ennemis\scary-walk\south")
        #     badguy_north = load_frames("assets/pnj/ennemis/scary-walk/north")
        #     badguy_east = load_frames("assets/pnj/ennemis/scary-walk/east")
        #     badguy_west = load_frames("assets/pnj/ennemis/scary-walk/west")
        #     badguy_frames = {"S":badguy_south, "N":badguy_north, "E":badguy_east, "W":badguy_west}
        #     badguy_fight_south = load_frames("assets\pnj\ennemis\cross-punch\south")
        #     badguy_fight_north = load_frames("assets/pnj/ennemis/cross-punch/north")
        #     badguy_fight_east = load_frames("assets/pnj/ennemis/cross-punch/east")
        #     badguy_fight_west = load_frames("assets/pnj/ennemis/cross-punch/west")
        #     badguy_fight_frames = {"S":badguy_fight_south, "N":badguy_fight_north, "E":badguy_fight_east, "W":badguy_fight_west}
        #     self.all_ennemis.add(Badguy(badguy_frames,badguy_fight_frames,(14*self.tile_size,16*self.tile_size)))
        #     self.i +=1
            
            
        
        # obstacles = self.game_map.get_obstacles()
    
        self.all_sprites.update(keys, self.obstacles, self.game_map,self.all_ennemis,self.pnjs) # Pass game_map

        
        self.all_ennemis.update(self.player, self.obstacles,self.map_width,self.map_height,self.tile_size)
        
        self.camera.update(self.player)

        # --- Rendu ---
        self.game_map.draw(self.screen, self.camera)

        for do in self.decoObj_second_plan:
            self.screen.blit(do.image,self.camera.apply(do.rect))

        for obj in self.map_objects:
            self.screen.blit(obj.image,self.camera.apply(obj.rect))
            obj.update(self.screen,self.player,keys,self.camera,self.inventory)
        # pygame.draw.rect(self.screen, "blue", self.camera.apply(self.map_indicator.hitbox),1)

        

        # dessiner joueur
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))
            # pygame.draw.rect(self.screen, (255,0,0), self.camera.apply(sprite.hitbox), 1)
            # pygame.draw.rect(self.screen, (0,255,0), self.camera.apply(sprite.foot_hitbox), 1)
            # pygame.draw.rect(self.screen, (0,0,255), self.camera.apply(sprite.rect), 1)
        
        for ennemie in self.all_ennemis:
            # ennemie.update(keys, obstacles, game_map,player)
            self.screen.blit(ennemie.image,self.camera.apply(ennemie.rect))
            pygame.draw.rect(self.screen,'red',self.camera.apply(ennemie.hitbox),1)
        
        # print(game_map.get_tile(player.hitbox.center)) # Update current_tile)
        
        
        self.pnjs.update(self.player,self.screen,self.camera,keys,self.obstacles,self.map_width,self.map_height,self.inventory)
        for p in self.pnjs:
            self.screen.blit(p.image,self.camera.apply(p.rect))
            pygame.draw.rect(self.screen, "blue", self.camera.apply(p.hitbox),1)
        
        
        for g in self.great_pnj:
            self.screen.blit(g.image,self.camera.apply(g.rect))

        for do in self.decoObj_first_plan:
            self.screen.blit(do.image,self.camera.apply(do.rect))
        
        for b in self.buildings:
            b.draw(self.screen, self.camera, self.player.hitbox)

        self.great_pnj.update(self.player,keys,self.screen,self.camera,self.inventory,self.event_change_tile,self.game_map.get_map_data(),dt,self.event_change_map)

        for e in self.event_tiles:
            event = e.update(self.game_map.get_tile(self.player.hitbox.center)) 
            if event != 0:
                data = read_data(event)
                self.load_game(data)

    


        #ici pour les caisses une fois détruite 
        for t in range(len(self.event_change_tile)):
            new = self.event_change_tile[t].switch_tile()
            self.game_map.new_map_data(new)
            self.event_change_tile.pop(t)
            self.obstacles = self.game_map.get_obstacles()
            for ob in self.map_objects:
                self.game_map.add_obstacles(ob.hitbox)
            print("new_obj set !")
        
        for e in self.event_change_map:
            
            data = read_data("projectS\data\%s.json"%(e))
            self.event_change_map.pop(0)
            self.load_game(data)
            
               
        
        # dessiner obstacles avec offset caméra
        # for obs in obstacles:
        #     pygame.draw.rect(self.screen, "red", self.camera.apply(obs),1)

        self.player.draw_crosshair(self.screen, self.camera)
        self.player.draw_life(self.screen, self.camera)
        

        # print(self.inventory)
        # pygame.draw.rect(screen,'green',camera.apply(player.hitbox),1)

        # event_tiles.update(game_map.get_tile(player.hitbox.center),game_map)
        # events.update(dt)