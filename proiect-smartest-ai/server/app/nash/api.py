from fastapi import APIRouter
from app.nash.models import NashProblem, SolveResponse, NashEquilibrium, EvaluateRequest
from app.nash.logic import pure_nash_equilibria
from app.nash.question_generator import generate_random_nash_question

router = APIRouter(prefix="/nash", tags=["nash"])

# --- EXISTENT ---
@router.post("/solve", response_model=SolveResponse)
def solve_nash(problem: NashProblem):
    idx = pure_nash_equilibria(problem.p1_payoffs, problem.p2_payoffs)
    equilibria = [
        NashEquilibrium(
            row=r, col=c,
            name=f"({problem.p1_strategies[r]}, {problem.p2_strategies[c]})"
        ) for (r, c) in idx
    ]
    if equilibria:
        return SolveResponse(
            has_equilibrium=True,
            equilibria=equilibria,
            message="Există cel puțin un echilibru Nash pur."
        )
    return SolveResponse(
        has_equilibrium=False,
        equilibria=[],
        message="Nu există echilibru Nash pur."
    )

# --- NOU: GENERARE ÎNTREBARE RANDOM ---
@router.get("/generate")
def generate_question():
    """Generează o întrebare random de tip Nash."""
    question = generate_random_nash_question()
    return {
        "question": question["question_text"],
        "p1_strategies": question["p1_strategies"],
        "p2_strategies": question["p2_strategies"],
        "p1_payoffs": question["p1_payoffs"],
        "p2_payoffs": question["p2_payoffs"]
    }

# --- NOU: EVALUARE RĂSPUNS STUDENT ---
@router.post("/evaluate")
def evaluate_answer(request: EvaluateRequest):
    """
    Primește răspunsul studentului (text) și lista echilibrelor corecte.
    Returnează scorul și feedback-ul.
    """
    student_answer = request.student_answer.strip().lower()
    correct = [eq.lower() for eq in request.correct_equilibria]

    matched = any(eq in student_answer for eq in correct)
    score = 100 if matched else 0
    feedback = (
        "Corect! Ai identificat echilibrul Nash corect."
        if matched
        else "Răspuns incorect. Încearcă să identifici perechea de strategii unde fiecare jucător alege un răspuns optim."
    )

    return {"score": score, "feedback": feedback}
