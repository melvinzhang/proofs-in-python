# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "sympy",
#     "z3-solver",
#     "mathesis",
# ]
# ///
"""
Writing proofs in Python — lightning talk demos.

Run everything:           uv run demo.py
Run one proof:            uv run demo.py full_adder
                          uv run demo.py arithmetic_progression_sum
                          uv run demo.py double_angle

Each function below proves ONE statement, and the proof is right there in
the open -- no hidden helper. Three idioms appear:

    SymPy:    assert simplify(lhs - rhs) == 0   # the difference is 0 for all x
    z3:       prove(claim)                      # valid for all inputs, else
                                                # it prints a counterexample
    mathesis: nd.apply(line, rule)              # a textbook proof, by hand:
                                                # one justified inference step
                                                # per line (see ..._by_hand)

Because the SymPy proof is an `assert`, a false claim stops the program with
an error rather than printing a reassuring line.
"""

import sys


# --- A-level / Additional Maths (SymPy) -----------------------------------

def double_angle():
    """The double-angle identity:  cos(2x) = 1 - 2 sin^2 x."""
    from sympy import Symbol, sin, cos, simplify

    x = Symbol("x")
    assert simplify(cos(2 * x) - (1 - 2 * sin(x) ** 2)) == 0
    print("proved")


def pythagorean_identity():
    """The Pythagorean identity:  sin^2 x + cos^2 x = 1."""
    from sympy import Symbol, sin, cos, simplify

    x = Symbol("x")
    assert simplify(sin(x) ** 2 + cos(x) ** 2 - 1) == 0
    print("proved")


def compound_angle():
    """The compound-angle formula:  sin(A+B) = sinA cosB + cosA sinB."""
    from sympy import symbols, sin, cos, simplify

    a, b = symbols("A B")
    assert simplify(sin(a + b) - (sin(a) * cos(b) + cos(a) * sin(b))) == 0
    print("proved")


def sum_of_integers():
    """Closed form:  1 + 2 + ... + n = n(n+1)/2."""
    from sympy import symbols, summation, simplify

    n, k = symbols("n k", positive=True, integer=True)
    total = summation(k, (k, 1, n))                 # SymPy evaluates the sum
    assert simplify(total - n * (n + 1) / 2) == 0
    print("proved")


def arithmetic_progression_sum():
    """AP sum: a + (a+d) + ... + (a+(n-1)d) = n(2a+(n-1)d)/2."""
    from sympy import symbols, summation, simplify

    a, d = symbols("a d")
    n, k = symbols("n k", positive=True, integer=True)
    total = summation(a + k * d, (k, 0, n - 1))
    assert simplify(total - n * (2 * a + (n - 1) * d) / 2) == 0
    print("proved")


def sum_of_squares():
    """Closed form:  1^2 + 2^2 + ... + n^2 = n(n+1)(2n+1)/6."""
    from sympy import symbols, summation, simplify

    n, k = symbols("n k", positive=True, integer=True)
    total = summation(k ** 2, (k, 1, n))
    assert simplify(total - n * (n + 1) * (2 * n + 1) / 6) == 0
    print("proved")


def binomial_theorem():
    """The binomial expansion of (a+b)^4 = sum_{k} C(4,k) a^(4-k) b^k."""
    from sympy import symbols, binomial, summation, simplify

    a, b = symbols("a b")
    k = symbols("k", integer=True)
    expansion = summation(binomial(4, k) * a ** (4 - k) * b ** k, (k, 0, 4))
    assert simplify((a + b) ** 4 - expansion) == 0
    print("proved")


def quadratic_formula():
    """The quadratic formula's root really solves  a x^2 + b x + c = 0."""
    from sympy import symbols, sqrt, simplify

    a, b, c = symbols("a b c")
    x = (-b + sqrt(b ** 2 - 4 * a * c)) / (2 * a)   # the formula
    assert simplify(a * x ** 2 + b * x + c) == 0    # substitute it back in
    print("proved")


def remainder_theorem():
    """Dividing p(x) by (x - r) leaves remainder p(r)."""
    from sympy import symbols, rem, simplify

    x, r = symbols("x r")
    p = x ** 3 - 2 * x + 5
    assert simplify(rem(p, x - r, x) - p.subs(x, r)) == 0
    print("proved")


# --- O & A-level Computing (z3) --------------------------------------------

def de_morgan():
    """De Morgan's law:  not(p and q) = (not p) or (not q)."""
    from z3 import Bools, Not, And, Or, prove

    p, q = Bools("p q")
    prove(Not(And(p, q)) == Or(Not(p), Not(q)))


def distributive_law():
    """AND distributes over OR:  a & (b | c) = (a & b) | (a & c)."""
    from z3 import Bools, And, Or, prove

    a, b, c = Bools("a b c")
    prove(And(a, Or(b, c)) == Or(And(a, b), And(a, c)))


def absorption_law():
    """The absorption law:  a | (a & b) = a."""
    from z3 import Bools, And, Or, prove

    a, b = Bools("a b")
    prove(Or(a, And(a, b)) == a)


