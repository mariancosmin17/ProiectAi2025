from fastapi import APIRouter, Query
from typing import Optional

from .models import (
    SearchProblem,
    SearchSolution,
    GenerateQuestionResponse,
    EvaluateRequest,
    EvaluateResponse,
)
from .logic import get_optimal_strategy, evaluate_answer
from .question_generator import generate_random_question

router = APIRouter(prefix="/search", tags=["search"])


# -------------------------------------------------
# /generate - Generează întrebare aleatoare
# -------------------------------------------------

@router.get("/generate", response_model=GenerateQuestionResponse)
def generate_question(
        difficulty: Optional[str] = Query(None, description="easy, medium, sau hard")
):
    """
    Generează o întrebare aleatoare despre strategii de căutare.

    - **difficulty**: "easy" (3 opțiuni), "medium" (5 opțiuni), "hard" (7 opțiuni + explicație)
    """
    question_data = generate_random_question(difficulty)

    return GenerateQuestionResponse(
        question_text=question_data["question_text"],
        problem_name=question_data["problem_name"],
        instance_description=question_data["instance_description"],
        difficulty=question_data["difficulty"],
        options=question_data.get("options"),
    )


# -------------------------------------------------
# /solve - Returnează soluția optimă
# -------------------------------------------------

@router.post("/solve", response_model=SearchSolution)
def solve_search_problem(problem: SearchProblem):
    """
    Returnează strategia optimă pentru o problemă de căutare dată.

    - **problem_name**: ex.  "N-Queens", "Hanoi", "Graph Coloring", "Knight's Tour"
    """
    result = get_optimal_strategy(problem.problem_name)

    return SearchSolution(
        problem_name=problem.problem_name,
        optimal_strategy=result["optimal_strategy"],
        alternative_strategies=result["alternative_strategies"],
        explanation=result["explanation"],
    )


# -------------------------------------------------
# /evaluate - Evaluează răspunsul studentului
# -------------------------------------------------

@router.post("/evaluate", response_model=EvaluateResponse)
def evaluate_student_answer(request: EvaluateRequest):
    """
    Evaluează răspunsul unui student la o întrebare despre strategii de căutare.

    Scorare îmbunătățită:
    - 100%: Răspuns corect
    - 50-70%: Strategie suboptimală dar validă (+ bonus pentru explicație)
    - 20-30%:  Răspuns greșit cu cuvinte cheie relevante
    - 10%: Strategie nepotrivită identificată
    - 0%: Răspuns complet greșit

    Bonus:  +10-20% pentru explicații detaliate cu concepte relevante
    """
    result = evaluate_answer(
        request.problem_name,
        request.student_answer,
        request.instance_description
    )

    return EvaluateResponse(
        score=result["score"],
        feedback=result["feedback"],
        correct_answer=result["correct_answer"],
        detailed_analysis=result.get("detailed_analysis"),
    )