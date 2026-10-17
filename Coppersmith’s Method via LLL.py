# Author: Rayaan Tasnim, prodigious teen programmer

import sys
import math
from fractions import Fraction

def lll(basis, delta=0.75):
    """
    Pure Python LLL Lattice Basis Reduction algorithm using exact rational arithmetic 
    (fractions.Fraction) to guarantee numerical stability and prevent precision loss.
    """
    n = len(basis)
    b = [list(row) for row in basis]
    
    def dot(u, v):
        return sum(x * y for x, y in zip(u, v))
    
    def gram_schmidt(b_matrix):
        size = len(b_matrix)
        B = []
        mu = [[Fraction(0)] * size for _ in range(size)]
        for i in range(size):
            B.append(list(b_matrix[i]))
            for j in range(i):
                num = dot(b_matrix[i], B[j])
                den = dot(B[j], B[j])
                mu[i][j] = Fraction(num, den) if den != 0 else Fraction(0)
                for k in range(len(B[j])):
                    B[i][k] -= mu[i][j] * B[j][k]
        return B, mu

    k = 1
    while k < n:
        B, mu = gram_schmidt(b)
        
        # Step 2: Size reduction
        for j in range(k - 1, -1, -1):
            if abs(mu[k][j]) > Fraction(1, 2):
                q = round(float(mu[k][j]))
                for c in range(len(b[k])):
                    b[k][c] -= int(q) * b[j][c]
                B, mu = gram_schmidt(b)
        
        # Step 3: Lovász condition check
        lhs = dot(B[k], B[k])
        rhs = (Fraction(str(delta)) - mu[k][k-1]**2) * dot(B[k-1], B[k-1])
        if lhs >= rhs:
            k += 1
        else:
            b[k], b[k-1] = b[k-1], b[k]
            k = max(k - 1, 1)
            
    return b

def evaluate_polynomial_coeffs(coeffs, x):
    """Evaluates polynomial given by coefficients [a_0, a_1, ..., a_d] at point x."""
    res = 0
    for i, c in enumerate(coeffs):
        res += c * (x ** i)
    return res

