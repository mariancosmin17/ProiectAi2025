from fastapi import APIRouter
from typing import Dict
from .models import (
    GenerateAlphaBetaRequest,
    AlphaBetaProblem,
    AlphaBetaSolveResponse,
    AlphaBetaEvaluateRequest,
    AlphaBetaEvaluateResponse,
)
from .question_generator import generate_tree
from .logic import alphabeta_minimax

router = APIRouter(prefix="/alphabeta", tags=["alphabeta"])


@router.post("/generate")
def generate_alphabeta(req: GenerateAlphaBetaRequest) -> Dict:
    root = generate_tree(
        depth=req.depth,
        branching=req.branching,
        value_min=req.value_min,
        value_max=req.value_max,
        root_type="MAX",
    )
    return {
        "question": "Pentru arborele de mai jos, care este valoarea din rădăcină și câte frunze sunt vizitate cu MinMax + Alpha-Beta?",
        "root": root.model_dump(),
        "meta": {
            "depth": req.depth,
            "branching": req.branching,
            "value_range": [req.value_min, req.value_max],
        },
    }


@router.post("/solve", response_model=AlphaBetaSolveResponse)
def solve_alphabeta(problem: AlphaBetaProblem):
    root_value, visited_leaves, trace = alphabeta_minimax(problem.root)
    return AlphaBetaSolveResponse(
        root_value=root_value,
        visited_leaves=visited_leaves,
        trace=trace,
        message="Soluție calculată cu MinMax + Alpha-Beta.",
    )


@router.post("/evaluate", response_model=AlphaBetaEvaluateResponse)
def evaluate_alphabeta(req: AlphaBetaEvaluateRequest):
    # Scor simplu:
    # 70% dacă root_value e corect
    # 30% dacă visited_leaves e corect
    score = 0
    parts = []

    if req.student_root_value is not None and req.student_root_value == req.correct_root_value:
        score += 70
        parts.append("Valoarea din rădăcină este corectă.")
    else:
        parts.append("Valoarea din rădăcină este greșită.")

    if req.student_visited_leaves is not None and req.student_visited_leaves == req.correct_visited_leaves:
        score += 30
        parts.append("Numărul de frunze vizitate este corect.")
    else:
        parts.append("Numărul de frunze vizitate este greșit.")

    feedback = " ".join(parts)
    return AlphaBetaEvaluateResponse(score=score, feedback=feedback)