def boolean_simplification():
    """Consensus theorem: the term (b & c) is redundant, fewer gates suffice."""
    from z3 import Bools, Not, And, Or, prove

    a, b, c = Bools("a b c")
    full = Or(And(a, b), And(Not(a), c), And(b, c))
    simplified = Or(And(a, b), And(Not(a), c))
    prove(full == simplified)


def full_adder():
    """A full-adder gate circuit equals binary addition, for all inputs."""
    from z3 import Bools, Xor, And, Or, If, prove

    a, b, cin = Bools("a b cin")
    sum_bit = Xor(Xor(a, b), cin)
    carry = Or(And(a, b), And(cin, Xor(a, b)))

    total = If(a, 1, 0) + If(b, 1, 0) + If(cin, 1, 0)
    prove(If(sum_bit, 1, 0) == total % 2)   # sum   = (a + b + cin) mod 2
    prove(If(carry, 1, 0) == total / 2)     # carry = (a + b + cin) div 2


def twos_complement():
    """Negation is bit-flip-plus-one:  -x == ~x + 1, for all 8-bit x."""
    from z3 import BitVec, prove

    x = BitVec("x", 8)
    prove(-x == ~x + 1)


def shift_is_multiply():
    """A left shift is multiplication by two:  x << 1 == x * 2."""
    from z3 import BitVec, prove

    x = BitVec("x", 8)
    prove(x << 1 == x * 2)


def midpoint():
    """Binary search midpoint: (lo+hi)/2 overflows; an overflow-free form does not."""
    from z3 import BitVec, ZeroExt, LShR, Implies, And, prove

    lo, hi = BitVec("lo", 32), BitVec("hi", 32)
    valid = And(lo >= 0, hi >= 0)                        # real array indices
    true_mid = LShR(ZeroExt(1, lo) + ZeroExt(1, hi), 1)  # midpoint, no overflow

    prove(Implies(valid, true_mid == ZeroExt(1, (lo + hi) / 2)))                  # buggy -> counterexample
    prove(Implies(valid, true_mid == ZeroExt(1, (lo & hi) + LShR(lo ^ hi, 1))))   # fixed -> proved


def xor_counterexample():
    """Disprove a false claim: z3 finds an input where x XOR y != x OR y."""
    from z3 import Bools, Xor, Or, Solver, sat

    x, y = Bools("x y")
    s = Solver()
    s.add(Xor(x, y) != Or(x, y))            # ask for a disagreeing input
    if s.check() == sat:
        m = s.model()
        print(f"false -- counterexample:  x={m[x]}, y={m[y]}")
    else:
        print("no counterexample: the claim holds")


# --- A textbook-style proof, written by hand (mathesis) --------------------

def conjunction_commutes_by_hand():
    """Hand-written natural deduction:  A∧B ⊢ B∧A, one rule per step.

    mathesis works the goal BACKWARDS (analytic / goal-directed), the way a
    tactic prover like pyzar does -- you reduce the goal, then justify each
    piece.  Read the apply()s top-down as: "to prove the goal, it suffices
    to ...".  (A forward premise->conclusion order is not valid here; the
    conventional textbook orientation shows up in nd.latex().)
    """
    from mathesis.grammars import BasicGrammar
    from mathesis.deduction.natural_deduction import NDTree, rules as R

    g = BasicGrammar()
    nd = NDTree([g.parse("A∧B")], g.parse("B∧A"))   # premise ⊢ goal
    nd.apply(nd[2], R.Conjunction.Intro())          # to prove B∧A, prove B and A  [∧I]
    nd.apply(nd[4], R.Conjunction.Elim("right"))    # B follows from A∧B           [∧E]
    nd.apply(nd[6], R.Conjunction.Elim("left"))     # A follows from A∧B           [∧E]
    assert nd.is_valid()                            # every branch is justified
    print(nd.tree())
    print("proved")


PROOFS = {
    "double_angle": double_angle,
    "pythagorean_identity": pythagorean_identity,
    "compound_angle": compound_angle,
    "sum_of_integers": sum_of_integers,
    "arithmetic_progression_sum": arithmetic_progression_sum,
    "sum_of_squares": sum_of_squares,
    "binomial_theorem": binomial_theorem,
    "quadratic_formula": quadratic_formula,
    "remainder_theorem": remainder_theorem,
    "de_morgan": de_morgan,
    "distributive_law": distributive_law,
    "absorption_law": absorption_law,
    "boolean_simplification": boolean_simplification,
    "full_adder": full_adder,
    "twos_complement": twos_complement,
    "shift_is_multiply": shift_is_multiply,
    "midpoint": midpoint,
    "xor_counterexample": xor_counterexample,
    "conjunction_commutes_by_hand": conjunction_commutes_by_hand,
}


def main():
    which = sys.argv[1:] or PROOFS.keys()
    for name in which:
        if name not in PROOFS:
            print(f"unknown proof: {name!r}; choose from {list(PROOFS)}")
            continue
        print(f"\n== {name}: {PROOFS[name].__doc__.splitlines()[0]} ==")
        PROOFS[name]()


if __name__ == "__main__":
    main()
