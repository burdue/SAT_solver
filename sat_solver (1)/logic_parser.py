import ast

class Expr: pass

class Var(Expr):
    def __init__(self, name): self.name = name
    def __repr__(self): return self.name

class Not(Expr):
    def __init__(self, operand): self.operand = operand
    def __repr__(self): return f"~{self.operand}"

class And(Expr):
    def __init__(self, left, right): self.left = left; self.right = right
    def __repr__(self): return f"({self.left} & {self.right})"

class Or(Expr):
    def __init__(self, left, right): self.left = left; self.right = right
    def __repr__(self): return f"({self.left} | {self.right})"

def parse_expr(expr_str):
    def transform(node):
        if isinstance(node, ast.Name): return Var(node.id)
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Invert): return Not(transform(node.operand))
        elif isinstance(node, ast.BinOp):
            left = transform(node.left)
            right = transform(node.right)
            if isinstance(node.op, ast.BitAnd): return And(left, right)
            if isinstance(node.op, ast.BitOr): return Or(left, right)
            if isinstance(node.op, ast.RShift): return Or(Not(left), right)
            if isinstance(node.op, ast.Eq): return And(Or(Not(left), right), Or(Not(right), left))
        raise ValueError("Unsupported expression")
    return transform(ast.parse(expr_str, mode='eval').body)

def eliminate_iff(expr):
    if isinstance(expr, And): return And(eliminate_iff(expr.left), eliminate_iff(expr.right))
    if isinstance(expr, Or): return Or(eliminate_iff(expr.left), eliminate_iff(expr.right))
    if isinstance(expr, Not): return Not(eliminate_iff(expr.operand))
    return expr

def push_not(expr):
    if isinstance(expr, Not):
        inner = expr.operand
        if isinstance(inner, Not): return push_not(inner.operand)
        if isinstance(inner, And): return Or(push_not(Not(inner.left)), push_not(Not(inner.right)))
        if isinstance(inner, Or): return And(push_not(Not(inner.left)), push_not(Not(inner.right)))
        return Not(push_not(inner))
    if isinstance(expr, And): return And(push_not(expr.left), push_not(expr.right))
    if isinstance(expr, Or): return Or(push_not(expr.left), push_not(expr.right))
    return expr

def distribute(expr):
    if isinstance(expr, And): return And(distribute(expr.left), distribute(expr.right))
    if isinstance(expr, Or):
        A, B = distribute(expr.left), distribute(expr.right)
        if isinstance(A, And): return And(distribute(Or(A.left, B)), distribute(Or(A.right, B)))
        if isinstance(B, And): return And(distribute(Or(A, B.left)), distribute(Or(A, B.right)))
        return Or(A, B)
    return expr

def to_cnf(expr):
    expr = eliminate_iff(expr)
    expr = push_not(expr)
    expr = distribute(expr)
    return expr

def flatten(expr):
    def collect_or(e):
        return collect_or(e.left) + collect_or(e.right) if isinstance(e, Or) else [e]
    def collect_and(e):
        return collect_and(e.left) + collect_and(e.right) if isinstance(e, And) else [e]
    return [frozenset(str(lit) for lit in collect_or(c)) for c in collect_and(expr)]
