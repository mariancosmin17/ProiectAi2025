import random
from typing import Dict, List

def _make_nodes(n: int) -> List[str]:
    # A, B, C, ...
    return [chr(ord("A") + i) for i in range(n)]

def _add_edge(g: Dict[str, List[str]], u: str, v: str, directed: bool):
    if v not in g[u]:
        g[u].append(v)
    if not directed:
        if u not in g[v]:
            g[v].append(u)

def generate_random_graph_question() -> Dict:
    """
    Generează un graf mic (6..10 noduri), orientat sau neorientat,
    cu start/goal random.
    """
    n = random.randint(6, 10)
    directed = random.random() < 0.35  # 35% orientat
    nodes = _make_nodes(n)

    g: Dict[str, List[str]] = {v: [] for v in nodes}

    # asigurăm un "spine" ca să nu fie complet rupt (mai ales la neorientat)
    for i in range(n - 1):
        _add_edge(g, nodes[i], nodes[i + 1], directed)

    # adăugăm muchii random
    extra_edges = random.randint(n, n * 2)
    for _ in range(extra_edges):
        u = random.choice(nodes)
        v = random.choice(nodes)
        if u == v:
            continue
        _add_edge(g, u, v, directed)

    # sortăm vecinii ca BFS să fie determinist (important pentru drum/path)
    for k in g:
        g[k] = sorted(set(g[k]))

    start, goal = random.sample(nodes, 2)

    question_text = (
        "Găsește distanța minimă (număr de muchii) de la START la GOAL folosind BFS.\n"
        f"Graf {'ORIENTAT' if directed else 'NEORIENTAT'}.\n"
        "Răspunde doar cu un număr (ex: 3) sau scrie 'Nu există drum'."
    )

    return {
        "graph": g,
        "start": start,
        "goal": goal,
        "question": question_text,
        "directed": directed,
    }