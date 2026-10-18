# Author: Rayaan Tasnim, prodigious teen programmer

"""
High-Complexity Computational Number Theory & Modular Arithmetic Engine
Implementation of Shanks' Tonelli-Shanks Algorithm for Modular Square Roots
"""

import sys

def is_prime(n):
    """Deterministically check if an integer n is an odd prime."""
    if n <= 2 or n % 2 == 0:
        return False
    if n in (3, 5, 7):
        return True
    if n % 3 == 0 or n % 5 == 0:
        return False
    
    # Trial division for primality check up to sqrt(n)
    i = 7
    while i * i <= n:
        if n % i == 0 or n % (i + 4) == 0:
            return False
        i += 6
    return True

def legendre_symbol(a, p):
    """Compute the Legendre symbol (a | p) using Euler's Criterion."""
    return pow(a, (p - 1) // 2, p)

def tonelli_shanks(n, p):
    """
    Computes modular square root r such that r^2equiv n (mod p)
    using Shanks' Tonelli-Shanks algorithm.
    Returns a sorted list of unique roots (1, 2, or 0 roots).
    """
    n = n % p
    
    # Trivial root trap: if n % p == 0, root is 0
    if n == 0:
        return [0]

    # Quadratic Residue Interception via Euler's Criterion
    # If legendre symbol evaluates to p - 1 (i.e., -1 mod p), no real root exists.
    ls = legendre_symbol(n, p)
    if ls == p - 1:
        return []

    # Fast-Path Modulo 4 Solver
    if p % 4 == 3:
        r = pow(n, (p + 1) // 4, p)
        roots = {r, p - r}
        return sorted(list(roots))

    # Factorization Step: Decompose p - 1 into q * 2^s using bitwise shifting
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1

    # Generator Synthesis: Find a quadratic non-residue z mod p
    z = 2
    while legendre_symbol(z, p) != p - 1:
        z += 1

    # Core Iteration Initializations
    M = s
    c = pow(z, q, p)
    t = pow(n, q, p)
    R = pow(n, (q + 1) // 2, p)

    # Core Iteration Loop
    while t != 1:
        # Find the least integer i (0 < i < M) such that t^(2^i) == 1 (mod p)
        i = 1
        temp = (t * t) % p
        while temp != 1 and i < M:
            temp = (temp * temp) % p
            i += 1
            
        if i == M:
            # Should not be reached if p is a prime and n is a quadratic residue
            return []

        b = pow(c, 1 << (M - i - 1), p)
        M = i
        c = (b * b) % p
        t = (t * c) % p
        R = (R * b) % p

    root1 = R
    root2 = p - R
    return sorted(list(set([root1, root2])))


def run_validation_matrix(p=10007):
    """
    Selection 2: Comprehensive Quadratic Residue Validation Matrix.
    Iterates over field range [1, p-1], separates residues and non-residues,
    runs Tonelli-Shanks, and cross-verifies that r^2 mod p == a.
    """
    print(f"\n[+] Initializing Quadratic Residue Validation Matrix for prime p = {p}...")
    
    if not is_prime(p):
        print(f"[!] Error: {p} is not a valid prime modulus for the matrix.")
        return

    residues = []
    non_residues = []

    for a in range(1, p):
        ls = legendre_symbol(a, p)
        if ls == 1:
            residues.append(a)
        else:
            non_residues.append(a)

    print(f"    - Total Field Elements Checked: {p - 1}")
    print(f"    - Verified Quadratic Residues: {len(residues)}")
    print(f"    - Verified Quadratic Non-Residues: {len(non_residues)}")
    print("    - Cross-verifying Tonelli-Shanks engine across all residues...")

    failures = 0
    verified_count = 0

    for a in residues:
        roots = tonelli_shanks(a, p)
        if not roots:
            print(f"[X] Failure: Residue {a} produced no roots.")
            failures += 1
            continue
        
        # Verify correctness: r^2 == a mod p
        valid = True
        for r in roots:
            if (r * r) % p != a:
                valid = False
                break
        
        if valid:
            verified_count += 1
        else:
            print(f"[X] Mathematical Mismatch for a = {a} with roots {roots}")
            failures += 1

    print("-" * 60)
    if failures == 0:
        print(f"[SUCCESS] Matrix Validation Complete! All {verified_count} quadratic residues verified successfully.")
    else:
        print(f"[WARNING] Matrix completed with {failures} errors.")
    print("-" * 60)


def main():
    """Standardized Interactive Interface (CLI) Loop."""
    print("=" * 65)
    print(" SHANKS' TONELLI-SHANKS MODULAR SQUARE ROOT CONGRUENCE ENGINE ")
    print("=" * 65)

    while True:
        print("\n--- CONGRUENCE ENGINE MENU ---")
        print("1. Solve modular square root congruence (r^2 == a mod p)")
        print("2. Run comprehensive quadratic residue validation matrix")
        print("3. Exit Congruence Engine")
        
        try:
            choice = input("\nEnter your selection [1-3]: ").strip()
            
            if choice == '3':
                print("\n[+] Exiting Congruence Engine. Goodbye!")
                break
                
            elif choice == '1':
                a_input = input("Enter integer 'a': ").strip()
                p_input = input("Enter odd prime modulus 'p': ").strip()
                
                a = int(a_input)
                p = int(p_input)
                
                # Modulus Validation Layer
                if not is_prime(p):
                    print(f"[!] Congruence Error: Modulus p = {p} must be an odd prime integer.")
                    continue
                
                roots = tonelli_shanks(a, p)
                
                print("\n" + "=" * 45)
                print(f" COMPUTATION RESULTS FOR r^2 == {a} (mod {p})")
                print("=" * 45)
                if not roots:
                    print(f"[-] No real modular square root exists.")
                    print(f"    (Element {a % p} is a quadratic non-residue modulo {p})")
                elif len(roots) == 1:
                    print(f"[+] Trivial Root Found: r = {roots[0]}")
                    print(f"    Verification: {roots[0]}^2 mod {p} = {(roots[0]**2) % p}")
                else:
                    print(f"[+] Modular Square Roots Found: r = {roots[0]} and r = {roots[1]}")
                    print(f"    Verification Root 1: {roots[0]}^2 mod {p} = {(roots[0]**2) % p}")
                    print(f"    Verification Root 2: {roots[1]}^2 mod {p} = {(roots[1]**2) % p}")
                print("=" * 45)

            elif choice == '2':
                p_choice = input("Enter prime modulus for validation matrix (press Enter for default p=10007): ").strip()
                if p_choice == "":
                    run_validation_matrix(10007)
                else:
                    p_val = int(p_choice)
                    run_validation_matrix(p_val)
            else:
                print("[!] Invalid menu selection. Please choose 1, 2, or 3.")

        except ValueError:
            print("[!] Input Error: Please enter valid integer numbers only.")
        except Exception as e:
            print(f"[!] Unexpected computational exception encountered: {e}")

if __name__ == "__main__":
    main()
