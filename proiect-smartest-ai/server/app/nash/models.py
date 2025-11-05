from typing import List
from pydantic import BaseModel, Field

class NashProblem(BaseModel):
    p1_payoffs: List[List[int]] = Field(..., example=[[3, 1], [0, 2]])
    p2_payoffs: List[List[int]] = Field(..., example=[[3, 0], [1, 2]])
    p1_strategies: List[str] = Field(..., example=["Sus", "Jos"])
    p2_strategies: List[str] = Field(..., example=["Stânga", "Dreapta"])

class NashEquilibrium(BaseModel):
    row: int
    col: int
    name: str

class SolveResponse(BaseModel):
    has_equilibrium: bool
    equilibria: List[NashEquilibrium]
    message: str
