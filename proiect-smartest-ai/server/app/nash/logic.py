from typing import List, Tuple

def _best_responses(payoffs: List[List[int]], by_row: bool) -> List[Tuple[int, int]]:
    res: List[Tuple[int, int]] = []
    rows, cols = len(payoffs), len(payoffs[0])
    if by_row:  # Jucătorul 2: max pe rând
        for r in range(rows):
            m = max(payoffs[r])
            for c in range(cols):
                if payoffs[r][c] == m:
                    res.append((r, c))
    else:       # Jucătorul 1: max pe coloană
        for c in range(cols):
            col_vals = [payoffs[r][c] for r in range(rows)]
            m = max(col_vals)
            for r in range(rows):
                if payoffs[r][c] == m:
                    res.append((r, c))
    return res

def pure_nash_equilibria(p1: List[List[int]], p2: List[List[int]]) -> List[Tuple[int, int]]:
    br_p1 = set(_best_responses(p1, by_row=False))
    br_p2 = set(_best_responses(p2, by_row=True))
    return sorted(list(br_p1.intersection(br_p2)))
