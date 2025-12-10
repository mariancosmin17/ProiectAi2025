from pydantic import BaseModel, Field
from typing import Dict, List, Union, Literal

class CSPProblem(BaseModel):
    variables: List[str]
    domains: Dict[str, List[Union[str, int]]]
    constraints: List[List[str]]

class CSPSolution(BaseModel):
    solution: Dict[str, Union[str, int]]
    steps: int
    message:  str

class GenerateCSPRequest(BaseModel):
    problem_type: Literal["random", "graph_coloring", "scheduling"] = Field(
        default="random",
        description="Tipul problemei de generat"
    )
    num_variables: int = Field(default=6, ge=2, le=15, description="Numărul de variabile")
    domain_size_min: int = Field(default=1, ge=1, le=5, description="Mărimea minimă a domeniului")
    domain_size_max: int = Field(default=3, ge=1, le=5, description="Mărimea maximă a domeniului")
    num_constraints: int = Field(default=5, ge=1, le=50, description="Numărul de constrângeri")
    num_colors: int = Field(default=3, ge=2, le=8, description="Numărul de culori (pentru graph coloring)")
    edge_probability: float = Field(default=0.4, ge=0.1, le=0.9, description="Probabilitatea muchiilor")
    num_time_slots: int = Field(default=4, ge=2, le=10, description="Numărul de time slots (pentru scheduling)")