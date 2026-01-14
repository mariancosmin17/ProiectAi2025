from typing import List, Tuple, Optional
from pydantic import BaseModel, Field

Coord = Tuple[int, int]

class PathProblem(BaseModel):
    grid: List[List[int]] = Field(..., description="0=liber, 1=obstacol")
    start: Coord
    goal: Coord
    question: str

class SolveResponse(BaseModel):
    has_path: bool
    cost: Optional[int] = None
    path: List[Coord] = []
    message: str

class EvaluateRequest(BaseModel):
    student_answer: str
    correct_cost: Optional[int] = None   # None dacă nu există drum
    has_path: bool
