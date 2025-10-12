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

# --- Fonction pour charger les frames d’un dossier ---
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


# --- Initialisation ---
pygame.init()
pygame.mouse.set_visible(False) 
pygame.event.set_grab(True)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Jeu avec collisions et scrolling")
clock = pygame.time.Clock()

# --- Charger les frames du joueur ---
frames_south = load_frames("assets/player/animations/walk-1/south")  # 1.png = repos, 2.png+ = marche
frames_north = load_frames("assets/player/animations/walk-1/north")
frames_east = load_frames("assets/player/animations/walk-1/east")
frames_west = load_frames("assets/player/animations/walk-1/west")
frames = {"S":frames_south, "N":frames_north, "E":frames_east, "W":frames_west}

player = Player(frames, pos=(14*64, 4*64))
badguy = Badguy(pos=(14*64, 6*64))

all_ennemis = pygame.sprite.Group(badguy)
all_sprites = pygame.sprite.Group(player)

pause = False

# --- Obstacles (Rectangles) ---

# 
map_data = [
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
    [3,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0,-22, 1, 1, 1, 1, 1,-24, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3],
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

pygame.event.set_grab(True)

tile_size = 64

# créer la map
game_map = Map(map_data, tile_size,textures)

# obstacles pour collisions
obstacles,obstacles_coord = game_map.get_obstacles()

# --- Caméra ---
map_width = len(map_data[0]) * tile_size
map_height = len(map_data) * tile_size
camera = Camera(map_width, map_height, 800, 600)

buildings = []
b1_matrix = [
    [0,1,1,1,1,1,2],
    [10,11,11,11,11,11,12],
    [10,11,11,11,11,11,12],
    [10,11,11,11,11,11,12],
    [10,11,11,11,11,11,12],
    [10,11,11,11,11,11,12],
    [20,21,21,21,21,21,22] 
]

b1 = Building(b1_matrix,roofs_tiles, tile_size, pos_x=11, pos_y=9)
buildings.append(b1)

# Liste des positions des PNJs sur la matrice
pnj_positions = [(12,10), (15,10), (6,6)]
pnjs = []
test=1
for tile_pos in pnj_positions:

    pnjs.append(PNJ("assets/player/animations/walk-1/south/frame_000.png", tile_pos, tile_size, str(test)))
    test+=1

#event manager
events = EventManager(player)

# Exemple de script d’event : avancer → attendre → animation → retour contrôle
cutscene_script = [
    MoveEvent(player, 1, 0, 200),   # avancer de 200px vers la droite
    WaitEvent(3000),                 # attendre 0.5s
    MoveEvent(player, 0, 1, 200),   # avancer de 200px vers la droite
    WaitEvent(3000), 
    MoveEvent(player, 0, -1, 100),
]

# --- Boucle principale ---
running = True

while running:
    dt = clock.tick(60)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # touche espace pour lancer la cutscene
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not events.active:
                
                events.start_event(cutscene_script.copy())

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if pause:
                pause = False
                pygame.event.set_grab(True)
                pygame.mouse.set_visible(False)
            else:
                pause = True
                pygame.event.set_grab(False)
                pygame.mouse.set_visible(True)
        # and not pause:
        #     pause = True
        #     pygame.event.set_grab(False)
        #     pygame.mouse.set_visible(True)
        


        

    all_sprites.update(keys, obstacles, game_map,all_ennemis) # Pass game_map

    
    all_ennemis.update(player.rect, obstacles)
    
    camera.update(player)

    # --- Rendu ---
    game_map.draw(screen, camera)

    # # dessiner obstacles avec offset caméra
    # for obs,color in obstacles:
    #     pygame.draw.rect(screen, color, camera.apply(obs))

    # dessiner joueur
    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite.rect))
        # pygame.draw.rect(screen, (0,255,0), camera.apply(sprite.hitbox), 2)
    
    for ennemie in all_ennemis:
        # ennemie.update(keys, obstacles, game_map,player)
        screen.blit(ennemie.image,camera.apply(ennemie.rect))
        pygame.draw.rect(screen, (0,255,0), camera.apply(ennemie.hitbox), 2)

   
    # print(game_map.get_tile(player.hitbox.center)) # Update current_tile)
    

    for pnj in pnjs:
        pnj.update(player,screen,camera,keys)
        screen.blit(pnj.image, camera.apply(pnj.rect))
       

    for b in buildings:
        b.draw(screen, camera, player.hitbox)

    player.draw_crosshair(screen, camera)

    events.update(dt)

    

    pygame.display.flip()
    
    if not pause:
            # --- Empêche la souris de sortir de la fenêtre ---
        mx, my = pygame.mouse.get_pos()
        sw, sh = screen.get_size()

        # On bloque la position si elle dépasse les bords
        if mx < 0: mx = 0
        if mx > sw: mx = sw
        if my < 0: my = 0
        if my > sh: my = sh

        pygame.mouse.set_pos((mx, my))


pygame.quit()
