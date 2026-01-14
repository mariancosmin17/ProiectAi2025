from fastapi import APIRouter
import re
from typing import Dict

from app.path.models import PathProblem, SolveResponse, EvaluateRequest
from app.path.logic import a_star_shortest_path
from app.path.question_generator import generate_random_path_question

router = APIRouter(prefix="/path", tags=["path"])

print("🔥 LOADED app.path.api")


@router.get("/generate", response_model=PathProblem)
def generate_question():
    q = generate_random_path_question()
    return PathProblem(
        grid=q["grid"],
        start=q["start"],
        goal=q["goal"],
        question=q["question"]
    )

@router.post("/solve", response_model=SolveResponse)
def solve_path(problem: PathProblem):
    has_path, cost, path = a_star_shortest_path(problem.grid, tuple(problem.start), tuple(problem.goal))
    if not has_path:
        return SolveResponse(has_path=False, cost=None, path=[], message="Nu există drum valid.")
    return SolveResponse(has_path=True, cost=cost, path=path, message="Drum minim găsit.")

@router.post("/evaluate")
def evaluate_answer(req: EvaluateRequest) -> Dict:
    ans = (req.student_answer or "").strip().lower()

    # Caz: nu există drum
    if not req.has_path or req.correct_cost is None:
        if "nu" in ans:  # "nu exista drum"
            return {"score": 100, "feedback": "Corect – nu există drum valid."}
        return {"score": 0, "feedback": "Incorect – pentru acest grid nu există drum valid."}

    # Extrage primul număr din răspuns
    m = re.search(r"(-?\d+)", ans)
    if not m:
        # bonus mic dacă a încercat
        if "drum" in ans or "path" in ans:
            return {"score": 10, "feedback": "Ai încercat, dar nu ai dat un cost numeric."}
        return {"score": 0, "feedback": "Răspuns invalid. Scrie un număr (cost) sau 'Nu există drum'."}

    val = int(m.group(1))
    correct = int(req.correct_cost)

    if val == correct:
        return {"score": 100, "feedback": "Perfect! Costul minim este corect."}

    # Scor parțial: cu cât e mai aproape, cu atât mai bine (dar nu negativ)
    diff = abs(val - correct)
    score = max(0, 80 - diff * 10)  # ex: diff=1 => 70, diff=2 => 60 ...
    return {
        "score": score,
        "feedback": f"Parțial. Costul corect este {correct}, iar tu ai răspuns {val}."
    }
