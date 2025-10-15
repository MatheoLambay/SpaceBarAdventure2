import pygame, heapq

TILE = 64

def tile_blocked(tx, ty, walls, map_w, map_h, size=TILE):
    """Check if a rectangle of size `size` at tile (tx, ty) collides with walls."""
    if tx < 0 or ty < 0 or tx >= map_w or ty >= map_h:
        return True
    r = pygame.Rect(tx*TILE, ty*TILE, size, size)
    for w in walls:
        if r.colliderect(w):
            return True
    return False

def astar(start, goal, walls, map_w, map_h, size=TILE):
    if start == goal:
        return [start]
    open_heap = []
    heapq.heappush(open_heap, (0, start))
    came_from = {}
    gscore = {start: 0}

    def h(a, b):
        dx = abs(a[0] - b[0])
        dy = abs(a[1] - b[1])
        return max(dx, dy)  # Diagonal distance

    while open_heap:
        _, current = heapq.heappop(open_heap)
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        cx, cy = current
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)]:
            nb = (cx + dx, cy + dy)
            if nb[0] < 0 or nb[1] < 0 or nb[0] >= map_w or nb[1] >= map_h:
                continue
            if tile_blocked(nb[0], nb[1], walls, map_w, map_h, size):
                continue
            move_cost = 1.414 if abs(dx)+abs(dy)==2 else 1
            tentative_g = gscore[current] + move_cost
            if nb not in gscore or tentative_g < gscore[nb]:
                came_from[nb] = current
                gscore[nb] = tentative_g
                f = tentative_g + h(nb, goal)
                heapq.heappush(open_heap, (f, nb))
    return None