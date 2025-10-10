import pygame
import os
from classes.player import Player
from classes.camera import Camera
from classes.map import Map
from classes.pnj import PNJ
from classes.building import Building

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
player = Player(frames, pos=(100, 100))
all_sprites = pygame.sprite.Group(player)

# --- Obstacles (Rectangles) ---
obstacles = [
    
]

map_data = [
    [1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,2,2,0,0,0,0,1,1,1],
    [1,0,0,3,3,0,0,0,0,1,1,1],
    [1,0,0,2,2,0,0,0,0,1,1,1],
    [1,1,1,1,1,1,1,0,1,1,1,1],
    [1,1,1,0,0,0,0,0,1,1,1,1],
    [1,1,1,0,0,0,1,0,1,1,1,1],
    [1,1,1,0,0,0,1,1,1,1,1,1],
    [1,1,1,0,0,0,1,1,1,1,1,1],
    [1,1,1,0,4,0,1,1,1,1,1,1],
    [1,1,1,0,0,0,1,1,1,1,1,1],
    [1,1,1,0,0,0,1,1,1,1,1,1],
    [1,1,1,0,0,0,1,1,1,1,1,1],
    [1,1,1,0,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,1,1,1],
    [1,1,1,1,0,1,1,1,1,1,1,1],
]
tile_size = 64

# créer la map
game_map = Map(map_data, tile_size)

# obstacles pour collisions
obstacles = game_map.get_obstacles()

# --- Caméra ---
map_width = 1600
map_height = 1200
camera = Camera(map_width, map_height)

buildings = []
b1_matrix = [
    [2,2,2],
    [2,2,2,2],
    [2,2,2]
]
b1 = Building(b1_matrix, tile_size, pos_x=6, pos_y=12)
buildings.append(b1)

# Liste des positions des PNJs sur la matrice
pnj_positions = [(6,3), (8,2), (10,5)]
pnjs = []

for tile_pos in pnj_positions:
    pnjs.append(PNJ("assets/south/1.png", tile_pos, tile_size=64))

# Boucle principale


# --- Boucle principale ---
running = True
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update(keys, obstacles, game_map) # Pass game_map
    camera.update(player)

    # --- Rendu ---
    game_map.draw(screen, camera)

    # # dessiner obstacles avec offset caméra
    # for obs in obstacles:
    #     pygame.draw.rect(screen, (200, 0, 0), camera.apply(obs))

    # dessiner joueur
    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite.rect))
        pygame.draw.rect(screen, (0,255,0), camera.apply(sprite.hitbox), 2)

   

    

    for pnj in pnjs:
        pnj.update(player)
        screen.blit(pnj.image, camera.apply(pnj.rect))
        pygame.draw.rect(screen, (0,255,0), camera.apply(pnj.rect), 2)

    for b in buildings:
        b.draw(screen, camera, player.hitbox)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
