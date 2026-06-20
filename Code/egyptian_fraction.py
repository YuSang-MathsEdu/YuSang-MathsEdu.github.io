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
  python Coding/egyptian_fraction.py 4 13
"""

from math import gcd


def egyptian_decomposition(a: int, b: int, max_iters: int = 10000, verbose: bool = True):
    """
    Return a list of denominators for the egyptian decomposition of a/b.
    If verbose is True, print per-step trace to stdout.
    """
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
        if verbose:
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


def one_line_summary(a, b, dens, cum):
    """Return a compact one-line summary string."""
    left = f"{a}/{b}"
    expr = format_decomposition(dens)
    right = f"{cum.numerator}/{cum.denominator}"
    return f"{left} -> {expr} -> {right}"


def main():
    import argparse
    import sys
    import json
    from fractions import Fraction

    parser = argparse.ArgumentParser(description="Egyptian fraction decomposition")
    parser.add_argument("a", type=int, help="numerator (a), must be < b")
    parser.add_argument("b", type=int, help="denominator (b)")
    parser.add_argument("--max-iters", type=int, default=10000, help="maximum iterations before aborting")
    parser.add_argument("--quiet", action="store_true", help="suppress per-step debug output")
    parser.add_argument("--summary", action="store_true", help="print one-line summary suitable for CI logs")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON to stdout")
    parser.add_argument("--json-file", type=str, default=None, help="write machine-readable JSON to this file path")
    args = parser.parse_args()

    a = args.a
    b = args.b
    orig = Fraction(a, b)

    try:
        dens = egyptian_decomposition(a, b, max_iters=args.max_iters, verbose=(not args.quiet))
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(1)

    print()
    print(f"Decomposition of {a}/{b} is:")
    print(format_decomposition(dens))

    # compute exact sum of unit fractions
    cum = Fraction(0, 1)
    if not args.quiet:
        print()
        print("Stepwise addition of unit fractions:")
    for i, d in enumerate(dens, start=1):
        cum += Fraction(1, d)
        if not args.quiet:
            print(f"  {i}. add 1/{d} => {cum.numerator}/{cum.denominator}")

    # Final outputs: expression, final rational, and verification vs original
    print()
    print(f"Full expression: {format_decomposition(dens)} = {cum.numerator}/{cum.denominator}")
    print(f"Verification: sum = {cum} (original {orig})")
    ok = (cum == orig)
    if ok:
        print("Check: OK — the decomposition sums exactly to the original fraction.")
    else:
        diff = cum - orig
        print(f"Check: MISMATCH — sum differs by {diff} ({float(diff):.12g})")

    # One-line summary for CI logs
    if args.summary:
        print()
        print(one_line_summary(a, b, dens, cum))

    # Machine-readable JSON output
    if args.json or args.json_file:
        obj = {
            "input": {"a": a, "b": b},
            "denominators": dens,
            "final_numerator": cum.numerator,
            "final_denominator": cum.denominator,
            "decimal_sum": float(cum),
            "ok": ok,
        }
        json_text = json.dumps(obj, separators=(',', ':'), sort_keys=True)
        if args.json:
            print()
            print(json_text)
        if args.json_file:
            try:
                with open(args.json_file, 'w', encoding='utf-8') as fh:
                    fh.write(json_text + '\n')
            except Exception as e:
                print(f"Warning: failed to write JSON file {args.json_file}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
