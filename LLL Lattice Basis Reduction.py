# Author: Rayaan Tasnim, prodigious teen programmer

import sys
import math
from fractions import Fraction

def exact_round(frac):
    """
    Computes exact round-to-nearest for a Fraction object.
    Ties are rounded away from zero (standard Python rounding behavior).
    """
    num = frac.numerator
    den = frac.denominator
    if den == 0:
        return 0
    sign = 1 if num * den >= 0 else -1
    num_abs = abs(num)
    den_abs = abs(den)
    res = (2 * num_abs + den_abs) // (2 * den_abs)
    return sign * res

def vector_dot(u, v):
    """Computes the exact inner product of two vectors."""
    return sum(x * y for x, y in zip(u, v))

def vector_norm_sq(u):
    """Computes the squared Euclidean norm of a vector."""
    return vector_dot(u, u)

def validate_basis(basis):
    """
    Global Matrix Safeguards & Geometric Pre-flight Interception:
    Validates input structure, dimension consistency, and integer types.
    """
    if not isinstance(basis, list) or len(basis) == 0:
        raise ValueError("Basis must be a non-empty list of vectors (rows).")
    
    dim = len(basis[0])
    if dim == 0:
        raise ValueError("Basis vectors cannot be empty.")
        
    for i, row in enumerate(basis):
        if not isinstance(row, list):
            raise ValueError(f"Row {i} is not a valid list vector.")
        if len(row) != dim:
            raise ValueError(f"Dimension mismatch: Row {i} has length {len(row)}, expected {dim}.")
        for val in row:
            if not isinstance(val, (int, float, Fraction)):
                raise ValueError(f"Invalid element '{val}' at row {i}. All entries must be numbers.")

def compute_gso(b):
    """
    Computes the Gram-Schmidt orthogonalization and GSO coefficients (mu)
    using exact rational arithmetic (fractions.Fraction).
    """
    n = len(b)
    dim = len(b[0])
    b_star = []
    mu = [[Fraction(0)] * n for _ in range(n)]
    norm_b_star_sq = [Fraction(0)] * n
    
    for i in range(n):
        bi_star = list(b[i])
        for j in range(i):
            if norm_b_star_sq[j] == 0:
                raise ValueError("Linearly dependent basis vectors detected: zero norm encountered in Gram-Schmidt orthogonalization.")
            mu[i][j] = vector_dot(b[i], b_star[j]) / norm_b_star_sq[j]
            bi_star = [bi_star[k] - mu[i][j] * b_star[j][k] for k in range(dim)]
        
        ns = vector_norm_sq(bi_star)
        if ns == 0:
            raise ValueError("Linearly dependent basis vectors detected: linearly dependent row span results in zero vector.")
        norm_b_star_sq[i] = ns
        b_star.append(bi_star)
        
    return b_star, mu, norm_b_star_sq

def lll_reduce(basis, delta=Fraction(3, 4)):
    """
    Executes the Lenstra–Lenstra–Lovász (LLL) Lattice Basis Reduction Algorithm.
    Guaranteed numerical stability via exact rational arithmetic and robust safeguards.
    """
    validate_basis(basis)
    
    n = len(basis)
    dim = len(basis[0])
    
    # Convert input matrix into exact Fraction objects
    b = [[Fraction(x) for x in row] for row in basis]
    
    try:
        b_star, mu, norm_b_star_sq = compute_gso(b)
    except Exception as e:
        raise ValueError(f"Geometric pre-flight interception error: {e}")
        
    k = 1
    while k < n:
        # Step 1: Size-Reduction Step
        for j in range(k - 1, -1, -1):
            x = exact_round(mu[k][j])
            if x != 0:
                b[k] = [b[k][l] - x * b[j][l] for l in range(dim)]
                b_star, mu, norm_b_star_sq = compute_gso(b)
                
        # Step 2: Lovász Condition Check
        # ||b_k* + mu[k][k-1] b_{k-1}*||^2 >= delta * ||b_{k-1}*||^2
        lhs = norm_b_star_sq[k] + (mu[k][k - 1] ** 2) * norm_b_star_sq[k - 1]
        rhs = delta * norm_b_star_sq[k - 1]
        
        if lhs >= rhs:
            k += 1
        else:
            # Swap adjacent basis vectors
            b[k], b[k - 1] = b[k - 1], b[k]
            b_star, mu, norm_b_star_sq = compute_gso(b)
            k = max(k - 1, 1)
            
    # Format output back to clean integers where possible
    return [[int(x) if x.denominator == 1 else float(x) for x in row] for row in b]

def interactive_arbitrary_reduction():
    print("\n--- Arbitrary Integer Lattice Basis Reduction ---")
    num_rows = int(input("Enter number of basis vectors (dimension n): "))
    basis = []
    print("Enter each vector row-by-row with coordinates separated by commas:")
    for i in range(num_rows):
        row_input = input(f"Vector {i+1}: ")
        row = [int(val.strip()) for val in row_input.split(",")]
        basis.append(row)
        
    print("\nRunning LLL reduction...")
    reduced_basis = lll_reduce(basis)
    
    print("\n[SUCCESS] Reduced Lattice Basis:")
    for row in reduced_basis:
        print(row)

def interactive_knapsack_attack():
    print("\n--- Subset-Sum / Knapsack Cryptosystem Breaking Matrix (Lagarias-Odlyzko) ---")
    weights_str = input("Enter knapsack weights separated by commas (e.g., 11, 23, 45, 92, 181, 357): ")
    weights = [int(w.strip()) for w in weights_str.split(",")]
    target = int(input("Enter target sum S: "))
    
    n = len(weights)
    # Scaling factor for Lagarias-Odlyzko matrix construction
    N = max(weights) * n + 1
    
    # Constructing the (n+1) x (n+1) subset-sum lattice basis matrix
    matrix = []
    for i in range(n):
        row = [0] * (n + 1)
        row[i] = 2
        row[n] = N * weights[i]
        matrix.append(row)
        
    last_row = [1] * n + [N * target]
    matrix.append(last_row)
    
    print("\nConstructed Lagarias-Odlyzko lattice matrix. Running LLL reduction...")
    reduced = lll_reduce(matrix)
    
    print("\n[SUCCESS] Reduced Matrix Output:")
    for row in reduced:
        print(row)
        
    print("\nAnalysis: Shortest vectors in the transformed space reveal structural relations corresponding to the subset-sum solution vector.")

def main_cli():
    while True:
        print("\n==================================================")
        print("     ADVANCED LLL LATTICE BASIS REDUCTION ENGINE")
        print("==================================================")
        print("1. Reduce an arbitrary integer lattice basis matrix")
        print("2. Execute standard knapsack cryptosystem/subset-sum breaking matrix")
        print("3. Exit Engine")
        print("--------------------------------------------------")
        
        choice = input("Select an option (1-3): ").strip()
        
        try:
            if choice == "1":
                interactive_arbitrary_reduction()
            elif choice == "2":
                interactive_knapsack_attack()
            elif choice == "3":
                print("\nExiting LLL Engine. Goodbye!")
                sys.exit(0)
            else:
                print("\n[ERROR] Invalid choice. Please select 1, 2, or 3.")
        except Exception as e:
            print(f"\n[CRITICAL EXCEPTION CAUGHT] Operation failed safely: {e}")
            print("Returning to main menu prompt...")

if __name__ == "__main__":
    main_cli()
