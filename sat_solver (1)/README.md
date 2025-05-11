# SAT Solver

This is a SAT solver in Python that supports three algorithms:
- **Resolution**
- **Davis–Putnam (DP)**
- **Davis–Putnam–Logemann–Loveland (DPLL)**

## 🔧 Usage

```bash
python main.py [resolution|dp|dpll]
```

The input formula should be in `input.txt` using the following syntax:
- `~A` for NOT A
- `A & B` for A AND B
- `A | B` for A OR B
- `A >> B` for implication (A → B)
- `A == B` for equivalence (A ↔ B)

### Example

**input.txt**
```
(A | B) & (~A | C) & (~B | ~C)
```

Run the solver:
```bash
python main.py dpll
```

## 📁 Files

- `main.py`: Entry point
- `logic_parser.py`: CNF converter
- `resolution.py`: Resolution method
- `dp.py`: Davis–Putnam method
- `dpll.py`: DPLL method