def coppersmith_univariate(poly_coeffs, N, m, X):
    """
    Coppersmith's method for finding small roots of modular polynomial equations.
    poly_coeffs: list of coefficients [a_0, a_1, ..., a_d] representing sum(a_i * x^i)
    N: Modulus
    m: Lattice parameter dimension
    X: Upper bound on the root
    """
    # Null polynomial trap
    if not poly_coeffs or all(c == 0 for c in poly_coeffs):
        raise ValueError("Null polynomial trap: Polynomial is zero or empty.")
        
    # Trim leading zeros
    while len(poly_coeffs) > 1 and poly_coeffs[-1] == 0:
        poly_coeffs.pop()
        
    d = len(poly_coeffs) - 1
    if d <= 0:
        raise ValueError("Polynomial degree must be at least 1.")

    # Modulus Shield
    if N <= 1:
        raise ValueError("Modulus Shield violation: N must be greater than 1.")

    # Root Bound Validation against theoretical ceiling: X < N^(1/d)
    theoretical_limit = N ** (1.0 / d)
    if X >= theoretical_limit:
        print(f"\n[WARNING] Root bound X ({X}) exceeds Coppersmith's theoretical ceiling N^(1/d) ({theoretical_limit:.4f}).")
        print("[WARNING] Lattice reduction cannot guarantee finding the roots, but proceeding with computation...\n")

    # Generate shift polynomials g_{i,j}(x) = x^j * N^(m-i) * f(x)^i
    # For simplicity, we use the standard triangular basis generation up to degree md.
    dimension = m * d + 1
    
    # Build polynomial matrix
    # We construct polynomials of degree up to dimension - 1
    basis_polynomials = []
    
    for i in range(m + 1):
        # N^(m-i) * f(x)^i
        # Compute f(x)^i
        f_pow = [1]
        for _ in range(i):
            # polynomial multiplication
            new_f = [0] * (len(f_pow) + len(poly_coeffs) - 1)
            for idx1, c1 in enumerate(f_pow):
                for idx2, c2 in enumerate(poly_coeffs):
                    new_f[idx1 + idx2] += c1 * c2
            f_pow = new_f
            
        scalar = N ** (m - i)
        scaled_poly = [c * scalar for c in f_pow]
        
        for j in range(d):
            if i * d + j < dimension:
                # shift by x^j
                shifted = [0] * j + scaled_poly
                # Pad to dimension size
                while len(shifted) < dimension:
                    shifted.append(0)
                basis_polynomials.append((i, j, shifted[:dimension]))

    # Construct coefficient matrix where columns correspond to powers x^k * X^k
    matrix = []
    for _, _, p in basis_polynomials:
        row = [p[k] * (X ** k) for k in range(len(p))]
        matrix.append(row)

    # Pad or square matrix if needed
    while len(matrix) < dimension:
        matrix.append([0] * dimension)
    matrix = matrix[:dimension]

    # Execute LLL Reduction
    reduced_basis = lll(matrix)

    # Extract shortest vector polynomial h(x)
    shortest_row = reduced_basis[0]
    
    # Unscale coefficients by dividing out X^k
    h_coeffs = [shortest_row[k] // (X ** k) if X > 0 else shortest_row[k] for k in range(len(shortest_row))]

    # Find integer roots of h(x) using bisection / integer search within [-X, X]
    roots = []
    # Test integer candidates around the interval [-X, X]
    step = max(1, int(X // 10000)) if X > 10000 else 1
    
    # Bounded search for integer roots
    current_x = -X
    while current_x <= X:
        val = evaluate_polynomial_coeffs(h_coeffs, current_x)
        if val == 0:
            if current_x not in roots:
                roots.append(current_x)
        current_x += 1

    # Verify roots over Z and modulo N
    valid_roots = []
    for r in roots:
        # Check f(r) == 0 mod N
        if evaluate_polynomial_coeffs(poly_coeffs, r) % N == 0:
            if r not in valid_roots:
                valid_roots.append(r)

    return valid_roots, h_coeffs

def run_coppersmith_cli():
    print("\n--- Coppersmith Engine: Small Roots of Modular Polynomials ---")
    try:
        deg = int(input("Enter polynomial degree (d): "))
        coeffs = []
        print(f"Enter coefficients from lowest degree (a_0) to highest degree (a_{deg}):")
        for i in range(deg + 1):
            c = int(input(f"  Coefficient a_{i}: "))
            coeffs.append(c)
            
        N = int(input("Enter modulus N: "))
        m = int(input("Enter lattice dimension parameter m (e.g., 2 or 3): "))
        X = int(input("Enter upper bound for the root (X): "))

        print("\n[+] Constructing lattice and executing LLL reduction...")
        roots, h_coeffs = coppersmith_univariate(coeffs, N, m, X)
        
        print("\n[+] Computation Complete.")
        print(f"Reconstructed integer polynomial h(x) coefficients: {h_coeffs}")
        if roots:
            print(f"[SUCCESS] Found valid integer root(s) satisfying f(x0) = 0 mod N: {roots}")
        else:
            print("[INFO] No small roots found within the specified bound X. Try increasing parameter m or bound X.")
    except Exception as e:
        print(f"\n[ERROR] Cryptanalytic Exception Encountered: {e}")

def run_rsa_attack_simulation():
    print("\n--- RSA Stereotyped Message Attack Simulation ---")
    print("Simulating vulnerable RSA encryption with low public exponent e = 3.")
    try:
        # Generate a small simulation RSA modulus for demonstration
        p = 1009
        q = 1013
        N = p * q
        e = 3
        
        print(f"Generated RSA Modulus N = p * q = {p} * {q} = {N}")
        print(f"Public Exponent e = {e}")
        
        secret_suffix = 123
        prefix_val = 456000  # e.g., known header padding
        # Total message m = prefix_val + secret_suffix
        m = prefix_val + secret_suffix
        print(f"[Simulation] True secret message: {m} (Prefix: {prefix_val}, Secret Suffix: {secret_suffix})")
        
        # Ciphertext C = m^e mod N
        C = pow(m, e, N)
        print(f"[Simulation] Encrypted Ciphertext C: {C}")
        
        print("\nSetting up Coppersmith attack to recover the secret suffix...")
        print(f"Polynomial equation: f(x) = (prefix + x)^e - C ≡ 0 (mod N)")
        print(f"Here, prefix = {prefix_val}, and suffix bound X = 1000")
        
        # f(x) = (prefix_val + x)^3 - C
        # Coefficients of (P + x)^3 = x^3 + 3Px^2 + 3P^2x + P^3 - C
        P = prefix_val
        poly_coeffs = [
            (P**3 - C) % N,
            (3 * (P**2)) % N,
            (3 * P) % N,
            1
        ]
        # Normalize or keep modulo N for constant term, others can be exact integers
        poly_coeffs = [
            P**3 - C,
            3 * (P**2),
            3 * P,
            1
        ]
        
        X = 1000  # bound on secret suffix
        m_param = 2
        
        print("[+] Executing Coppersmith Matrix Solver...")
        roots, _ = coppersmith_univariate(poly_coeffs, N, m_param, X)
        
        if roots:
            recovered_suffix = roots[0]
            recovered_message = prefix_val + recovered_suffix
            print(f"\n[SUCCESS] Secret suffix successfully extracted: {recovered_suffix}")
            print(f"[SUCCESS] Fully decrypted message: {recovered_message}")
        else:
            print("\n[FAILED] Could not extract root in simulation.")
            
    except Exception as e:
        print(f"\n[ERROR] RSA Simulation Exception: {e}")

def main():
    while True:
        print("\n==============================================")
        print("   CRYPTANALYTIC ENGINE & COPPERSMITH LABS    ")
        print("==============================================")
        print("1. Find small roots of a modular polynomial (Coppersmith Engine)")
        print("2. Execute an RSA Stereotyped Message Attack Simulation")
        print("3. Exit Cryptanalytic Engine")
        
        try:
            choice = input("Select an option [1-3]: ").strip()
            if choice == '1':
                run_coppersmith_cli()
            elif choice == '2':
                run_rsa_attack_simulation()
            elif choice == '3':
                print("\nShutting down Cryptanalytic Engine. Stay secure.")
                sys.exit(0)
            else:
                print("\n[ERROR] Invalid menu selection. Please choose 1, 2, or 3.")
        except KeyboardInterrupt:
            print("\n\nOperation interrupted by user. Exiting safely.")
            sys.exit(0)
        except Exception as e:
            print(f"\n[ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
