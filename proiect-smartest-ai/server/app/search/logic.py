from typing import Dict, List, Optional, Tuple
import re

# Baza de cunoștințe - ÎMBUNĂTĂȚITĂ
SEARCH_KNOWLEDGE = {
    "N-Queens": {
        "optimal": "Backtracking cu Forward Checking",
        "very_good": ["Backtracking cu Forward Checking", "Backtracking cu constrângeri"],
        "acceptable": ["Backtracking"],
        "suboptimal": ["DFS", "Depth-First Search"],
        "wrong": ["BFS", "Breadth-First Search", "A*", "Hill Climbing", "Greedy"],
        "explanation": "N-Queens este o problemă de satisfacere a constrângerilor (CSP). "
                       "Backtracking cu Forward Checking este optim deoarece elimină valorile invalide "
                       "din domenii înainte de a încerca următoarea atribuire, reducând dramatic spațiul de căutare.",
        "keywords": ["constrângeri", "csp", "revenire", "pruning", "forward checking"],
    },
    "Hanoi": {
        "optimal": "DFS",
        "very_good": ["DFS", "Depth-First Search"],
        "acceptable": ["Iterative Deepening"],
        "suboptimal": ["BFS", "Breadth-First Search"],
        "wrong": ["A*", "Hill Climbing", "Backtracking", "Greedy"],
        "explanation": "Turnurile Hanoi au o soluție recursivă naturală, iar DFS urmează "
                       "exact acest pattern. Iterative Deepening poate fi folosit pentru soluții optime "
                       "cu memorie limitată.",
        "keywords": ["recursiv", "stivă", "adâncime", "memorie limitată"],
    },
    "Graph Coloring": {
        "optimal": "Backtracking cu MRV",
        "very_good": ["Backtracking cu MRV", "Backtracking cu Forward Checking"],
        "acceptable": ["Backtracking"],
        "suboptimal": ["DFS", "Depth-First Search", "Greedy"],
        "wrong": ["BFS", "Breadth-First Search", "A*", "UCS", "Hill Climbing"],
        "explanation": "Graph Coloring este CSP.  Backtracking cu MRV (Minimum Remaining Values) "
                       "este optim deoarece alege întâi variabilele cu cele mai puține opțiuni rămase, "
                       "detectând rapid situațiile fără soluție și reducând dramatic spațiul de căutare.",
        "keywords": ["constrângeri", "csp", "mrv", "euristică", "minimum remaining values"],
    },
    "Knight's Tour": {
        "optimal": "Backtracking cu Warnsdorff",
        "very_good": ["Backtracking cu Warnsdorff", "Backtracking cu euristică", "Backtracking cu heuristic"],
        "acceptable": ["Backtracking"],
        "suboptimal": ["DFS", "Depth-First Search"],
        "wrong": ["BFS", "Breadth-First Search", "A*", "Hill Climbing", "Greedy", "UCS"],
        "explanation": "Knight's Tour necesită explorarea exhaustivă cu revenire.  "
                       "Backtracking cu heuristica Warnsdorff (alegerea mutării către poziția cu cele mai puține opțiuni) "
                       "reduce dramatic timpul de căutare de la ore la secunde.",
        "keywords": ["warnsdorff", "euristică", "exhaustiv", "revenire", "heuristic"],
    },
}


def get_optimal_strategy(problem_name: str) -> Dict:
    """Returnează strategia optimă pentru o problemă dată."""
    if problem_name not in SEARCH_KNOWLEDGE:
        raise ValueError(f"Problemă necunoscută: {problem_name}")

    data = SEARCH_KNOWLEDGE[problem_name]
    return {
        "optimal_strategy": data["optimal"],
        "alternative_strategies": data.get("very_good", []) + data.get("acceptable", []),
        "explanation": data["explanation"],
    }


