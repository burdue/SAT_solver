def dpll_solver(clauses, assignment=None, depth=0, step=[0]):
    if assignment is None:
        assignment = {}

    indent = "  " * depth

    def print_step(message):
        step[0] += 1
        print(f"{indent}Step {step[0]}: {message}")

    # Base case: check if all clauses are satisfied
    if not clauses:
        print_step("All clauses satisfied. SATISFIABLE.")
        return True

    # Check for empty clause (conflict)
    for clause in clauses:
        if not clause:
            print_step("Empty clause found. Conflict! UNSATISFIABLE.")
            return False

    # Unit propagation
    unit_clauses = [c for c in clauses if len(c) == 1]
    if unit_clauses:
        for unit in unit_clauses:
            lit = next(iter(unit))
            var = lit.lstrip("~")
            val = not lit.startswith("~")
            if var in assignment:
                if assignment[var] != val:
                    print_step(f"Conflict in unit propagation: {var} already assigned to {assignment[var]}")
                    return False
            else:
                print_step(f"Unit propagation: {var} = {val}")
                assignment[var] = val
                new_clauses = simplify(clauses, var, val)
                return dpll_solver(new_clauses, assignment, depth + 1, step)

    # Pure literal elimination
    all_literals = [lit for clause in clauses for lit in clause]
    literals_set = set(all_literals)
    pure_literals = []
    for lit in literals_set:
        neg = "~" + lit if not lit.startswith("~") else lit[1:]
        if neg not in literals_set:
            pure_literals.append(lit)

    if pure_literals:
        for lit in pure_literals:
            var = lit.lstrip("~")
            val = not lit.startswith("~")
            if var in assignment and assignment[var] != val:
                print_step(f"Conflict in pure literal: {var} already assigned to {assignment[var]}")
                return False
            print_step(f"Pure literal elimination: {var} = {val}")
            assignment[var] = val
            new_clauses = simplify(clauses, var, val)
            return dpll_solver(new_clauses, assignment, depth + 1, step)

    # Choose first unassigned variable to branch on
    for clause in clauses:
        for lit in clause:
            var = lit.lstrip("~")
            if var not in assignment:
                # Try True
                print_step(f"Branching: try {var} = True")
                new_assignment = assignment.copy()
                new_assignment[var] = True
                if dpll_solver(simplify(clauses, var, True), new_assignment, depth + 1, step):
                    return True
                # Try False
                print_step(f"Backtracking: try {var} = False")
                new_assignment[var] = False
                if dpll_solver(simplify(clauses, var, False), new_assignment, depth + 1, step):
                    return True
                print_step(f"Backtracking failed for both True and False on {var}")
                return False

    print_step("No variables left to assign. UNSATISFIABLE.")
    return False


def simplify(clauses, var, value):
    new_clauses = []
    for clause in clauses:
        new_clause = []
        skip_clause = False
        for lit in clause:
            v = lit.lstrip("~")
            is_neg = lit.startswith("~")
            if v == var:
                if value != is_neg:
                    skip_clause = True  # clause is satisfied
                    break
                else:
                    continue  # remove this literal from clause
            else:
                new_clause.append(lit)
        if not skip_clause:
            new_clauses.append(new_clause)
    return new_clauses
