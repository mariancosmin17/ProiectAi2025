from fastapi import APIRouter
from . models import CSPProblem, CSPSolution, GenerateCSPRequest
from . logic import (
    backtracking, 
    backtracking_mrv, 
    generate_random_csp,
    generate_graph_coloring,
    generate_scheduling_problem
)

router = APIRouter(prefix="/csp", tags=["csp"])

@router.post("/solve", response_model=CSPSolution)
def solve_csp(problem: CSPProblem):
    """Rezolvă CSP folosind backtracking standard."""
    solution, steps = backtracking(
        problem.variables, 
        problem.domains, 
        problem.constraints
    )

    if not solution: 
        return CSPSolution(
            solution={}, 
            steps=steps, 
            message="Nu există soluție validă."
        )

    return CSPSolution(
        solution=solution, 
        steps=steps, 
        message="Soluție găsită."
    )


@router.post("/solve-mrv", response_model=CSPSolution)
def solve_csp_mrv(problem: CSPProblem):
    """Rezolvă CSP folosind backtracking cu euristica MRV."""
    solution, steps = backtracking_mrv(
        problem.variables, 
        problem.domains, 
        problem.constraints
    )

    if not solution:
        return CSPSolution(
            solution={}, 
            steps=steps, 
            message="Nu există soluție validă (MRV)."
        )

    return CSPSolution(
        solution=solution, 
        steps=steps, 
        message="Soluție găsită cu MRV."
    )


@router.post("/generate", response_model=CSPProblem)
def generate_csp(request: GenerateCSPRequest):
    """Generează o instanță random de CSP."""
    
    if request.problem_type == "graph_coloring":
        variables, domains, constraints = generate_graph_coloring(
            num_nodes=request.num_variables,
            edge_probability=request.edge_probability,
            num_colors=request.num_colors
        )
    elif request.problem_type == "scheduling": 
        variables, domains, constraints = generate_scheduling_problem(
            num_tasks=request.num_variables,
            num_time_slots=request.num_time_slots
        )
    else:  # random
        variables, domains, constraints = generate_random_csp(
            num_variables=request.num_variables,
            domain_size_min=request.domain_size_min,
            domain_size_max=request.domain_size_max,
            num_constraints=request.num_constraints
        )
    
    return CSPProblem(
        variables=variables,
        domains=domains,
        constraints=constraints
    )