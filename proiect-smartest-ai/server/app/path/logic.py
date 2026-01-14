from typing import List, Tuple, Dict, Optional
import heapq

Coord = Tuple[int, int]

def manhattan(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def in_bounds(grid: List[List[int]], r: int, c: int) -> bool:
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])

def neighbors(grid: List[List[int]], node: Coord):
    r, c = node
    for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
        nr, nc = r + dr, c + dc
        if in_bounds(grid, nr, nc) and grid[nr][nc] == 0:
            yield (nr, nc)

def reconstruct(came_from: Dict[Coord, Coord], cur: Coord) -> List[Coord]:
    path = [cur]
    while cur in came_from:
        cur = came_from[cur]
        path.append(cur)
    path.reverse()
    return path

def a_star_shortest_path(grid, start, goal):
    """
    Returnează: (has_path: bool, cost: Optional[int], path: list[tuple[int,int]])
    grid: matrice 0/1 (1 = obstacol)
    start/goal: (r, c)
    """
    rows, cols = len(grid), len(grid[0])

    def in_bounds(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def passable(r, c):
        return grid[r][c] == 0

    def h(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan

    sr, sc = start
    gr, gc = goal
    if not in_bounds(sr, sc) or not in_bounds(gr, gc) or not passable(sr, sc) or not passable(gr, gc):
        return False, None, []

    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    gscore = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            # reconstruim path
            path = []
            cur = current
            while cur is not None:
                path.append(cur)
                cur = came_from[cur]
            path.reverse()
            return True, gscore[current], path

        r, c = current
        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
            nr, nc = r + dr, c + dc
            nxt = (nr, nc)
            if not in_bounds(nr, nc) or not passable(nr, nc):
                continue
            tentative = gscore[current] + 1
            if nxt not in gscore or tentative < gscore[nxt]:
                gscore[nxt] = tentative
                priority = tentative + h(nxt, goal)
                heapq.heappush(frontier, (priority, nxt))
                came_from[nxt] = current

    return False, None, []
