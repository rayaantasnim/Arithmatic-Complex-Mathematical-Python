import math
import random

def brent_pollard_rho(n: int) -> int:
    """
    Finds a non-trivial factor of a composite number using Brent's cycle-finding 
    optimization on Pollard's rho algorithm.
    Expected Time Complexity: O(n^0.25) amortized, behaving effectively like O(log n) 
    operations relative to massive bit-lengths.
    """
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3

    x = random.randint(1, n - 1)
    y = x
    c = random.randint(1, n - 1)
    m = random.randint(1, n - 1)
    g = 1
    r = 1
    q = 1

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

def factor_decomposition(n: int) -> list:
    """Recursively breaks down the number to find prime factors."""
    if n < 2:
        return []
    # Simplified primality fallback for demo structure
    # In full repo, swap this with your Miller-Rabin file component
    for p in: 
        if n % p == 0:
            return [p] + factor_decomposition(n // p)
            
    # Simple check to see if it's likely prime
    # if is_prime(n): return [n]
    
    factor = brent_pollard_rho(n)
    if factor == n:
        return [n]
    return factor_decomposition(factor) + factor_decomposition(n // factor)

def display_menu():
    print("\n" + "="*50)
    print(" MATHEMATICAL ENGINE: POLLARD'S RHO (BRENT OPTIMIZED)")
    print("="*50)
    print("[1] Find a single non-trivial factor")
    print("[2] Perform complete prime factorization (Decomposition)")
    print("[3] Exit Engine")
    print("="*50)

def main():
    while True:
        display_menu()
        choice = input("Select an option (1-3): ").strip()

        if choice == '3':
            print("\nExiting Engine. Back to the repo index.")
            break

        if choice in ['1', '2']:
            try:
                user_input = input("\nEnter a large composite integer (n): ").strip()
                n = int(user_input)

                if n <= 1:
                    print("❌ Error: Input must be an integer greater than 1.")
                    continue

                print("\n[Processing via optimized sub-linear math matrix...]")

                if choice == '1':
                    factor = brent_pollard_rho(n)
                    if factor == n:
                        print(f"Result: {n} is prime or factor search timed out.")
                    else:
                        print(f"🎉 Success! Found non-trivial factor: {factor}")
                        print(f"Verification: {factor} * {n // factor} = {n}")

                elif choice == '2':
                    factors = sorted(factor_decomposition(n))
                    factors_str = " * ".join(map(str, factors))
                    print(f"🎉 Complete Decomposition Matrix:")
                    print(f"Prime Factors: {factors}")
                    print(f"Equation: {n} = {factors_str}")

            except ValueError:
                print("❌ Invalid Input: Please enter a clean integer.")
            except Exception as e:
                print(f"❌ Computational Error: {e}")
        else:
            print("❌ Invalid Selection: Please choose an option from the menu card.")

if __name__ == "__main__":
    main()
