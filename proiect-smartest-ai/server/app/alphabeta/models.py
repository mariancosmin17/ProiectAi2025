from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Union


NodeType = Literal["MAX", "MIN"]

class TreeNode(BaseModel):
    # Nod intern
    type: Optional[NodeType] = None
    children: Optional[List["TreeNode"]] = None

    # Frunză
    value: Optional[int] = None

TreeNode.model_rebuild()


class GenerateAlphaBetaRequest(BaseModel):
    depth: int = Field(default=3, ge=2, le=5, description="Adâncimea arborelui (niveluri de decizie).")
    branching: int = Field(default=2, ge=2, le=4, description="Număr copii per nod.")
    value_min: int = Field(default=0, ge=-50, le=50)
    value_max: int = Field(default=15, ge=-50, le=50)


class AlphaBetaProblem(BaseModel):
    root: TreeNode


class AlphaBetaSolveResponse(BaseModel):
    root_value: int
    visited_leaves: int
    trace: List[str]
    message: str


class AlphaBetaEvaluateRequest(BaseModel):
    # răspunsuri student (varianta A)
    student_root_value: Optional[int] = None
    student_visited_leaves: Optional[int] = None

    # adevărul calculat (trimis din frontend)
    correct_root_value: int
    correct_visited_leaves: int


class AlphaBetaEvaluateResponse(BaseModel):
    score: int
    feedback: str
