from fastapi import APIRouter
import re
from typing import Dict

from app.graph.models import GraphProblem, SolveResponse, EvaluateRequest
from app.graph.logic import bfs_shortest_path
from app.graph.question_generator import generate_random_graph_question

router = APIRouter(prefix="/graph", tags=["graph"])

@router.get("/generate", response_model=GraphProblem)
def generate_question():
    q = generate_random_graph_question()
    return GraphProblem(
        graph=q["graph"],
        start=q["start"],
        goal=q["goal"],
        question=q["question"],
    )

@router.post("/solve", response_model=SolveResponse)
def solve_graph(problem: GraphProblem):
    has_path, dist, path = bfs_shortest_path(problem.graph, problem.start, problem.goal)
    if not has_path:
        return SolveResponse(has_path=False, distance=None, path=[], message="Nu există drum valid (BFS).")
    return SolveResponse(has_path=True, distance=dist, path=path, message="Drum minim găsit (BFS).")

@router.post("/evaluate")
def evaluate_answer(req: EvaluateRequest) -> Dict:
    ans = (req.student_answer or "").strip().lower()

    # Caz: nu există drum
    if not req.has_path or req.correct_distance is None:
        if "nu" in ans:  # "nu exista drum"
            return {"score": 100, "feedback": "Corect – nu există drum valid."}
        return {"score": 0, "feedback": "Incorect – pentru acest graf nu există drum valid."}

    # Extrage primul număr din răspuns
    m = re.search(r"(-?\d+)", ans)
    if not m:
        if "drum" in ans or "path" in ans or "bfs" in ans:
            return {"score": 10, "feedback": "Ai încercat, dar nu ai dat o distanță numerică."}
        return {"score": 0, "feedback": "Răspuns invalid. Scrie un număr sau 'Nu există drum'."}

    val = int(m.group(1))
    correct = int(req.correct_distance)

    if val == correct:
        return {"score": 100, "feedback": "Perfect! Distanța minimă (BFS) este corectă."}

    diff = abs(val - correct)
    score = max(0, 80 - diff * 10)
    return {
        "score": score,
        "feedback": f"Parțial. Distanța corectă este {correct}, iar tu ai răspuns {val}."
    }

