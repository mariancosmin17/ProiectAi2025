from pydantic import BaseModel
from typing import List, Optional


class SearchProblem(BaseModel):
    """Model pentru o problemă de căutare."""
    problem_name: str  # ex: "N-Queens"
    instance_description: str  # ex: "tablă 8x8"


class SearchSolution(BaseModel):
    """Răspunsul corect pentru o problemă de căutare."""
    problem_name: str
    optimal_strategy: str  # ex: "Backtracking"
    alternative_strategies: List[str]  # strategii acceptabile
    explanation: str  # de ce e optimă


class GenerateQuestionResponse(BaseModel):
    """Răspuns pentru /generate - întrebare generată."""
    question_text: str
    problem_name: str
    instance_description: str
    difficulty: str  # "easy", "medium", "hard"
    options: Optional[List[str]] = None  # opțiuni multiple choice (dacă e easy/medium)


class EvaluateRequest(BaseModel):
    """Request pentru evaluarea unui răspuns student."""
    problem_name: str
    student_answer: str
    instance_description: Optional[str] = None  # Pentru context (opțional)


class EvaluateResponse(BaseModel):
    """Răspuns pentru evaluare."""
    score: int  # 0-100
    feedback: str
    correct_answer: str
    detailed_analysis: Optional[str] = None  # Analiză detaliată (opțional)