from pydantic import BaseModel
from typing import Dict, List

class CSPProblem(BaseModel):
    variables: List[str]
    domains: Dict[str, List[str]]
    constraints: List[List[str]]  # ex: [["X1", "X2"], ["X2", "X3"]]

class CSPSolution(BaseModel):
    solution: Dict[str, str]
    steps: int
    message: str
