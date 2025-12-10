def is_valid(assignment, constraints):
    for (x, y) in constraints:
        if x in assignment and y in assignment:
            if assignment[x] == assignment[y]:
                return False
    return True

def backtracking(variables, domains, constraints, assignment={}, index=0, steps=0):
    steps += 1

    if index == len(variables):
        return assignment, steps

    var = variables[index]

    for value in domains[var]:
        assignment[var] = value

        if is_valid(assignment, constraints):
            result, steps = backtracking(variables, domains, constraints, assignment, index + 1, steps)
            if result:
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
            values.append(val)
    return values

def select_unassigned_var_mrv(variables, domains, assignment, constraints):
    """Alege variabila neatribuită cu cele mai puține valori rămase (MRV)."""
    unassigned = [v for v in variables if v not in assignment]
    best_var = None
    best_count = None

    for v in unassigned:
        count = len(remaining_values(v, domains, assignment, constraints))
        if best_count is None or count < best_count:
            best_var = v
            best_count = count

    return best_var
def backtracking_mrv(variables, domains, constraints, assignment=None, steps=0):
    if assignment is None:
        assignment = {}

    steps += 1

    # toate variabilele au fost atribuite
    if len(assignment) == len(variables):
        return assignment, steps

    # alegem variabila după MRV, nu după index fix
    var = select_unassigned_var_mrv(variables, domains, assignment, constraints)

    for value in domains[var]:
        assignment[var] = value

        if is_valid(assignment, constraints):
            result, steps = backtracking_mrv(variables, domains, constraints, assignment, steps)
            if result:
                return result, steps

        del assignment[var]

    return None, steps
