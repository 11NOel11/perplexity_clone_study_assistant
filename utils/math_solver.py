import sympy as sp

def solve_equation(equation):
    """Solves an algebraic equation."""
    try:
        expr = sp.sympify(equation.replace("=", "- (" ) + ")")
        solution = sp.solve(expr)
        return solution if solution else "No solution found."
    except Exception as e:
        return f"Error solving equation: {e}"
