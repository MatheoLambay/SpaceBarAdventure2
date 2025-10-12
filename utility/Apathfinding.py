import heapq
import pygame
import math

def a_star_move_rect(badguy_rect, player_rect, obstacles, speed):
    """
    Déplacement du Badguy vers le joueur en évitant les obstacles.
    obstacles: liste de pygame.Rect
    Renvoie la nouvelle position (x, y)
    """
    start = (badguy_rect.centerx, badguy_rect.centery)
    goal = (player_rect.centerx, player_rect.centery)

    # Si ligne droite possible, on avance directement
    if line_clear(start, goal, obstacles):
        dx = goal[0] - start[0]
        dy = goal[1] - start[1]
        dist = math.hypot(dx, dy)
        if dist == 0:
            return start
        move_x = speed * dx / dist
        move_y = speed * dy / dist
        return (start[0] + move_x, start[1] + move_y)

    # Sinon A* basé sur pixels ou mini-grille autour du Badguy
    def neighbors(pos):
        x, y = pos
        directions = [(-speed,0),(speed,0),(0,-speed),(0,speed),
                      (-speed,-speed),(-speed,speed),(speed,-speed),(speed,speed)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            rect = badguy_rect.copy()
            rect.center = (nx, ny)
            if not any(rect.colliderect(obs) for obs in obstacles):
                yield (nx, ny), math.hypot(dx, dy)

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start:0}
    f_score = {start:math.hypot(start[0]-goal[0], start[1]-goal[1])}

    while open_set:
        _, current = heapq.heappop(open_set)
        if math.hypot(current[0]-goal[0], current[1]-goal[1]) < speed:
            path = [goal]
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            next_pos = path[1] if len(path) > 1 else path[0]
            return next_pos

        for neighbor, cost in neighbors(current):
            tentative_g = g_score[current] + cost
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + math.hypot(neighbor[0]-goal[0], neighbor[1]-goal[1])
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return start  # pas de chemin trouvé

def line_clear(start, end, obstacles):
    """Vérifie si la ligne droite est libre d'obstacles"""
    x0, y0 = start
    x1, y1 = end
    steps = int(math.hypot(x1-x0, y1-y0))
    if steps == 0:
        return True
    for i in range(1, steps+1):
        xi = x0 + (x1-x0)*i/steps
        yi = y0 + (y1-y0)*i/steps
        rect = pygame.Rect(int(xi), int(yi), 1, 1)
        if any(rect.colliderect(obs) for obs in obstacles):
            return False
    return True
