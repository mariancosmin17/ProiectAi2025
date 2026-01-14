from collections import deque
from typing import Dict, List, Tuple, Optional

def bfs_shortest_path(graph: Dict[str, List[str]], start: str, goal: str) -> Tuple[bool, Optional[int], List[str]]:
    """
    BFS pentru drum minim (număr de muchii).
    Returnează: (has_path, distance, path)
    """
    if start not in graph or goal not in graph:
        return False, None, []

    q = deque([start])
    visited = set([start])
    parent = {start: None}

    while q:
        node = q.popleft()

        if node == goal:
            # reconstruim path
            path = []
            cur = goal
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return True, len(path) - 1, path

        for nei in graph.get(node, []):
            if nei not in visited:
                visited.add(nei)
                parent[nei] = node
                q.append(nei)

    return False, None, []