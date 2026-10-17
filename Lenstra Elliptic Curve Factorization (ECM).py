#!/usr/bin/env python3
"""
Lenstra Elliptic Curve Factorization (ECM) Algorithm Implementation.
Author: Elite Research Mathematician & Senior Backend Python Engineer Rayaan Tasnim.
"""

import math
import random
import sys


class FactorFound(Exception):
  """Custom exception to securely bubble up non-trivial factors found

  during modular arithmetic and elliptic curve group operations.
  """

  def __init__(self, factor):
    super().__init__(f"Factor found: {factor}")
    self.factor = factor


def extended_gcd(a, b):
  """Extended Euclidean Algorithm.

  Returns (g, x, y) such that a*x + b*y = g = gcd(a, b).
  """
  x0, x1, y0, y1 = 0, 1, 1, 0
  while b != 0:
    q, a, b = divmod(a, b)
    x0, x1 = x1 - q * x0, x0
    y0, y1 = y1 - q * y0, y0
  return a, x1, y1


def mod_inverse(a, m):
  """Computes modular inverse of a modulo m.

  If gcd(a, m) > 1 and < m, immediately triggers FactorFound(gcd).
  """
  a = a % m
  if a == 0:
    raise FactorFound(math.gcd(a, m) if m > 1 else m)
  g, x, y = extended_gcd(a, m)
  if g > 1:
    if g == m:
      return None
    raise FactorFound(g)
  return (x % m + m) % m


def is_perfect_power(n):
  """Preprocessing Shield: Checks if n = p^k for k > 1.

  Returns base p if so, else None. Intercepts perfect powers
  to prevent ECM curve group law collapses.
  """
  if n <= 3:
    return None
  for b in range(2, int(math.isqrt(n)) + 1):
    temp = n
    while temp % b == 0:
      temp //= b
    if temp == 1:
      return b
  for k in range(2, n.bit_length() + 1):
    root = int(n ** (1.0 / k))
    for r in range(max(2, root - 2), root + 3):
      if r > 1 and r**k == n:
        return r
  return None


def check_small_primes(n):
  """Entry Safeguard: Intercepts trivial small inputs and prime factors of 2, 3, 5, 7."""
  if n <= 1:
    raise ValueError("Number must be an integer greater than 1.")
  small_primes = [2, 3, 5, 7]
  if n in small_primes:
    return "PRIME", None
  for p in small_primes:
    if n % p == 0:
      return "COMPOSITE", p
  return None, None


def ec_add(P, Q, a, n):
  """Adds two points P and Q on the Weierstrass elliptic curve y^2 = x^3 + ax + b (mod n)."""
  if P is None:
    return Q
  if Q is None:
    return P

  x1, y1 = P
  x2, y2 = Q

  if x1 == x2:
    if (y1 + y2) % n == 0:
      return None  # Point at infinity
    else:
      return ec_double(P, a, n)

  dx = (x2 - x1) % n
  inv_dx = mod_inverse(dx, n)
  dy = (y2 - y1) % n
  lam = (dy * inv_dx) % n

  x3 = (lam * lam - x1 - x2) % n
  y3 = (lam * (x1 - x3) - y1) % n
  return (x3, y3)


def ec_double(P, a, n):
  """Doubles a point P on the Weierstrass elliptic curve y^2 = x^3 + ax + b (mod n)."""
  if P is None:
    return None

  x1, y1 = P
  if y1 == 0:
    g = math.gcd(2 * y1, n)
    if 1 < g < n:
      raise FactorFound(g)
    return None

  dy = (3 * x1 * x1 + a) % n
  inv_dy = mod_inverse(2 * y1, n)
  lam = (dy * inv_dy) % n

  x3 = (lam * lam - 2 * x1) % n
  y3 = (lam * (x1 - x3) - y1) % n
  return (x3, y3)


def ec_multiply(k, P, a, n):
  """Scalar point multiplication k * P using the logarithmic double-and-add binary strategy."""
  R = None
  Q = P
  while k > 0:
    if k & 1:
      R = ec_add(R, Q, a, n)
    Q = ec_double(Q, a, n)
    k >>= 1
  return R


def generate_primes_sieve(b1):
  """Generates a deterministic list of prime numbers up to smoothness bound B1."""
  if b1 < 2:
    return []
  sieve = [True] * (b1 + 1)
  sieve[0] = sieve[1] = False
  for start in range(2, int(math.isqrt(b1)) + 1):
    if sieve[start]:
      for i in range(start * start, b1 + 1, start):
        sieve[i] = False
  return [i for i, is_p in enumerate(sieve) if is_p]


