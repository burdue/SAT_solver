def resolution_solver(clauses):
    print("Initial clauses:")
    for i, c in enumerate(clauses):
        print(f"  C{i+1}: {c}")
    print()

    new = []
    clauses = [set(clause) for clause in clauses]
    step = 1
    pairs_tried = set()

    while True:
        n = len(clauses)
        for i in range(n):
            for j in range(i + 1, n):
                ci, cj = clauses[i], clauses[j]
                resolvents = resolve(ci, cj)

                for resolvent in resolvents:
                    # Avoid repeating same resolutions
                    key = frozenset((frozenset(ci), frozenset(cj), frozenset(resolvent)))
                    if key in pairs_tried:
                        continue
                    pairs_tried.add(key)

                    print(f"Step {step}: Resolve {ci} and {cj} → {resolvent}")
                    step += 1

                    if not resolvent:
                        print("Derived empty clause. UNSATISFIABLE.")
                        return False

                    if resolvent not in clauses and resolvent not in new:
                        new.append(resolvent)

        if all(res not in clauses for res in new):
            print("No new clauses. SATISFIABLE (no contradiction found).")
            return True

        clauses.extend(new)
        new.clear()


def resolve(ci, cj):
    resolvents = []
    for lit in ci:
        neg = negate_literal(lit)
        if neg in cj:
            new_clause = (ci - {lit}) | (cj - {neg})
            resolvents.append(new_clause)
    return resolvents


def negate_literal(lit):
    return lit[1:] if lit.startswith("~") else "~" + lit
