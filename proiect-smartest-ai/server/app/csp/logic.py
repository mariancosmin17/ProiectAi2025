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
