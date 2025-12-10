from fastapi import APIRouter
from .models import CSPProblem, CSPSolution
from .logic import backtracking, backtracking_mrv

router = APIRouter(prefix="/csp", tags=["csp"])

@router.post("/solve", response_model=CSPSolution)
def solve_csp(problem: CSPProblem):
    solution, steps = backtracking(problem.variables, problem.domains, problem.constraints)

    if not solution:
        return CSPSolution(solution={}, steps=steps, message="Nu există soluție validă.")

    return CSPSolution(solution=solution, steps=steps, message="Soluție găsită.")
@router.post("/solve-mrv", response_model=CSPSolution)
def solve_csp_mrv(problem: CSPProblem):
    solution, steps = backtracking_mrv(problem.variables, problem.domains, problem.constraints)

    if not solution:
        return CSPSolution(solution={}, steps=steps, message="Nu există soluție validă (MRV).")

    return CSPSolution(solution=solution, steps=steps, message="Soluție găsită cu MRV.")
