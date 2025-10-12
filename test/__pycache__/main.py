import pygame
from player import Player
from enemy import Enemy
from pathfinding import TILE

pygame.init()

# --- Map setup ---
MAP_W, MAP_H = 15, 10
SCREEN_W, SCREEN_H = MAP_W * TILE, MAP_H * TILE
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()

# --- Walls ---
walls = []
internal_wall_tiles = [
    (4,2),(4,3),(4,4),(4,5),
    (7,0),(7,1),(7,2),(7,3),(7,4),
    (10,5),(11,5),(12,5),(13,5),
    (2,7),(3,7),(4,7),(5,7)
]
for tx, ty in internal_wall_tiles:
    walls.append(pygame.Rect(tx*TILE, ty*TILE, TILE, TILE))

# --- Player and Enemy ---
player = Player(TILE, TILE, 4.0, walls)
enemy = Enemy((MAP_W-2)*TILE, (MAP_H-2)*TILE, 3.0, walls, MAP_W, MAP_H)

# --- Game loop ---
running = True
while running:
    dt = clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    # --- Player input ---
    player.handle_input()

    # --- Enemy update ---
    enemy.update(player.rect.center)

    # --- Drawing ---
    screen.fill((30,30,30))
    for w in walls:
        pygame.draw.rect(screen, (200,200,200), w)
    pygame.draw.rect(screen, (50,150,255), player.rect)
    pygame.draw.rect(screen, (220,60,60), enemy.rect)

    pygame.display.flip()

pygame.quit()
