#!/usr/bin/env python3
"""
Egyptian-fraction style loop:
Input two natural numbers a and b (with a < b).
Loop:
  c = ceil(b/a)
  d = a*c - b
  if d == 0: stop
  else a, b = d, b*c (reduce fraction each step)
This script prints the sequence of c's and the resulting sum of unit fractions.

Usable from CLI as:
  python egyptian_fraction.py 4 13
"""

from math import gcd


def egyptian_decomposition(a: int, b: int, max_iters: int = 10000):
    if a <= 0 or b <= 0:
        raise ValueError("a and b must be positive integers.")
    if not (a < b):
        raise ValueError("Require a < b.")
    dens = []
    iters = 0
    while True:
        iters += 1
        if iters > max_iters:
            raise RuntimeError("Exceeded maximum iterations; aborting (possible non-termination).")
        # compute ceil(b/a) using integer arithmetic
        c = (b + a - 1) // a
        dens.append(c)
        d = a * c - b
        # Debug / trace info (you can comment this out if verbose):
        print(f"Step {iters}: a={a}, b={b}, c=ceil({b}/{a})={c}, d={a}*{c}-{b}={d}")
        if d == 0:
            break
        # update and reduce fraction a/b to keep numbers smaller
        a, b = d, b * c
        g = gcd(a, b)
        if g > 1:
            a //= g
            b //= g
    return dens


def format_decomposition(dens):
    parts = [f"1/{d}" for d in dens]
    return " + ".join(parts)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Egyptian fraction decomposition")
    parser.add_argument("a", type=int, help="numerator (a), must be < b")
    parser.add_argument("b", type=int, help="denominator (b)")
    parser.add_argument("--max-iters", type=int, default=10000, help="maximum iterations before aborting")
    args = parser.parse_args()

    a = args.a
    b = args.b

    try:
        dens = egyptian_decomposition(a, b, max_iters=args.max_iters)
    except Exception as e:
        print("Error:", e)
        return

    print()
    print(f"Decomposition of {a}/{b} is:")
    print(format_decomposition(dens))

    # optional check: verify sum equals original fraction
    from fractions import Fraction
    ssum = sum(Fraction(1, d) for d in dens)
    print(f"Verification: sum = {ssum} (original {Fraction(a, b)})")


if __name__ == "__main__":
    main()
