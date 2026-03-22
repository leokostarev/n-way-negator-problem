# this is a hand-written 3-negator circuit
# for solution given by solver in solve-for-3-circuit.py

from itertools import product


def circuit(x1: bool, x2: bool, x3: bool):
    v1 = not ((x1 and x2) or (x1 and x3) or (x2 and x3))

    v2 = not ((x1 and x2 and x3) or (x1 and v1) or (x2 and v1) or (x3 and v1))

    out1 = (x2 and v1) or (x3 and v1) or (x2 and x3 and v2) or (v1 and v2)

    out2 = (x1 and v1) or (x3 and v1) or (x1 and x3 and v2) or (v1 and v2)

    out3 = (x1 and v1) or (x2 and v1) or (x1 and x2 and v2) or (v1 and v2)

    assert (x1 ^ out1) and (x2 ^ out2) and (x3 ^ out3)


for xs in product((False, True), repeat=3):
    circuit(*xs)

print("All combinations passed!")
