# SAT solver to search for 3-negator circuit
# a hand-rewritten solution is in check-3-circuit.py

from pysat.formula import *
from pysat.solvers import Solver


vpool = IDPool()


# Общий вид выражения, которое можно составить из or и and
def varcomb(vars: list[Formula], names: list[str], prefix: str):
    terms: list[Formula] = []

    for mask in range(1, 2 ** len(vars)):
        term = Atom(compose_name(prefix, names, mask))

        for i, var in enumerate(vars):
            if mask >> i & 1:
                term &= var
        terms.append(term)

    return Or(*terms)


def compose_name(prefix: str, names: list[str], mask: int):
    return f"{prefix}({' '.join([n for i, n in enumerate(names) if mask >> i & 1])})"


# xi = PYSAT_TRUE/PYSAT_FALSE
def comp(x1: Formula, x2: Formula, x3: Formula):
    # circuit is DAG, therefore we can topologically sort its components, and it has the following form

    # first not gate can only take an expression of x1,x2,x3 as input
    v1 = Neg(varcomb([x1, x2, x3], ["x1", "x2", "x3"], "v1"))

    # second not gate can take an expression of x1,x2,x3,v1
    v2 = Neg(varcomb([x1, x2, x3, v1], ["x1", "x2", "x3", "v1"], "v2"))

    # trird - expression of x1,x2,x3,v1,v2
    out1 = varcomb([x1, x2, x3, v1, v2], ["x1", "x2", "x3", "v1", "v2"], "out1")
    out2 = varcomb([x1, x2, x3, v1, v2], ["x1", "x2", "x3", "v1", "v2"], "out2")
    out3 = varcomb([x1, x2, x3, v1, v2], ["x1", "x2", "x3", "v1", "v2"], "out3")

    return (x1 ^ out1) & (x2 ^ out2) & (x3 ^ out3)


def main():
    F: Formula = PYSAT_FALSE
    T: Formula = PYSAT_TRUE

    expression = (
        comp(F, F, F)
        & comp(F, F, T)
        & comp(F, T, F)
        & comp(F, T, T)
        & comp(T, F, F)
        & comp(T, F, T)
        & comp(T, T, F)
        & comp(T, T, T)
    )

    with Solver(bootstrap_with=expression) as solver:
        if not solver.solve():
            print("UNSAT")
            return

        model: list[int] = solver.get_model()

        vpool = expression.export_vpool()
        ans = []
        for lit in model:
            var_id = abs(lit)
            atom = vpool.obj(var_id)

            if type(atom) is Atom:
                ans.append(f"{int(lit > 0)} = {str(atom.object)}")

    print("\n".join(sorted(ans)))


main()
