# app/nash/api.py

from fastapi import APIRouter
from typing import List, Dict, Tuple
import re
import unicodedata

from app.nash.models import (
    NashProblem,
    SolveResponse,
    NashEquilibrium,
    EvaluateRequest,
)
from app.nash.logic import pure_nash_equilibria
from app.nash.question_generator import generate_random_nash_question

router = APIRouter(prefix="/nash", tags=["nash"])

# -------------------------------------------------
# Helpers
# -------------------------------------------------

def _strip_accents(s: str) -> str:
    """Scoate diacriticele (ăâîșț -> aaiste)."""
    return "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )


def _norm(s: str) -> str:
    """Normalizează: fără diacritice, lowercase, spații comprimate."""
    s = _strip_accents(s).lower()
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _extract_labels_from_equilibria(correct_equilibria: List[str]) -> List[str]:
    """
    Din ["(Sus, Stânga)", "(Jos, Dreapta)"] scoate ["Sus", "Stânga", "Jos", "Dreapta"].
    Folosim asta doar pentru bonusul de 10% (a folosit etichete din tabel).
    """
    labels: set[str] = set()
    for eq in correct_equilibria:
        m = re.search(r"\((.*?)\)", eq)
        if not m:
            continue
        for part in m.group(1).split(","):
            p = part.strip()
            if p:
                labels.add(p)
    return list(labels)


def _parse_pairs(text: str) -> List[Tuple[str, str]]:
    """
    Extrage toate perechile (a, b) din răspunsul studentului și le normalizează.

    Exemplu:
        text = "Sunt două: (Sus, Stânga) și (Jos, Dreapta)"
        => [("sus", "stanga"), ("jos", "dreapta")]
    """
    pairs: List[Tuple[str, str]] = []

    # căutăm TOATE parantezele din răspunsul studentului
    for m in re.finditer(r"\(([^()]*)\)", text):
        inside = m.group(1)
        parts = [p.strip() for p in inside.split(",")]
        if len(parts) != 2:
            continue
        a, b = parts
        if a and b:
            pairs.append((_norm(a), _norm(b)))
    return pairs


def _norm_eq_list(correct_equilibria: List[str]) -> List[Tuple[str, str]]:
    """
    Normalizează echilibrele corecte în perechi (lhs, rhs) deja normalizate.

    ["(Sus, Stânga)"] -> [("sus", "stanga")]
    """
    norm: List[Tuple[str, str]] = []
    for eq in correct_equilibria:
        m = re.search(r"\((.*?)\)", eq)
        if not m:
            continue
        parts = [p.strip() for p in m.group(1).split(",")]
        if len(parts) != 2:
            continue
        norm.append((_norm(parts[0]), _norm(parts[1])))
    return norm


def _count_matched_pairs(answer: str, correct_equilibria: List[str]) -> int:
    """
    Numără câte perechi corecte apar în răspunsul studentului.

    - perechile pot fi în orice ordine
    - comparația se face pe string normalizat
    """
    ans_pairs = set(_parse_pairs(answer))
    corr_pairs = set(_norm_eq_list(correct_equilibria))
    return len(ans_pairs.intersection(corr_pairs))


# -------------------------------------------------
# /solve
# -------------------------------------------------

@router.post("/solve", response_model=SolveResponse)
def solve_nash(problem: NashProblem):
    idx = pure_nash_equilibria(problem.p1_payoffs, problem.p2_payoffs)
    equilibria = [
        NashEquilibrium(
            row=r,
            col=c,
            name=f"({problem.p1_strategies[r]}, {problem.p2_strategies[c]})",
        )
        for (r, c) in idx
    ]

    if equilibria:
        return SolveResponse(
            has_equilibrium=True,
            equilibria=equilibria,
            message="Există cel puțin un echilibru Nash pur.",
        )

    return SolveResponse(
        has_equilibrium=False,
        equilibria=[],
        message="Nu există echilibru Nash pur.",
    )


# -------------------------------------------------
# /generate
# -------------------------------------------------

@router.get("/generate")
def generate_question():
    q = generate_random_nash_question()
    return {
        "question": q["question_text"],
        "p1_strategies": q["p1_strategies"],
        "p2_strategies": q["p2_strategies"],
        "p1_payoffs": q["p1_payoffs"],
        "p2_payoffs": q["p2_payoffs"],
    }


# -------------------------------------------------
# /evaluate
# -------------------------------------------------

@router.post("/evaluate")
def evaluate_answer(request: EvaluateRequest) -> Dict:
    """
    Scorare:
      - dacă NU există NE pur și răspunsul conține 'nu' -> 100%
      - dacă există N echilibre și răspunsul conține k dintre ele -> round(100*k/N)
      - dacă k = 0 dar răspunsul conține etichete din tabel -> 10%
      - altfel -> 0%
    """
    answer_raw = request.student_answer or ""
    answer_norm = _norm(answer_raw)
    correct_eq = request.correct_equilibria or []
    total = len(correct_eq)

    # 1) NU există echilibru Nash pur
    if total == 0:
        if "nu" in answer_norm:
            return {
                "score": 100,
                "feedback": "Corect – pentru acest joc nu există echilibru Nash pur.",
            }
        return {
            "score": 0,
            "feedback": "Răspuns incorect. Pentru acest joc nu există echilibru Nash pur.",
        }

    # 2) Există unul sau mai multe NE – numărăm perechile corecte
    matched = _count_matched_pairs(answer_raw, correct_eq)

    if matched > 0:
        score = round(100 * matched / total)
        if score == 100:
            fb = "Perfect! Ai identificat toate echilibrele Nash."
        elif matched == 1 and total > 1:
            fb = f"Parțial corect – ai identificat 1 din {total} echilibre Nash."
        else:
            fb = f"Parțial corect – ai identificat {matched} din {total} echilibre Nash."
        return {"score": score, "feedback": fb}

    # 3) Nu a nimerit niciun NE, dar a folosit etichete corecte din tabel -> 10%
    labels = _extract_labels_from_equilibria(correct_eq)
    labels_norm = [_norm(l) for l in labels]
    if any(l in answer_norm for l in labels_norm):
        return {
            "score": 10,
            "feedback": "Ai folosit etichete din tabel, dar nu ai indicat un echilibru corect.",
        }

    # 4) Complet greșit
    return {
        "score": 0,
        "feedback": "Răspuns incorect. Încearcă să identifici perechile unde ambii jucători au răspunsuri optime.",
    }
