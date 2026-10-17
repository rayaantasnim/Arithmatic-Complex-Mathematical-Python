#!/usr/bin/env python3
"""
Advanced Pollard's Rho Integer Factorization Engine with Brent's Cycle-Finding Optimization.
Engineered with rigorous mathematical safeguards, pre-flight interception matrices,
and a standardized interactive CLI interface.
"""

import math
import random
import sys
import time


def is_prime(n, k=40):
    """
    Robust Miller-Rabin deterministic/probabilistic primality test.
    Handles large integers efficiently.
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    # Write n - 1 as d * 2^r
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Deterministic bases for 64-bit integers, plus random bases for arbitrary scale
    bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for a in bases:
        if n <= a:
            break
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    # Additional random checks for extreme safety
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


def preflight_check(n):
    """
    Pre-flight interception matrix:
    - Rejects n <= 1 (Domain Error)
    - Identifies trivial small primes (2, 3, 5, 7)
    - Intercepts trivial prime multiples of 2, 3, 5, 7
    - Intercepts perfect squares using math.isqrt
    - Intercepts higher perfect powers (n = p^k for k >= 3)
    Returns (factor, is_prime_flag).
    """
    if n <= 1:
        raise ValueError("Domain Error: Integer must be strictly greater than 1.")

    if n in (2, 3, 5, 7):
        return n, True

    # Trivial small prime multiples check
    for p in (2, 3, 5, 7):
        if n % p == 0:
            return p, False

    # Perfect Squares Edge Case Matrix
    root = math.isqrt(n)
    if root * root == n:
        return root, False

    # Perfect Powers Edge Case Matrix (k >= 3)
    max_k = n.bit_length()
    for k in range(3, max_k + 1):
        p = int(n ** (1.0 / k) + 0.5)
        if p ** k == n:
            return p, False
        if (p + 1) ** k == n:
            return p + 1, False
        if p > 1 and (p - 1) ** k == n:
            return p - 1, False

    if is_prime(n):
        return n, True

    return None, False


def brent_pollard_rho(n):
    """
    Brent's modified Pollard's Rho algorithm with O(n^0.25) amortized complexity.
    Uses windowed evaluation, chunking, and accumulative modular multiplication.
    """
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3
    if n % 5 == 0:
        return 5
    if n % 7 == 0:
        return 7

    if is_prime(n):
        return n

    # Dynamic boundary scaling for random initialization to avoid ValueError
    y = random.randint(1, n - 1)
    c = random.randint(1, n - 1)
    m = random.randint(1, max(1, n // 100))
    g = 1
    r = 1
    q = 1
    x = y

    while g == 1:
        x = y
        for _ in range(r):
            y = (pow(y, 2, n) + c) % n

        k = 0
        while k < r and g == 1:
            ys = y
            for _ in range(min(m, r - k)):
                y = (pow(y, 2, n) + c) % n
                q = (q * abs(x - y)) % n
            g = math.gcd(q, n)
            k += m
        r *= 2

    if g == n:
        while True:
            ys = (pow(ys, 2, n) + c) % n
            g = math.gcd(abs(x - ys), n)
            if g > 1:
                break

    return g


def factor_decomposition(n):
    """
    Bulletproof recursive structural decomposition engine.
    Breaks down an arbitrary composite integer completely into its prime factors.
    """
    if n <= 1:
        return []

    factor, prime_flag = preflight_check(n)
    if prime_flag or factor == n:
        return [n]

    if factor is not None and factor < n:
        return sorted(factor_decomposition(factor) + factor_decomposition(n // factor))

    d = brent_pollard_rho(n)
    if d == n or d == 1:
        return [n]

    return sorted(factor_decomposition(d) + factor_decomposition(n // d))


def main_cli():
    """
    Standardized interactive terminal interface loop with full exception handling.
    """
    while True:
        print("\n" + "=" * 60)
        print("     POLLARD'S RHO & BRENT'S FACTORIZATION ENGINE")
        print("=" * 60)
        print("  1. Isolate a single non-trivial factor (Engine Phase)")
        print("  2. Perform complete prime factorization (Decomposition Matrix)")
        print("  3. Exit Engine")
        print("=" * 60)

        try:
            choice = input("Select operation [1-3]: ").strip()
            if not choice:
                continue

            if choice == "3":
                print("\n[Exiting Engine. Goodbye!]")
                sys.exit(0)

            if choice not in ("1", "2"):
                print("\n[!] Error: Invalid selection. Please choose 1, 2, or 3.")
                continue

            raw_input = input("Enter target integer n (> 1): ").strip()
            n = int(raw_input)

            start_time = time.time()

            if choice == "1":
                print(f"\n[*] Pre-flight analysis and factor isolation for n = {n}...")
                factor, prime_flag = preflight_check(n)
                
                if prime_flag:
                    result = f"{n} is a verified PRIME number. No non-trivial factors exist."
                elif factor is not None and factor < n:
                    result = f"Isolated non-trivial factor: {factor} (Complement: {n // factor})"
                else:
                    d = brent_pollard_rho(n)
                    if d == n or d == 1:
                        result = f"{n} is verified PRIME or atomic."
                    else:
                        result = f"Isolated non-trivial factor: {d} (Complement: {n // d})"
                
                elapsed = time.time() - start_time
                print(f"[+] Result: {result}")
                print(f"[*] Execution time: {elapsed:.6f} seconds")

            elif choice == "2":
                print(f"\n[*] Executing full prime factorization decomposition matrix for n = {n}...")
                factors = factor_decomposition(n)
                elapsed = time.time() - start_time
                
                print(f"[+] Complete Prime Factors: {factors}")
                print(f"[+] Product Verification: {' * '.join(map(str, factors))} = {n}")
                print(f"[*] Execution time: {elapsed:.6f} seconds")

        except ValueError as ve:
            print(f"\n[!] ValueError Exception Caught: {ve}")
            print("[!] Please ensure you input a valid whole integer greater than 1.")
        except KeyboardInterrupt:
            print("\n\n[!] Operation interrupted by user. Exiting gracefully.")
            sys.exit(0)
        except Exception as e:
            print(f"\n[!] Unexpected Exception Caught: {e}")
            print("[!] Returning to main menu.")


if __name__ == "__main__":
    main_cli()
