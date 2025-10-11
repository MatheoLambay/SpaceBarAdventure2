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

# --- Fonction pour charger les frames d’un dossier ---
def load_frames(folder_path):
    frames = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".png"):
            frame = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
            frames.append(frame)
    return frames


# --- Initialisation ---
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Jeu avec collisions et scrolling")
clock = pygame.time.Clock()

# --- Charger les frames du joueur ---
frames = load_frames("assets/south")  # 1.png = repos, 2.png+ = marche
player = Player(frames, pos=(14*64, 4*64))
all_sprites = pygame.sprite.Group(player)

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
    [3,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3],
    [3,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3],
    [3,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3],
    [3,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3],
    [3,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3],
    [3,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3],
    [3,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3],
    [3,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3],
    [3, 3,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3, 3],
    [3, 3, 3,-4,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-4,-4,-4, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3,-4,-4,-4,-4,-4,-4,-4,-4, 0, 0, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,-4, 0, 0, 0, 0, 0, 0, 0, 0,-4, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,-4,-4,-4,-4,-4,-4,-4,-4,-4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],

]


tile_size = 64

# créer la map
game_map = Map(map_data, tile_size)

# obstacles pour collisions
obstacles = game_map.get_obstacles()

# --- Caméra ---
map_width = len(map_data[0]) * tile_size
map_height = len(map_data) * tile_size
camera = Camera(map_width, map_height)

buildings = []
b1_matrix = [
    [1,2,2,2],
    [1,2,2,2,2],
    [1,2,2,2]
]
b1 = Building(b1_matrix, tile_size, pos_x=6, pos_y=12)
buildings.append(b1)

# Liste des positions des PNJs sur la matrice
pnj_positions = [(6,3), (8,2), (10,5)]
pnjs = []

for tile_pos in pnj_positions:
    pnjs.append(PNJ("assets/south/1.png", tile_pos, tile_size=64))

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

    all_sprites.update(keys, obstacles, game_map) # Pass game_map
    camera.update(player)

    # --- Rendu ---
    game_map.draw(screen, camera)

    # # dessiner obstacles avec offset caméra
    # for obs,color in obstacles:
    #     pygame.draw.rect(screen, color, camera.apply(obs))

    # dessiner joueur
    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite.rect))
        pygame.draw.rect(screen, (0,255,0), camera.apply(sprite.hitbox), 2)

   
    print(game_map.get_tile(player.hitbox.center)) # Update current_tile)
    

    for pnj in pnjs:
        pnj.update(player)
        screen.blit(pnj.image, camera.apply(pnj.rect))
        pygame.draw.rect(screen, (0,255,0), camera.apply(pnj.rect), 2)

    for b in buildings:
        b.draw(screen, camera, player.hitbox)

    events.update(dt)

    pygame.display.flip()
    

pygame.quit()
