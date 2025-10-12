
# Simple python astar algorithm chasing game. Here enemy chases us and we avoid it.
# Just a test for demo image of gameidea.org a-star post.


import pygame
import heapq
import math
import random


pygame.init()


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
PLAYER_COLOR = (0, 0, 255)  # Blue
ENEMY_COLOR = (255, 0, 0)   # Red
WALL_COLOR = (0, 0, 0)      # Black
BACKGROUND_COLOR = (255, 255, 255)  # White


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Chase with A* Pathfinding")


player_pos = [1, 1]
enemy_pos = [SCREEN_WIDTH // GRID_SIZE - 2, SCREEN_HEIGHT // GRID_SIZE - 2]


directions = {
    pygame.K_w: (0, -1),
    pygame.K_s: (0, 1),
    pygame.K_a: (-1, 0),
    pygame.K_d: (1, 0)
}


walls = [ # test obstacles, for dynamic (moving) obstacles, modify this array on runtime.
    (5, 5), (6, 5), (7, 5), (8, 5), (9, 5),
    (12, 10), (13, 10), (14, 10), (15, 10),
    (3, 8), (4, 8), (5, 8), (6, 8), (7, 8),
    (3, 12), (4, 12), (5, 12), (6, 12), (7, 12),
    (10, 15), (10, 16), (10, 17), (10, 18), (10, 19),
    (15, 15), (15, 16), (15, 17), (15, 18), (15, 19),
]


def draw_game():
    screen.fill(BACKGROUND_COLOR)
    
    # Draw walls
    for wall in walls:
        pygame.draw.rect(screen, WALL_COLOR, (wall[0] * GRID_SIZE, wall[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    # Draw player (blue car)
    pygame.draw.rect(screen, PLAYER_COLOR, (player_pos[0] * GRID_SIZE, player_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    # Draw enemy (red car)
    pygame.draw.rect(screen, ENEMY_COLOR, (enemy_pos[0] * GRID_SIZE, enemy_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    pygame.display.flip()


# A* pathfinding algorithm
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(start, goal, walls):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    cost_so_far = {start: 0}
    
    while open_list:
        current = heapq.heappop(open_list)[1]
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path
        
        for direction in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            
            if (0 <= neighbor[0] < SCREEN_WIDTH // GRID_SIZE and
                0 <= neighbor[1] < SCREEN_HEIGHT // GRID_SIZE and
                neighbor not in walls):
                
                new_cost = cost_so_far[current] + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(goal, neighbor)
                    heapq.heappush(open_list, (priority, neighbor))
                    came_from[neighbor] = current
    return []



def game_loop():
    clock = pygame.time.Clock()
    running = True
    player_speed = 1
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        for key in directions:
            if keys[key]:
                new_pos = [player_pos[0] + directions[key][0], player_pos[1] + directions[key][1]]
                if (0 <= new_pos[0] < SCREEN_WIDTH // GRID_SIZE and
                    0 <= new_pos[1] < SCREEN_HEIGHT // GRID_SIZE and
                    tuple(new_pos) not in walls):
                    player_pos[0] += directions[key][0] * player_speed
                    player_pos[1] += directions[key][1] * player_speed
        
        # Enemy chasing player using A*
        path = a_star(tuple(enemy_pos), tuple(player_pos), walls)
        if path: ## and random.randint(0, 1) == 0:
            enemy_pos[0], enemy_pos[1] = path[0]
        
        draw_game()
        clock.tick(10)




game_loop()
pygame.quit()