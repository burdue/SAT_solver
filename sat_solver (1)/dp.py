def dp_solver(clauses):
    clauses = [set(clause) for clause in clauses]
    step = 0

    print("\nInitial CNF clauses:")
    for c in clauses:
        print("  ", " ∨ ".join(sorted(c)))
    print()

    def eliminate(clauses, var):
        nonlocal step
        pos = set()
        neg = set()
        others = []

        for clause in clauses:
            if var in clause:
                pos.add(frozenset(clause))
            elif f"~{var}" in clause:
                neg.add(frozenset(clause))
            else:
                others.append(clause)

        if not pos or not neg:
            # No resolution needed
            return clauses

        resolvents = []
        for c1 in pos:
            for c2 in neg:
                step += 1
                r = (set(c1) - {var}) | (set(c2) - {f"~{var}"})
                print(f"Step {step}: Resolve {sorted(c1)} and {sorted(c2)} → {sorted(r)}")
                if not r:
                    print("Derived empty clause: UNSATISFIABLE")
                    return None
                resolvents.append(r)

        new_clauses = others + resolvents
        print(f"After eliminating variable '{var}', new clause set:")
        for c in new_clauses:
            print("  ", " ∨ ".join(sorted(c)))
        print()
        return new_clauses

    # Get all variables
    vars = set()
    for clause in clauses:
        for literal in clause:
            var = literal.lstrip("~")
            vars.add(var)

    for var in sorted(vars):
        clauses = eliminate(clauses, var)
        if clauses is None:
            return False

    print("No empty clause derived: SATISFIABLE")
    return True