def normalize_answer(answer: str) -> str:
    """Normalizează răspunsul (lowercase, fără diacritice, spații comprimate)."""
    import unicodedata
    answer = ''.join(
        c for c in unicodedata.normalize('NFD', answer)
        if unicodedata.category(c) != 'Mn'
    )
    answer = re.sub(r'\s+', ' ', answer.lower().strip())
    return answer


def calculate_match_score(student_answer: str, target_strategy: str) -> Tuple[int, str]:
    """
    Calculează cât de bine match-uiește răspunsul cu strategia țintă.

    Returns:
        (score, match_type) unde:
        - score: 0-100
        - match_type: "exact", "complete", "partial", "incomplete", "none"
    """
    student_norm = normalize_answer(student_answer)
    target_norm = normalize_answer(target_strategy)

    # Match exact (identic)
    if student_norm == target_norm:
        return (100, "exact")

    # Extragem componentele strategiei țintă
    target_words = set(target_norm.split())
    student_words = set(student_norm.split())

    # Ignorăm cuvinte comune neimportante
    filler_words = {"cu", "cu", "si", "sau", "pentru", "de", "la"}
    target_words = target_words - filler_words
    student_words = student_words - filler_words

    if not target_words:
        return (0, "none")

    # Calculăm overlap-ul
    common_words = target_words.intersection(student_words)
    coverage = len(common_words) / len(target_words)

    # Match complet (toate cuvintele importante din target sunt în student)
    if coverage == 1.0:
        return (100, "complete")

    # Match parțial bun (>= 50% cuvinte)
    if coverage >= 0.5:
        score = int(80 * coverage)
        return (score, "partial")

    # Match slab (< 50% cuvinte)
    if coverage > 0:
        score = int(50 * coverage)
        return (score, "incomplete")

    # Fără match
    return (0, "none")


def find_best_match(student_answer: str, strategy_list: List[str]) -> Tuple[int, str, str]:
    """
    Găsește cel mai bun match din lista de strategii.

    Returns:
        (best_score, best_strategy, match_type)
    """
    best_score = 0
    best_strategy = ""
    best_match_type = "none"

    for strategy in strategy_list:
        score, match_type = calculate_match_score(student_answer, strategy)
        if score > best_score:
            best_score = score
            best_strategy = strategy
            best_match_type = match_type

    return (best_score, best_strategy, best_match_type)


def contains_explanation_keywords(text: str, keywords: List[str]) -> int:
    """Numără câte cuvinte cheie din explicație apar în text."""
    text_norm = normalize_answer(text)
    count = 0
    for kw in keywords:
        if normalize_answer(kw) in text_norm:
            count += 1
    return count


