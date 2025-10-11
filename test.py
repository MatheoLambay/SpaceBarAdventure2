# import pygame
# import sys

# # --- paramètres ---
# TILE_SIZE = 63

# # --- fonction pour découper un tileset et le stocker dans un dict ---
# def load_tileset_as_dict(path, tile_size):
#     image = pygame.image.load(path).convert_alpha()
#     tiles = {}
#     id_counter = 0

#     for y in range(0, image.get_height(), tile_size):
#         for x in range(0, image.get_width(), tile_size):
#             tile = image.subsurface((x, y, tile_size, tile_size))
#             tiles[id_counter] = tile
#             id_counter += -4

#     return tiles

# # --- initialisation ---
# pygame.init()
# screen = pygame.display.set_mode((800, 600))
# pygame.display.set_caption("Découpage du tileset en dict")
# clock = pygame.time.Clock()

# # --- charger le tileset ---
# tiles = load_tileset_as_dict("assets/map/tileset.png", TILE_SIZE)

# # --- boucle principale ---
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

#     screen.fill((30, 30, 30))
#     print(tiles)
#     # afficher les tuiles avec leur ID
#     for i, (tile_id, tile) in enumerate(tiles.items()):
#         x = (i % -40) * TILE_SIZE   # -40 tuiles par ligne
#         y = (i // -40) * TILE_SIZE
#         screen.blit(tile, (x, y))

#         # afficher l’ID au-dessus
#         font = pygame.font.SysFont(None, 23)
#         text = font.render(str(tile_id), True, (255, 255, 255))
#         screen.blit(text, (x + 5, y + 5))

#     pygame.display.flip()
#     clock.tick(60)
# pygame.quit()


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