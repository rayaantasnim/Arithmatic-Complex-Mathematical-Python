# Author: Rayaan Tasnim, prodigious teen programmer

import math
import sys

def check_perfect_power(n):
    """
    Intercepts perfect powers n = p^k. Returns the base root if found, else None.
    """
    if n <= 1:
        return None
    max_k = n.bit_length()
    for k in range(max_k, 1, -1):
        low = 1
        high = 1 << ((n.bit_length() + k - 1) // k)
        while low <= high:
            mid = (low + high) // 2
            val = mid ** k
            if val == n:
                return mid
            elif val < n:
                low = mid + 1
            else:
                high = mid - 1
    return None

def legendre_symbol(a, p):
    """
    Computes the Legendre symbol (a / p) using Euler's criterion.
    """
    if a % p == 0:
        return 0
    if p == 2:
        return 1 if (a % 8 == 1 or a % 8 == 7) else -1
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls

def get_primes_up_to(bound):
    """
    Generates a list of prime numbers up to the specified bound using a sieve of Eratosthenes.
    """
    if bound < 2:
        return []
    sieve = [True] * (bound + 1)
    sieve[0] = sieve[1] = False
    for start in range(2, int(math.isqrt(bound)) + 1):
        if sieve[start]:
            for i in range(start * start, bound + 1, start):
                sieve[false_idx := i] = False # standard indexing
    return [i for i, is_p in enumerate(sieve) if is_p]

def gaussian_elimination_gf2(matrix):
    """
    Performs Gaussian Elimination over GF(2) to find linear dependencies.
    matrix is a list of lists (rows of bits, augmented or simple).
    Returns list of dependency index lists.
    """
    if not matrix or not matrix[0]:
        return []
    
    nrows = len(matrix)
    ncols = len(matrix[0])
    
    # Track row operations to reconstruct dependencies
    # We will keep track of history as indices
    row_history = [[i] for i in range(nrows)]
    
    mat = [row[:] for row in matrix]
    
    lead = 0
    for r in range(nrows):
        if lead >= ncols:
            break
        i = r
        while not mat[i][lead]:
            i += 1
            if i == nrows:
                i = r
                lead += 1
                if lead == ncols:
                    return []
        
        mat[r], mat[i] = mat[i], mat[r]
        row_history[r], row_history[i] = row_history[i], row_history[r]
        
        for j in range(nrows):
            if j != r and mat[j][lead]:
                mat[j] = [mat[j][k] ^ mat[r][k] for k in range(ncols)]
                row_history[j] = row_history[j] + row_history[r] # XOR combination in history means symmetric difference
        lead += 1
        
    # Find zero rows in mat or rows with dependencies
    dependencies = []
    for r in range(nrows):
        if all(val == 0 for val in mat[r]):
            # Reduce history by counting item frequencies mod 2
            from collections import Counter
            counts = Counter(row_history[r])
            dep_indices = [idx for idx, count in counts.items() if count % 2 == 1]
            if dep_indices:
                dependencies.append(dep_indices)
    return dependencies

def quadratic_sieve(n, factor_base_bound=50, sieve_interval=1000):
    """
    Simplified Quadratic Sieve implementation.
    """
    if n <= 1:
        return None
    
    # Pre-processing checks
    if n % 2 == 0:
        return 2
    
    root_val = check_perfect_power(n)
    if root_val is not None:
        return root_val

    # 1. Construct Factor Base
    small_primes = get_primes_up_to(factor_base_bound)
    factor_base = []
    for p in small_primes:
        if p == 2:
            if n % 8 == 1:
                factor_base.append(p)
        else:
            if legendre_symbol(n, p) == 1:
                factor_base.append(p)
                
    if not factor_base:
        return None

    m = math.isqrt(n)
    
    # 2. Relation Sieving
    smooth_relations = [] # stores tuples: (x_val, Q_val, exponent_vector)
    
    # Simple trial division sieving across interval [-sieve_interval, sieve_interval]
    for x_offset in range(-sieve_interval, sieve_interval + 1):
        x = m + x_offset
        q_val = x * x - n
        if q_val <= 0:
            continue
        
        temp_val = q_val
        exp_vec = [0] * len(factor_base)
        
        # Factor over factor base
        is_smooth = True
        for idx, p in enumerate(factor_base):
            while temp_val % p == 0:
                exp_vec[idx] += 1
                temp_val //= p
                
        if temp_val == 1:
            smooth_relations.append((x, q_val, exp_vec))
            
        if len(smooth_relations) >= len(factor_base) + 5:
            break
            
    if len(smooth_relations) < len(factor_base):
        # Not enough relations found, expand interval or fail gracefully
        return None

    # 3. Exponent Vector Modulo 2 Matrix
    matrix_gf2 = [[val % 2 for val in rel[2]] for rel in smooth_relations]
    
    # Transpose for gaussian elimination (rows = factor base primes, cols = relations)
    # Actually, standard GF2 elimination for QS: rows = relations, cols = factor base primes.
    # Let's format matrix as rows = relations, cols = factor base primes (mod 2).
    # Wait, gaussian_elimination_gf2 expects rows = relations, cols = factor primes.
    
    deps = gaussian_elimination_gf2(matrix_gf2)
    
    for dep in deps:
        # Combine relations
        x_product = 1
        q_product_sum_vector = [0] * len(factor_base)
        
        for idx in dep:
            x_val, q_val, exp_vec = smooth_relations[idx]
            x_product = (x_product * x_val) % n
            for i in range(len(factor_base)):
                q_product_sum_vector[i] += exp_vec[i]
                
        # y = sqrt(product of Q(x)) mod n
        y = 1
        for i, exp in enumerate(q_product_sum_vector):
            y = (y * pow(factor_base[i], exp // 2, n)) % n
            
        # Check gcd(x_product - y, n)
        factor = math.gcd(abs(x_product - y), n)
        if 1 < factor < n:
            return factor
            
    return None

def run_benchmark():
    """
    Selection 2: Benchmark sieving matrix across smooth relations using a classic composite.
    """
    # Product of two 4-digit primes: 1009 * 1013 = 1022117
    composite = 1022117
    print(f"\n[BENCHMARK] Initiating Quadratic Sieve Benchmark on composite: {composite}")
    print(f"[BENCHMARK] Target decomposition: 1009 * 1013")
    
    bound = 60
    interval = 1500
    
    print(f"[BENCHMARK] Factor Base Bound: {bound}")
    print(f"[BENCHMARK] Sieving Interval: ±{interval}")
    
    small_primes = get_primes_up_to(bound)
    factor_base = [p for p in small_primes if p == 2 or legendre_symbol(composite, p) == 1]
    print(f"[BENCHMARK] Generated Factor Base (size {len(factor_base)}): {factor_base}")
    
    m = math.isqrt(composite)
    smooth_relations = []
    
    for x_offset in range(-interval, interval + 1):
        x = m + x_offset
        q_val = x * x - composite
        if q_val <= 0:
            continue
        temp_val = q_val
        exp_vec = [0] * len(factor_base)
        for idx, p in enumerate(factor_base):
            while temp_val % p == 0:
                exp_vec[idx] += 1
                temp_val //= p
        if temp_val == 1:
            smooth_relations.append((x, q_val, exp_vec))
            
    print(f"[BENCHMARK] Smooth relations collected: {len(smooth_relations)}")
    matrix_gf2 = [[val % 2 for val in rel[2]] for rel in smooth_relations]
    print(f"[BENCHMARK] Binary Matrix Dimensions: {len(matrix_gf2)} rows x {len(factor_base)} columns")
    
    if len(smooth_relations) >= len(factor_base):
        factor = quadratic_sieve(composite, factor_base_bound=bound, sieve_interval=interval)
        print(f"[BENCHMARK] Successfully extracted non-trivial factor: {factor}")
        if factor:
            other = composite // factor
            print(f"[BENCHMARK] Complete factorization: {composite} = {factor} * {other}")
    else:
        print("[BENCHMARK] Insufficient smooth relations gathered in this window. Try adjusting parameters.")
    print("-" * 60)

def main():
    while True:
        print("\n" + "="*50)
        print("   QUADRATIC SIEVE FACTORIZATION ENGINE (QS-FE)   ")
        print("="*50)
        print("1. Factorize a composite number using the Quadratic Sieve framework")
        print("2. Benchmark sieving matrix across smooth relations")
        print("3. Exit Sieve Engine")
        print("-" * 50)
        
        try:
            choice = input("Select an option (1-3): ").strip()
            if not choice:
                continue
                
            option = int(choice)
            
            if option == 1:
                num_str = input("Enter a positive composite integer to factorize: ").strip()
                n = int(num_str)
                
                if n <= 1:
                    print("Error: Domain validation failed. Input must be greater than 1.")
                    continue
                    
                print(f"[*] Processing integer {n}...")
                factor = quadratic_sieve(n)
                if factor and factor != n:
                    print(f"[+] Non-trivial factor found: {factor}")
                    print(f"[+] Cofactor: {n // factor}")
                else:
                    print("[-] Failed to extract a non-trivial factor with default parameters. Try larger bounds or benchmark mode.")
                    
            elif option == 2:
                run_benchmark()
                
            elif option == 3:
                print("[*] Exiting Sieve Engine. Goodbye!")
                break
            else:
                print("Error: Invalid choice. Please select 1, 2, or 3.")
                
        except ValueError as ve:
            print(f"[!] Input Error: Invalid numerical format entered. Details: {ve}")
        except Exception as e:
            print(f"[!] Computational Exception Encountered: {e}")

if __name__ == "__main__":
    main()