def evaluate_answer(
        problem_name: str,
        student_answer: str,
        instance_description: Optional[str] = None
) -> Dict:
    """
    Evaluează răspunsul studentului cu sistem STRICT de punctaj.

    Scorare:
    - Match exact cu optimal (100%): 100%
    - Match complet cu optimal (toate cuvintele): 100%
    - Match exact cu acceptable:  85%
    - Match complet cu acceptable: 85%
    - Match parțial bun cu optimal (>=70%): 70-90%
    - Match parțial cu acceptable (>=70%): 60-75%
    - Match slab cu optimal (50-69%): 50-69%
    - Match cu suboptimal:  40-50%
    - Match cu wrong: 10%
    - Fără match clar: 0-30%
    """
    if problem_name not in SEARCH_KNOWLEDGE:
        return {
            "score": 0,
            "feedback": "Problemă necunoscută.",
            "correct_answer": "N/A",
            "detailed_analysis": None,
        }

    data = SEARCH_KNOWLEDGE[problem_name]

    optimal = data["optimal"]
    very_good = data.get("very_good", [])
    acceptable = data.get("acceptable", [])
    suboptimal = data.get("suboptimal", [])
    wrong = data.get("wrong", [])
    keywords = data.get("keywords", [])
    explanation = data["explanation"]

    context = f" pentru {instance_description}" if instance_description else ""

    has_explanation = len(student_answer.strip()) > 20
    keyword_count = contains_explanation_keywords(student_answer, keywords)

    # Găsim cel mai bun match pentru fiecare categorie
    optimal_score, optimal_match, optimal_type = find_best_match(student_answer, very_good)
    acceptable_score, acceptable_match, acceptable_type = find_best_match(student_answer, acceptable)
    suboptimal_score, suboptimal_match, suboptimal_type = find_best_match(student_answer, suboptimal)
    wrong_score, wrong_match, wrong_type = find_best_match(student_answer, wrong)

    # === DECIZIE PE BAZA SCORURILOR ===

    # CAZ 1: Match PERFECT cu optimal (exact sau complet)
    if optimal_score == 100 and optimal_type in ["exact", "complete"]:
        base_score = 100

        if has_explanation and keyword_count >= 2:
            feedback = (
                f"🎉 Perfect!  {optimal} este strategia optimă pentru {problem_name}{context}. "
                f"Ai oferit și o explicație excelentă!\n\n"
                f"📚 {explanation}"
            )
            detailed_analysis = f"Răspuns optimal cu explicație completă ({keyword_count} concepte relevante)."
        else:
            feedback = (
                f"✅ Excelent! {optimal} este strategia optimă pentru {problem_name}{context}.\n\n"
                f"📚 {explanation}"
            )
            detailed_analysis = "Răspuns optimal identificat corect."

        return {
            "score": base_score,
            "feedback": feedback,
            "correct_answer": optimal,
            "detailed_analysis": detailed_analysis,
        }

    # CAZ 2: Match PARȚIAL BUN cu optimal (70-99%)
    if optimal_score >= 70 and optimal_score < 100:
        base_score = optimal_score

        feedback = (
            f"✅ Foarte aproape!  Ai identificat direcția corectă pentru {problem_name}{context}.\n\n"
            f"💡 Răspunsul optim complet este:  **{optimal}**\n"
            f"Tu ai scris: \"{student_answer.strip()}\"\n\n"
            f"📚 {explanation}"
        )
        detailed_analysis = f"Răspuns parțial corect ({optimal_score}% match cu strategia optimă)."

        return {
            "score": base_score,
            "feedback": feedback,
            "correct_answer": optimal,
            "detailed_analysis": detailed_analysis,
        }

    # CAZ 3: Match PERFECT cu acceptable (85%)
    if acceptable_score == 100 and acceptable_type in ["exact", "complete"]:
        base_score = 85

        feedback = (
            f"✅ Corect!  Ai identificat strategia de bază corectă pentru {problem_name}{context}.\n\n"
            f"💡 Totuși, {optimal} ar fi mult mai eficient!  "
            f"Optimizările reduc dramatic timpul de execuție.\n\n"
            f"📚 {explanation}"
        )
        detailed_analysis = f"Răspuns corect dar neoptimizat.  Strategia optimă este {optimal}."

        return {
            "score": base_score,
            "feedback": feedback,
            "correct_answer": optimal,
            "detailed_analysis": detailed_analysis,
        }

    # CAZ 4: Match PARȚIAL cu acceptable (60-75%)
    if acceptable_score >= 70 and acceptable_score < 100:
        base_score = min(75, acceptable_score)

        feedback = (
            f"⚠️ Aproape corect pentru categoria acceptabilă, dar incomplet.\n\n"
            f"💡 Răspunsul de bază acceptabil ar fi: **{acceptable_match}**\n"
            f"Răspunsul optim este: **{optimal}**\n\n"
            f"📚 {explanation}"
        )
        detailed_analysis = f"Răspuns parțial - {acceptable_score}% match cu varianta acceptabilă."

        return {
            "score": base_score,
            "feedback": feedback,
            "correct_answer": optimal,
            "detailed_analysis": detailed_analysis,
        }

    # CAZ 5: Match SLAB cu optimal (50-69%)
    if optimal_score >= 50 and optimal_score < 70:
        base_score = optimal_score

        feedback = (
            f"⚠️ Răspuns incomplet.  Ai menționat elemente corecte dar lipsesc detalii importante.\n\n"
            f"💡 Răspunsul complet optim este: **{optimal}**\n"
            f"Tu ai scris: \"{student_answer.strip()}\"\n\n"
            f"📚 {explanation}"
        )
        detailed_analysis = f"Răspuns incomplet ({optimal_score}% din strategia optimă)."

        return {
            "score": base_score,
            "feedback": feedback,
            "correct_answer": optimal,
            "detailed_analysis": detailed_analysis,
        }

    # CAZ 6: Match cu SUBOPTIMAL
    if suboptimal_score >= 70:
        base_score = 45

        if has_explanation and keyword_count >= 2:
            base_score = 55

        feedback = (
            f"⚠️ Parțial corect.  Strategia ta ({suboptimal_match}) poate funcționa teoretic, "
            f"dar {optimal} este mult mai eficient pentru {problem_name}{context}.\n\n"
            f"📚 {explanation}"
        )
        detailed_analysis = "Strategie suboptimală - funcționează dar ineficient."

        return {
            "score": base_score,
            "feedback": feedback,
            "correct_answer": optimal,
            "detailed_analysis": detailed_analysis,
        }

    # CAZ 7: Match cu WRONG
    if wrong_score >= 70:
        score = 10
        feedback = (
            f"❌ Răspuns incorect. Strategia menționată ({wrong_match}) nu este potrivită pentru {problem_name}{context}.\n\n"
            f"💡 Strategia optimă este: **{optimal}**\n\n"
            f"📚 {explanation}"
        )
        detailed_analysis = "Strategie nepotrivită pentru această problemă."

        return {
            "score": score,
            "feedback": feedback,
            "correct_answer": optimal,
            "detailed_analysis": detailed_analysis,
        }

    # CAZ 8: Răspuns cu cuvinte cheie relevante (dar fără strategie clară)
    if keyword_count >= 2:
        score = 30
        feedback = (
            f"❌ Răspuns incomplet. Ai menționat concepte relevante ({keyword_count} termeni corecți), "
            f"dar nu ai identificat strategia specifică.\n\n"
            f"💡 Strategia optimă pentru {problem_name}{context} este: **{optimal}**\n\n"
            f"📚 {explanation}"
        )
        detailed_analysis = f"Răspuns vag cu {keyword_count} concepte relevante, dar fără strategie clară."

        return {
            "score": score,
            "feedback": feedback,
            "correct_answer": optimal,
            "detailed_analysis": detailed_analysis,
        }

    # CAZ 9: Răspuns foarte vag
    general_keywords = ["cautare", "algoritm", "strategie", "search", "rezolv", "metoda"]
    if any(kw in normalize_answer(student_answer) for kw in general_keywords):
        score = 20
        feedback = (
            f"❓ Răspuns prea vag. Trebuie să identifici o strategie SPECIFICĂ.\n\n"
            f"💡 Pentru {problem_name}{context}, strategia optimă este: **{optimal}**\n\n"
            f"📚 {explanation}"
        )
        detailed_analysis = "Răspuns foarte vag fără strategie identificabilă."

        return {
            "score": score,
            "feedback": feedback,
            "correct_answer": optimal,
            "detailed_analysis": detailed_analysis,
        }

    # CAZ 10: Complet greșit sau total neidentificabil
    feedback = (
        f"❌ Răspuns incorect sau neidentificabil.\n\n"
        f"💡 Pentru {problem_name}{context}, strategia optimă este: **{optimal}**\n\n"
        f"📚 {explanation}"
    )
    detailed_analysis = "Răspuns complet greșit sau imposibil de interpretat."

    return {
        "score": 0,
        "feedback": feedback,
        "correct_answer": optimal,
        "detailed_analysis": detailed_analysis,
    }