import random
from typing import Dict, List

def generate_random_nash_question() -> Dict:
    # număr de strategii (2x2, 3x3 etc.)
    n = random.choice([2, 3])

    # denumiri posibile pentru strategii
    p1_labels_sets = [
        ["Sus", "Jos"],
        ["U", "D"],
        ["A", "B"],
        ["Rând1", "Rând2"],
        ["X", "Y"]
    ]
    p2_labels_sets = [
        ["Stânga", "Dreapta"],
        ["L", "R"],
        ["X", "Y"],
        ["Col1", "Col2"],
        ["Stg", "Dr"]
    ]

    # alegem seturi de etichete random
    p1_strategies = random.choice(p1_labels_sets)
    p2_strategies = random.choice(p2_labels_sets)

    # dacă jocul e 3x3, completăm etichete extra
    if n == 3:
        p1_strategies += [random.choice(["Mijloc", "C", "M"])]
        p2_strategies += [random.choice(["Centru", "M", "C"])]

    # generează payoff-uri random între 0 și 5
    p1_payoffs = [[random.randint(0, 5) for _ in range(n)] for _ in range(n)]
    p2_payoffs = [[random.randint(0, 5) for _ in range(n)] for _ in range(n)]

    # alegem o formulare de întrebare random
    questions = [
        "Identificați echilibrul Nash (dacă există) pentru jocul următor:",
        "Pentru jocul de mai jos, există echilibru Nash pur?",
        "Care este echilibrul Nash în strategii pure pentru acest joc?",
        "Se poate determina un echilibru Nash pentru următorul joc?",
        "Există o pereche de strategii care formează echilibru Nash?"
    ]
    question_text = random.choice(questions)

    return {
        "p1_payoffs": p1_payoffs,
        "p2_payoffs": p2_payoffs,
        "p1_strategies": p1_strategies,
        "p2_strategies": p2_strategies,
        "question_text": question_text
    }
