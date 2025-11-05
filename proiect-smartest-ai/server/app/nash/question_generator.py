import random
from typing import Dict

def generate_random_nash_question() -> Dict:
    # Exemple de jocuri posibile (matrici de payoff)
    games = [
        {
            "p1_payoffs": [[3, 1], [0, 2]],
            "p2_payoffs": [[3, 0], [1, 2]],
            "p1_strategies": ["Sus", "Jos"],
            "p2_strategies": ["Stânga", "Dreapta"],
            "question_text": "Pentru jocul de mai jos, există echilibru Nash pur?"
        },
        {
            "p1_payoffs": [[2, 0], [3, 1]],
            "p2_payoffs": [[2, 3], [0, 1]],
            "p1_strategies": ["U", "D"],
            "p2_strategies": ["L", "R"],
            "question_text": "Identificați echilibrul Nash (dacă există) pentru jocul următor:"
        },
        {
            "p1_payoffs": [[1, 4], [2, 3]],
            "p2_payoffs": [[3, 2], [1, 4]],
            "p1_strategies": ["A", "B"],
            "p2_strategies": ["X", "Y"],
            "question_text": "Există un echilibru Nash pur pentru acest joc?"
        }
    ]

    chosen = random.choice(games)
    return chosen
