import random
from typing import Dict, List, Tuple

def generate_random_csp(
    num_variables: int = 6,
    domain_size_min: int = 1,
    domain_size_max: int = 3,
    num_constraints: int = 5,
    value_pool: List[str] = None
) -> Tuple[List[str], Dict[str, List[str]], List[List[str]]]: 
    """
    Generează o instanță random de CSP.
    
    Args:
        num_variables:  Numărul de variabile
        domain_size_min:  Mărimea minimă a domeniului
        domain_size_max: Mărimea maximă a domeniului
        num_constraints:  Numărul de constrângeri
        value_pool: Pool-ul de valori posibile (default: ["a", "b", "c", "d"])
    
    Returns:
        (variables, domains, constraints)
    """
    if value_pool is None:
        value_pool = ["a", "b", "c", "d", "e"]
    
    # Generăm variabilele
    variables = [f"V{i+1}" for i in range(num_variables)]
    
    # Generăm domeniile - fiecare variabilă are un domeniu random
    domains = {}
    for var in variables:
        domain_size = random.randint(domain_size_min, min(domain_size_max, len(value_pool)))
        domains[var] = random.sample(value_pool, domain_size)
    
    # Generăm constrângerile - perechi de variabile diferite
    constraints = []
    possible_pairs = [(variables[i], variables[j]) 
                     for i in range(num_variables) 
                     for j in range(i + 1, num_variables)]
    
    # Alegem random constrângeri, dar nu mai multe decât perechile posibile
    num_constraints = min(num_constraints, len(possible_pairs))
    selected_pairs = random.sample(possible_pairs, num_constraints)
    
    for pair in selected_pairs:
        constraints.append(list(pair))
    
    return variables, domains, constraints


def generate_graph_coloring(
    num_nodes: int = 6,
    edge_probability: float = 0.4,
    num_colors: int = 3
) -> Tuple[List[str], Dict[str, List[str]], List[List[str]]]: 
    """
    Generează o problemă de colorare a grafurilor.
    
    Args:
        num_nodes: Numărul de noduri în graf
        edge_probability: Probabilitatea ca două noduri să fie conectate
        num_colors:  Numărul de culori disponibile
    
    Returns:
        (variables, domains, constraints)
    """
    colors = ["rosu", "albastru", "verde", "galben", "portocaliu", "violet", "roz", "maro"]
    colors = colors[: num_colors]
    
    # Variabilele sunt nodurile
    variables = [f"Nod{i+1}" for i in range(num_nodes)]
    
    # Toate nodurile au același domeniu (culorile disponibile)
    domains = {var: colors. copy() for var in variables}
    
    # Generăm muchii random
    constraints = []
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < edge_probability:
                constraints.append([variables[i], variables[j]])
    
    # Asigurăm că graful e conectat (adăugăm un lanț)
    if len(constraints) < num_nodes - 1:
        for i in range(num_nodes - 1):
            pair = [variables[i], variables[i + 1]]
            if pair not in constraints:
                constraints.append(pair)
    
    return variables, domains, constraints


def generate_scheduling_problem(
    num_tasks: int = 5,
    num_time_slots: int = 4
) -> Tuple[List[str], Dict[str, List[int]], List[List[str]]]:
    """
    Generează o problemă de scheduling. 
    
    Args:
        num_tasks: Numărul de task-uri
        num_time_slots: Numărul de slot-uri de timp
    
    Returns:
        (variables, domains, constraints)
    """
    # Variabilele sunt task-urile
    variables = [f"Task{i+1}" for i in range(num_tasks)]
    
    # Fiecare task poate fi programat în diferite slot-uri
    domains = {}
    for var in variables:
        # Unele task-uri au mai puține opțiuni (pentru a face problema interesantă)
        available_slots = random.randint(1, num_time_slots)
        domains[var] = random.sample(range(1, num_time_slots + 1), available_slots)
    
    # Generăm constrângeri:  task-uri care nu pot fi în același timp
    constraints = []
    num_constraints = random.randint(num_tasks - 1, min(num_tasks * 2, num_tasks * (num_tasks - 1) // 2))
    
    possible_pairs = [(variables[i], variables[j]) 
                     for i in range(num_tasks) 
                     for j in range(i + 1, num_tasks)]
    
    selected_pairs = random.sample(possible_pairs, min(num_constraints, len(possible_pairs)))
    
    for pair in selected_pairs:
        constraints.append(list(pair))
    
    return variables, domains, constraints

def is_valid(assignment, constraints):
    """Verifică dacă assignment-ul curent respectă toate constrângerile."""
    for (x, y) in constraints:
        if x in assignment and y in assignment:
            if assignment[x] == assignment[y]: 
                return False
    return True

def backtracking(variables, domains, constraints, assignment=None, steps=0):
    """Backtracking standard - explorează variabilele în ordine."""
    if assignment is None:
        assignment = {}
    
    steps += 1

    # Toate variabilele au fost atribuite
    if len(assignment) == len(variables):
        return assignment. copy(), steps

    # Alege următoarea variabilă neatribuită (în ordine)
    var = None
    for v in variables:
        if v not in assignment:
            var = v
            break

    # Încearcă fiecare valoare din domeniu
    for value in domains[var]:
        assignment[var] = value

        if is_valid(assignment, constraints):
            result, steps = backtracking(variables, domains, constraints, assignment, steps)
            if result is not None:
                return result, steps

        del assignment[var]

    return None, steps


def remaining_values(var, domains, assignment, constraints):
    """Câte valori mai sunt posibile pentru variabilă, ținând cont de ce e deja atribuit."""
    values = []
    for val in domains[var]:
        temp = assignment.copy()
        temp[var] = val
        if is_valid(temp, constraints):
            values. append(val)
    return values


def select_unassigned_var_mrv(variables, domains, assignment, constraints):
    """Alege variabila neatribuită cu cele mai puține valori rămase (MRV)."""
    unassigned = [v for v in variables if v not in assignment]
    
    if not unassigned: 
        return None
    
    best_var = None
    best_count = float('inf')

    for v in unassigned:
        count = len(remaining_values(v, domains, assignment, constraints))
        if count < best_count:
            best_var = v
            best_count = count

    return best_var


def backtracking_mrv(variables, domains, constraints, assignment=None, steps=0):
    """Backtracking cu euristica MRV (Minimum Remaining Values)."""
    if assignment is None:
        assignment = {}

    steps += 1

    # Toate variabilele au fost atribuite
    if len(assignment) == len(variables):
        return assignment.copy(), steps

    # Alegem variabila după MRV, nu după index fix
    var = select_unassigned_var_mrv(variables, domains, assignment, constraints)
    
    if var is None:
        return None, steps

    # Încearcă fiecare valoare din domeniu
    for value in domains[var]:
        assignment[var] = value

        if is_valid(assignment, constraints):
            result, steps = backtracking_mrv(variables, domains, constraints, assignment, steps)
            if result is not None:
                return result, steps

        del assignment[var]

    return None, steps