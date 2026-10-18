# Author: Rayaan Tasnim, prodigious teen programmer

import random
import sys

def is_prime(n, k=5):
    """Miller-Rabin primality test to verify modulus p."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
        
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

def prime_factors(n):
    """Factor n into prime powers: returns dict {prime: exponent}."""
    factors = {}
    d = 2
    while d * d <= n:
        while (n % d) == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors

def extended_gcd(a, b):
    """Extended Euclidean Algorithm for modular inverse."""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    """Computes modular inverse of a modulo m."""
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"Modular inverse does not exist for {a} modulo {m}")
    return (x % m + m) % m

def chinese_remainder_theorem(remainders, moduli):
    """Solves system of congruences x = remainders[i] mod moduli[i] using CRT."""
    total_modulus = 1
    for m in moduli:
        total_modulus *= m
    
    x = 0
    for r, m in zip(remainders, moduli):
        mi = total_modulus // m
        yi = mod_inverse(mi, m)
        x += r * mi * yi
    return x % total_modulus, total_modulus

def baby_step_giant_step(g, h, q, p):
    """Solves g^x = h mod p where order divides q (subgroup order solver)."""
    for x in range(q):
        if pow(g, x, p) == h:
            return x
    raise ValueError(f"Discrete logarithm not found in subgroup of order {q}")

def pohlig_hellman(g, h, p):
    """
    Computes discrete logarithm x such that g^x == h mod p 
    using the Pohlig-Hellman algorithm and Chinese Remainder Theorem.
    """
    N = p - 1
    factors = prime_factors(N)
    
    remainders = []
    moduli = []
    
    for q, e in factors.items():
        q_e = q ** e
        x_val = 0
        
        # Digit-by-digit extraction for prime power q^e
        for k in range(e):
            power_val = N // (q ** (k + 1))
            gamma = pow(g, N // q, p)
            
            inv_g_x = mod_inverse(pow(g, x_val, p), p)
            hk_base = (h * inv_g_x) % p
            hk = pow(hk_base, power_val, p)
            
            xk = baby_step_giant_step(gamma, hk, q, p)
            x_val += xk * (q ** k)
            
        remainders.append(x_val)
        moduli.append(q_e)
        
    x, total_mod = chinese_remainder_theorem(remainders, moduli)
    return x

def main_menu():
    print("=" * 65)
    print(" POHLIG-HELLMAN DISCRETE LOGARITHM ENGINE & CRYPTANALYSIS ")
    print("=" * 65)
    print("1. Solve discrete logarithm problem (g^x == h mod p)")
    print("2. Run cryptographic vulnerability demonstration (Smooth group)")
    print("3. Exit Logarithm Engine")
    print("-" * 65)

def run():
    while True:
        main_menu()
        choice = input("Select option (1-3): ").strip()
        
        if choice == '3':
            print("Exiting Logarithm Engine. Goodbye!")
            break
            
        elif choice == '1':
            try:
                p_str = input("Enter prime modulus p: ").strip()
                g_str = input("Enter base g: ").strip()
                h_str = input("Enter target h: ").strip()
                
                p = int(p_str)
                g = int(g_str)
                h = int(h_str)
                
                # Modulus Primality Shield
                if not is_prime(p):
                    raise ValueError(f"Modulus p = {p} is NOT prime! Invalid cyclic group input.")
                
                g = g % p
                h = h % p
                
                if g == 0:
                    raise ValueError("Base g cannot be 0 mod p.")
                if h == 0:
                    raise ValueError("Target h cannot be 0 mod p.")
                
                # Identity Traps
                if h == 1:
                    x = 0
                    print("[Identity Trap] h == 1 detected. Direct solution: x = 0")
                elif h == g:
                    x = 1
                    print("[Identity Trap] h == g detected. Direct solution: x = 1")
                else:
                    print("[*] Deconstructing group order (p - 1) and executing Pohlig-Hellman...")
                    x = pohlig_hellman(g, h, p)
                
                # Post-Computation Verification
                print(f"[*] Verifying solution: pow({g}, {x}, {p}) == {h} ...")
                if pow(g, x, p) == h:
                    print(f"[SUCCESS] Discrete logarithm computed successfully!")
                    print(f"          x = {x}\n")
                else:
                    print("[ERROR] Verification failed! Computed x does not satisfy g^x == h mod p.\n")
                    
            except Exception as e:
                print(f"[ERROR] Exception caught: {e}")
                print("[!] Returning to main menu safely.\n")
                
        elif choice == '2':
            print("\n--- Cryptanalytic Vulnerability Demonstration (Smooth Group) ---")
            print("Constructing a smooth group where p - 1 factors entirely into small primes...")
            
            # Smooth base factor product (e.g., 2^6 * 3^3 * 5^2 = 43200)
            smooth_base = (2**6) * (3**3) * (5**2)
            candidate_p = None
            for k in range(1, 2000):
                cand = k * smooth_base + 1
                if is_prime(cand):
                    candidate_p = cand
                    break
            
            if not candidate_p:
                print("[ERROR] Failed to construct smooth prime for demonstration.\n")
                continue
                
            p = candidate_p
            print(f"[*] Generated smooth prime modulus p = {p}")
            print(f"[*] Group order p - 1 = {p - 1}")
            print(f"[*] Prime factor decomposition of (p - 1): {prime_factors(p - 1)}")
            
            g = 2
            while pow(g, (p - 1) // 2, p) == 1:
                g += 1
                
            secret_x = random.randint(1000, p - 2)
            h = pow(g, secret_x, p)
            
            print(f"[*] Assigned secret private exponent x = {secret_x}")
            print(f"[*] Public target h = g^x mod p = {h}")
            print("[*] Launching Pohlig-Hellman attack on smooth group...")
            
            recovered_x = pohlig_hellman(g, h, p)
            print(f"[SUCCESS] Vulnerability demonstrated! Extracted secret x = {recovered_x}")
            
            if pow(g, recovered_x, p) == h:
                print(f"[VERIFIED] Cryptanalytic attack successful: pow(g, recovered_x, p) == h holds true!\n")
            else:
                print(f"[ERROR] Attack verification failed.\n")
            
        else:
            print("[!] Invalid choice. Please select 1, 2, or 3.\n")

if __name__ == "__main__":
    run()
