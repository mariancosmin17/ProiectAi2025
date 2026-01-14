from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class GraphProblem(BaseModel):
    graph: Dict[str, List[str]]
    start: str
    goal: str
    question: str

class SolveResponse(BaseModel):
    has_path: bool
    distance: Optional[int] = None
    path: List[str] = Field(default_factory=list)
    message: str

class EvaluateRequest(BaseModel):
    student_answer: str
    correct_distance: Optional[int] = None
    has_path: bool