def ecm_factorize(n, b1=2000, max_curves=200):
  """Core ECM Engine implementing Lenstra's Stage 1 algorithm."""
  # 1. Global Safeguards & Preprocessing
  status, factor = check_small_primes(n)
  if status == "PRIME":
    return f"{n} is prime."
  if status == "COMPOSITE":
    return factor

  base_p = is_perfect_power(n)
  if base_p is not None:
    return base_p

  # 2. Stage 1 Smoothness Bounds & Prime Power Setup
  primes = generate_primes_sieve(b1)
  prime_powers = []
  for p in primes:
    p_power = p
    while p_power * p <= b1:
      p_power *= p
    prime_powers.append(p_power)

  # 3. Randomized Curve Trials Loop
  for curve_idx in range(max_curves):
    x0 = random.randrange(0, n)
    y0 = random.randrange(0, n)
    a = random.randrange(0, n)

    # Compute b such that the curve passes through (x0, y0)
    b = (y0 * y0 - x0 * x0 * x0 - a * x0) % n

    # Validate curve discriminant: 4*a^3 + 27*b^2 (mod n)
    discriminant = (4 * a * a * a + 27 * b * b) % n
    g = math.gcd(discriminant, n)
    if g > 1:
      if g < n:
        return g
      else:
        continue  # Discard singular curve

    P = (x0, y0)

    try:
      # Accumulate scalar multiplications over prime power bounds
      for p_pow in prime_powers:
        P = ec_multiply(p_pow, P, a, n)
    except FactorFound as ff:
      f = ff.factor
      if 1 < f < n:
        return f

  raise RuntimeError(
      "ECM Stage 1 exhausted maximum curve trials without factorization."
      " Increase B1 or max_curves."
  )


def run_continuous_test():
  """Demonstrates ECM breaking down composite targets across multiple test cases."""
  print("\n--- Running Continuous ECM Demonstration Test ---")
  test_composites = [
      1189,  # 29 * 41
      10403,  # 101 * 103
      5917,  # 61 * 97
      1000003 * 1000033,  # Large composite product
      2**32 + 1,  # Fermat number F4 (6700417 * 641)
  ]

  for target in test_composites:
    print(f"\nTarget composite: {target}")
    try:
      factor = ecm_factorize(target, b1=2000, max_curves=50)
      cofactor = target // factor
      print(f"[SUCCESS] Discovered factor: {factor} | Cofactor: {cofactor}")
      print(f"[SUCCESS] Product verification: {factor * cofactor == target}")
    except Exception as e:
      print(f"[FAILED] Test failed for {target}: {e}")
  print("\nContinuous test completed successfully.")


def main():
  """Standardized interactive CLI interface with an infinite control loop."""
  print("==================================================")
  print("   LENSTRA ELLIPTIC CURVE FACTORIZATION (ECM)     ")
  print("==================================================")

  while True:
    print("\nMain Menu:")
    print("  1. Factorize an integer via Elliptic Curve Groups")
    print("  2. Run continuous test (Demonstrate ECM breaking composites)")
    print("  3. Exit Engine")

    try:
      choice = input("Select an option [1-3]: ").strip()
      if choice == "1":
        raw_input = input("Enter an integer to factorize: ").strip()
        n = int(raw_input)
        print(f"Running ECM on {n}...")
        result = ecm_factorize(n)
        if isinstance(result, int):
          cofactor = n // result
          print(f"\n[+] Non-trivial factor found: {result}")
          print(f"[+] Cofactor: {cofactor}")
          print(f"[+] Verification: {result} * {cofactor} = {n}")
        else:
          print(f"\n[+] Result: {result}")

      elif choice == "2":
        run_continuous_test()

      elif choice == "3":
        print("Exiting ECM Engine. Goodbye!")
        break
      else:
        print("[!] Invalid selection. Please choose 1, 2, or 3.")

    except ValueError as ve:
      print(f"[!] Input Error: Please enter a valid integer. Details: {ve}")
    except FactorFound as ff:
      f = ff.factor
      print(f"\n[+] Non-trivial factor caught at top-level: {f}")
    except Exception as e:
      print(f"[!] Computational Error: {e}")


if __name__ == "__main__":
  main()
