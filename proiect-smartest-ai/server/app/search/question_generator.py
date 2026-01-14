import random
from typing import Dict, List

PROBLEMS = [
    {
        "name": "N-Queens",
        "instances": [
            "tablă 4x4",
            "tablă 8x8",
            "tablă 12x12",
            "tablă de dimensiune N generică"
        ]
    },
    {
        "name": "Hanoi",
        "instances": [
            "3 discuri și 3 tijuri",
            "5 discuri și 4 tijuri",
            "n discuri și k tijuri (k ≥ 3)",
            "4 discuri și 3 tijuri"
        ]
    },
    {
        "name": "Graph Coloring",
        "instances": [
            "graf cu 5 noduri și 7 muchii",
            "graf complet K₅",
            "graf bipartit K₃,₃",
            "graf cu 10 noduri și 15 muchii"
        ]
    },
    {
        "name": "Knight's Tour",
        "instances": [
            "tablă de șah 8x8",
            "tablă 5x5",
            "tablă dreptunghiulară 6x8",
            "tablă de dimensiune m×n"
        ]
    }
]

QUESTION_TEMPLATES = [
    "Pentru problema {problem} pe {instance}, care este cea mai potrivită strategie de rezolvare dintre următoarele? ",
    "Dat fiind {problem} cu {instance}, ce strategie de căutare este optimă?",
    "Care strategie recomandați pentru rezolvarea problemei {problem} în cazul {instance}?",
    "În contextul problemei {problem} ({instance}), care este algoritmul cel mai eficient?",
    "Identificați strategia optimă pentru {problem} având {instance}.",
]

ALL_STRATEGIES = [
    "BFS (Breadth-First Search)",
    "DFS (Depth-First Search)",
    "Backtracking",
    "Backtracking cu Forward Checking",
    "A* (A-star)",
    "Hill Climbing",
    "Iterative Deepening",
    "UCS (Uniform Cost Search)",
    "Greedy Best-First Search",
    "Backtracking cu MRV",
]


def generate_random_question(difficulty: str = None) -> Dict:
    """
    Generează o întrebare aleatoare despre strategii de căutare.

    difficulty: "easy", "medium", "hard", sau None (alege random)
    """
    if difficulty is None:
        difficulty = random.choice(["easy", "medium", "hard"])

    # Alege problemă și instanță
    problem_data = random.choice(PROBLEMS)
    problem_name = problem_data["name"]
    instance = random.choice(problem_data["instances"])

    # Alege template pentru întrebare
    template = random.choice(QUESTION_TEMPLATES)
    question_text = template.format(problem=problem_name, instance=instance)

    # Generează opțiuni în funcție de dificultate
    options = None

    if difficulty == "easy":
        # 3 opțiuni
        options = _generate_options(problem_name, num_options=3)
        question_text += f"\n\nOpțiuni:\n" + "\n".join([f"{chr(65 + i)}. {opt}" for i, opt in enumerate(options)])

    elif difficulty == "medium":
        # 5 opțiuni
        options = _generate_options(problem_name, num_options=5)
        question_text += f"\n\nOpțiuni:\n" + "\n".join([f"{chr(65 + i)}. {opt}" for i, opt in enumerate(options)])

    elif difficulty == "hard":
        # 7 opțiuni + cerință de explicație
        options = _generate_options(problem_name, num_options=7)
        question_text += f"\n\nOpțiuni:\n" + "\n".join([f"{chr(65 + i)}. {opt}" for i, opt in enumerate(options)])
        question_text += "\n\n**Bonus:** Explicați pe scurt de ce ați ales această strategie."

    return {
        "question_text": question_text,
        "problem_name": problem_name,
        "instance_description": instance,
        "difficulty": difficulty,
        "options": options,
    }


def _generate_options(problem_name: str, num_options: int) -> List[str]:
    """Generează opțiuni pentru întrebare, incluzând răspunsul corect."""
    from .logic import SEARCH_KNOWLEDGE

    if problem_name not in SEARCH_KNOWLEDGE:
        return random.sample(ALL_STRATEGIES, min(num_options, len(ALL_STRATEGIES)))

    correct = SEARCH_KNOWLEDGE[problem_name]["optimal"]
    acceptable = SEARCH_KNOWLEDGE[problem_name]["acceptable"]

    # Includem strategia corectă
    options = [correct]

    # Adăugăm alte strategii acceptabile (dacă există)
    for alt in acceptable:
        if alt != correct and len(options) < num_options:
            options.append(alt)

    # Completăm cu strategii random
    remaining = [s for s in ALL_STRATEGIES if s not in options]
    while len(options) < num_options and remaining:
        options.append(remaining.pop(random.randint(0, len(remaining) - 1)))

    # Amestecăm ordinea
    random.shuffle(options)

    return options