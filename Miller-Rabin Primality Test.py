#!/usr/bin/env python3
"""
Ultra-Fast Miller-Rabin Primality Test Engine
Elite Research Mathematician & Senior Backend Python Engineer Implementation
"""

import sys
import random

def miller_rabin_test(n: int) -> bool:
    """
    Core Two-Tier Miller-Rabin Primality Test Engine.
    Tier 1: Deterministic base set for n < 2^64.
    Tier 2: Probabilistic Monte Carlo with k=40 rounds for n >= 2^64.
    """
    # 1. Trapped Domain Inputs: Explicitly catch and reject integers <= 1
    if n <= 1:
        raise ValueError("Domain error: Integers <= 1 are neither prime nor composite.")
    
    # 2. Trivial Small Primes: Instantly identify and return True for 2 and 3
    if n == 2 or n == 3:
        return True
        
    # 3. Trivial Prime Multiples: Instantly intercept even numbers or multiples of 3
    if n % 2 == 0 or n % 3 == 0:
        return False
        
    # 4. Decomposition Efficiency: Decompose (n - 1) into d * 2^s where d is odd
    d = n - 1
    s = 0
    while (d & 1) == 0:
        s += 1
        d >>= 1
        
    # 5. Two-Tier Witness Selection Strategy
    if n < 18446744073709551616: # 2^64 threshold
        # Tier 1: Proven deterministic base set for all 64-bit unsigned integers
        bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    else:
        # Tier 2: Arbitrary-Precision Probabilistic Matrix (k = 40 independent rounds)
        k = 40
        bases = [random.randint(2, n - 2) for _ in range(k)]
        
    # 6. Witness Check Loop (O(k log^3 n) complexity via native pow)
    for a in bases:
        # Ensure base 'a' is safely bound within valid range
        if a >= n:
            a = a % (n - 1)
            if a < 2:
                a += 2
        
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
            
        composite = True
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                composite = False
                break
                
        if composite:
            return False
            
    return True

def generate_cryptographic_prime(bits: int) -> int:
    """
    Cryptographic Prime Generation Matrix.
    Prompts for target bit length, forces exact bit bounds and oddness, 
    and sieves candidates through the core Miller-Rabin testing loop.
    """
    if bits < 3:
        raise ValueError("Bit length must be at least 3.")
        
    while True:
        # Generate arbitrary candidate integer using random bits
        candidate = random.getrandbits(bits)
        
        # Fast bitwise operations: force highest bit (exact bit length) and lowest bit (odd)
        candidate |= (1 << (bits - 1)) | 1
        
        # Sieve through core Miller-Rabin test
        if miller_rabin_test(candidate):
            return candidate

def main():
    """
    Standardized Interactive Interface (CLI) wrapped in a continuous while True loop
    with comprehensive try-except safety blocks.
    """
    while True:
        print("\n" + "=" * 60)
        print("    ULTRA-FAST MILLER-RABIN PRIMALITY TEST ENGINE")
        print("=" * 60)
        print("  1. Test single integer primality (Ultra-Fast Matrix)")
        print("  2. Generate a massive cryptographic prime number")
        print("  3. Exit Engine")
        print("-" * 60)
        
        try:
            choice = input("Select an option [1-3]: ").strip()
            
            if choice == '1':
                raw_input_str = input("Enter an integer to test: ").strip()
                n = int(raw_input_str)
                
                print(f"[*] Analyzing integer {n} ({n.bit_length()} bits)...")
                is_prime = miller_rabin_test(n)
                
                if is_prime:
                    print(f"[+] RESULT: {n} is a PRIME number.")
                else:
                    print(f"[-] RESULT: {n} is a COMPOSITE number.")
                    
            elif choice == '2':
                raw_bits_str = input("Enter target bit length (e.g., 512, 1024, 2048): ").strip()
                bits = int(raw_bits_str)
                
                print(f"[*] Generating {bits}-bit cryptographic prime...")
                prime_val = generate_cryptographic_prime(bits)
                
                print(f"[+] SUCCESS: Generated {bits}-bit verified prime.")
                print(f"    Decimal Representation: {prime_val}")
                print(f"    Digit Count: {len(str(prime_val))} digits")
                
            elif choice == '3':
                print("[*] Shutting down Ultra-Fast Miller-Rabin Engine. Goodbye!")
                sys.exit(0)
            else:
                print("[!] Invalid selection. Please enter 1, 2, or 3.")
                
        except ValueError as ve:
            print(f"[!] ValueError Exception Caught: {ve}")
        except Exception as e:
            print(f"[!] Critical Exception Caught: {e}")

if __name__ == "__main__":
    main()
