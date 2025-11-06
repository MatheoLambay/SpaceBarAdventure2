import pygame
import os
import json


def make_blur(surface, intensity=0.18):
    """
    Flou léger, ne passe jamais au noir.
    intensity : <=1 ; plus petit = plus flou (ex: 0.18)
    """
    # Faire une copie pour ne jamais modifier la surface originale
    temp_surf = surface.copy()

    # Extra : convertir en 32-bit pour éviter perte de couleur
    temp_surf = temp_surf.convert_alpha()

    w, h = temp_surf.get_size()
    # protéger contre intensity trop petit ou nul
    small_w, small_h = max(1, int(w * intensity)), max(1, int(h * intensity))

    # Downscale puis upscale
    small = pygame.transform.smoothscale(temp_surf, (small_w, small_h))
    blurred = pygame.transform.smoothscale(small, (w, h))

    return blurred


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

def load_character_sprites(path, tile_size=64, cols=7, rows=4, directions=("S", "N", "E", "W"), scale=None):
    """
    Charge une spritesheet contenant 4x7 (rows x cols) frames.
    Une ligne = une direction dans l'ordre ('S','N','E','W').
    Renvoie un dict {direction: [Surface, ...]} avec chaque frame centrée et copiée.
    - path : chemin vers la spritesheet
    - tile_size : taille d'une frame (ici 64)
    - cols, rows : nombre de colonnes et lignes (7x4 par défaut)
    - scale : facteur (float) ou None pour garder la taille tile_size
    """
    img = pygame.image.load(path).convert_alpha()
    img_w, img_h = img.get_size()
    fw = fh = tile_size

    sprites = {}
    for r in range(rows):
        row_frames = []
        for c in range(cols):
            x = c * fw
            y = r * fh
            if x + fw <= img_w and y + fh <= img_h:
                frame = img.subsurface((x, y, fw, fh)).copy()
                if scale is not None and scale != 1.0:
                    sw = max(1, int(fw * scale))
                    sh = max(1, int(fh * scale))
                    frame = pygame.transform.smoothscale(frame, (sw, sh))
                row_frames.append(frame)
        if r < len(directions):
            sprites[directions[r]] = row_frames

    # assure que chaque direction existe (retourne liste vide si manquante)
    for d in directions:
        sprites.setdefault(d, [])

    return sprites

def read_data(link):
    with open(link,"r", encoding='utf-8') as r:
        return json.load(r)