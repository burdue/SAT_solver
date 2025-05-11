from dp import dp_solver
from dpll import dpll_solver
from resolution import resolution_solver

def main():
    print("Welcome to the SAT Solver (Step-by-Step Version)!")
    print("--------------------------------------------------")
    
    # You can change this input or load from a file
    # Example CNF: (A ∨ ~B) ∧ (~A ∨ B ∨ C) ∧ (~C)
    clauses = [
        ["A", "~B"],
        ["~A", "B", "C"],
        ["~C"]
    ]
    
    print("CNF to be solved:")
    for clause in clauses:
        print("  ", " ∨ ".join(clause))
    print()

    print("Choose SAT solving method:")
    print("1. DPLL (step-by-step)")
    print("2. Davis-Putnam (DP) (step-by-step)")
    print("3. Resolution (step-by-step)")
    choice = input("Enter your choice (1/2/3): ")

    if choice == "1":
        print("\nRunning DPLL Solver...\n")
        result = dpll_solver(clauses)
        print("\nFinal Result:", "SATISFIABLE" if result else "UNSATISFIABLE")

    elif choice == "2":
        print("\nRunning Davis-Putnam Solver...\n")
        result = dp_solver(clauses)
        print("\nFinal Result:", "SATISFIABLE" if result else "UNSATISFIABLE")

    elif choice == "3":
        print("\nRunning Resolution Solver...\n")
        result = resolution_solver(clauses)
        print("\nFinal Result:", "SATISFIABLE" if result else "UNSATISFIABLE")

    else:
        print("Invalid choice. Please run the program again.")

if __name__ == "__main__":
    main()

