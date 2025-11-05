from fastapi import APIRouter
from app.nash.models import NashProblem, SolveResponse, NashEquilibrium
from app.nash.logic import pure_nash_equilibria

router = APIRouter(prefix="/nash", tags=["nash"])

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
