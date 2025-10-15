import heapq
import math

def a_star(start, goal, game_map):
    """
    Trouve un chemin sur ta map.
    start, goal : tuples (col, row)
    game_map.map_data : ta matrice
    """
    def is_walkable(col, row):
        # On considère les cases négatives comme bloquées
        if 0 <= row < len(game_map.map_data) and 0 <= col < len(game_map.map_data[0]):
            return game_map.map_data[row][col] >= 0
        return False

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # distance manhattan

    open_heap = []
    heapq.heappush(open_heap, (0, start))
    came_from = {start: None}
    gscore = {start: 0}

    while open_heap:
        _, current = heapq.heappop(open_heap)

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = current[0]+dx, current[1]+dy
            if not is_walkable(nx, ny):
                continue

            tentative_g = gscore[current] + 1
            if tentative_g < gscore.get((nx, ny), float('inf')):
                gscore[(nx, ny)] = tentative_g
                fscore = tentative_g + heuristic((nx, ny), goal)
                heapq.heappush(open_heap, (fscore, (nx, ny)))
                came_from[(nx, ny)] = current

    return []  # pas de chemin trouvé
