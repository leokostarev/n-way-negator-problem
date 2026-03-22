from itertools import combinations, product
import math
import os
from typing import Any


def parenthesize(expr: str):
    return f"({expr})"


# This generates a function which effectivly determines
# if count of turned on input variables is greater or equal to k
# n - total number of variables
# k - number of variables in monom
def ge_inputs(n: int, k: int, exclude: str = ""):
    vars = [f"x{i}" for i in range(1, n + 1)]

    return parenthesize(
        " or ".join(
            parenthesize(" and ".join(i))
            for i in combinations(vars, k)
            if exclude not in i
        )
    )


# This generates 2^s-1 variable negator circuit, using s "not" gates
# in form of a python function
# s - number of "not" gates


def gen(s: int):
    n = 2**s - 1  # number of inputs, from here on out named `x1`..`xn`

    # let count of turned on inputs from this point on be equal to phi,
    # then `v{s-1}`..`v0` are bits of phi,
    # such that phi = `v{s-1}` * 2^(s-1) + `v{s-2}` * 2^{s-2} + ... + `v0`.
    # nv{i} = not v{i}

    # we well construct them in order `v{s-1}`, nv{s-1}, `v{s-2}`, nv{s-2}, ..., `v0`, `nv0`
    # theese valus are used to construct `out1`, `out2`, ..., `outn`,
    # which are the outputs of the circuit, such that `out{i}` is the negation of `x{i}`

    # resulting function code
    func = [f"def negate({', '.join(f'x{i}' for i in range(1, n + 1))}):\n"]

    def add_line(line: str):
        nonlocal func
        func.append(f"    {line}\n")

    # constructing `v{s-1}` and `nv{s-1}`, theese are special
    # because they only depend on inputs, not on other `v`s
    highest = ge_inputs(n, 2 ** (s - 1))
    add_line(f"v{s - 1} = {highest}")
    add_line(f"nv{s - 1} = not v{s-1}")

    # constructing `v{i}`s and `nv{i}`s for i = s-2, s-3, ..., 0
    for v_idx in range(s - 2, -1, -1):
        vs_before_me_n = s - 1 - v_idx  # number of `v{j}`s, such that j > v_idx

        # "Abandon all hope, ye who enter here." Dante
        # python functional devil made me write this, I'm sorry
        # just belibe and don't read this if you value your sanity
        vi_formula = " or ".join(
            parenthesize(
                " and ".join(
                    (
                        f"v{bbi + 1 + v_idx}"
                        if (before_bits >> bbi & 1)
                        else f"nv{bbi + 1 + v_idx}"
                    )
                    for bbi in range(0, vs_before_me_n)
                )
                + " and "
                + ge_inputs(n, ((2 * before_bits + 1) << v_idx))
            )
            for before_bits in range(0, 2**vs_before_me_n)
        )

        add_line(f"v{v_idx} = {vi_formula}")
        add_line(f"nv{v_idx} = not v{v_idx}")

    # constructing `outi` for i = 1, 2, ..., n
    for x_idx in range(1, n + 1):
        # x{i} is turned off if (phi == 0) <=> (`nv{s-1}` == .. ==`nv0` == True)
        outi_formula = [parenthesize(" and ".join(f"nv{bit}" for bit in range(s)))]

        # otherwise some variables might be turned on, but not x{i}
        # which is represented by "branching" for each value of phi
        for phi in range(1, n):
            outi_formula.append(
                parenthesize(
                    # this part is "branching", "exactly phi variables are turned on"
                    " and ".join(
                        f"v{bit}" if (phi >> bit & 1) else f"nv{bit}"
                        for bit in range(s)
                    )
                    # end "branching" part
                    + " and "
                    + ge_inputs(n, phi, f"x{x_idx}")  # phi other variables is on
                )
            )

        outi_formula = " or ".join(outi_formula)

        add_line(f"out{x_idx} = {outi_formula}")

    add_line(
        f"return ({", ".join(
        f"out{x_idx}"
        for x_idx in range(1, n + 1)
    )},)"  # returning results as tuple
    )

    return "".join(func)


def test(code: str, s: int):
    ns: dict[str, Any] = {}
    exec(code, ns)
    neg = ns["negate"]

    for inp in product((False, True), repeat=(2**s - 1)):
        out = neg(*inp)

        for i, j in zip(inp, out):
            assert i != j

    print(f"{s=}, success!")


def test_upto(s_max: int):
    for s in range(1, s_max + 1):
        code = gen(s)
        test(code, s)


def measure_upto(s_max: int):
    print("n = (2^s - 1) is the number of input variables of the circuit")
    print("s, n, length, log2(length)")
    for s in range(1, s_max + 1):
        n = 2**s - 1
        l = len(gen(s))
        print(s, n, l, round(math.log2(l), 2))


def main():
    print(
        "Usage:",
        "Please use values of s above 4 with caution, as the resulting code grows exponentially with s",
        "Commands:",
        "gen s [filename] - generates circuit with s not gates, and writes to ./generated/filename \
 (or prints to console if filename is not provided)",
        "test k - tests circuit with s not gates for s = 1..k",
        "measure k - measures length of generated code for s = 1..k",
        sep="\n",
        end="\n\n",
    )

    command = input("Enter command: ").split()

    if command[0] == "gen":
        s = int(command[1])
        circuit = gen(s)

        if len(command) == 2:
            print(circuit)
        else:
            filename = command[2]

            os.makedirs("./generated", exist_ok=True)
            with open(f"./generated/{filename}", "w") as f:
                f.write(circuit)

            print(
                f"Circuit with s={s} not gates generated and written to ./generated/{filename}"
            )
    elif command[0] == "test":
        k = int(command[1])
        test_upto(k)
    elif command[0] == "measure":
        k = int(command[1])
        measure_upto(k)
    else:
        print("Unknown command")


if __name__ == "__main__":
    main()
