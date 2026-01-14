import random
from typing import Dict, List, Tuple

Coord = Tuple[int, int]

def _random_grid(n: int, obstacle_prob: float) -> List[List[int]]:
    grid = []
    for _ in range(n):
        row = [1 if random.random() < obstacle_prob else 0 for _ in range(n)]
        grid.append(row)
    return grid

def _pick_free_cell(grid: List[List[int]]) -> Coord:
    n = len(grid)
    while True:
        r = random.randrange(n)
        c = random.randrange(n)
        if grid[r][c] == 0:
            return (r, c)

def generate_random_path_question() -> Dict:
    """
    Generează un grid NxN cu obstacole + start/goal.
    Întrebarea cere cost minim (număr de pași) folosind A* / shortest path.
    """
    n = random.choice([5, 6, 7])
    obstacle_prob = random.choice([0.18, 0.22, 0.25])

    # încercăm de câteva ori să găsim un grid "interesant"
    for _ in range(20):
        grid = _random_grid(n, obstacle_prob)
        start = _pick_free_cell(grid)
        goal = _pick_free_cell(grid)
        if start != goal:
            # asigurăm că start/goal sunt libere
            grid[start[0]][start[1]] = 0
            grid[goal[0]][goal[1]] = 0
            break

    question_text = (
        "Găsește costul minim (număr de pași) de la START la GOAL pe grid (4-direcții). "
        "Obstacolele sunt celulele cu 1. Poți folosi A* (heuristică Manhattan). "
        "Răspunde doar cu un număr (ex: 10) sau scrie 'Nu există drum'."
    )

    return {
        "grid": grid,
        "start": start,
        "goal": goal,
        "question": question_text
    }
