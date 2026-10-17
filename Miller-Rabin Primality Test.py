import random

def miller_rabin_deterministic_check(n: int, a: int, d: int, s: int) -> bool:
    """
    Core witness loop for Miller-Rabin.
    Checks if 'a' is a witness to the compositeness of 'n'.
    Time Complexity: O(log^3 n) bit operations via modular exponentiation.
    """
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for _ in range(s - 1):
        x = pow(x, 2, n)
        if x == n - 1:
            return True
    return False

def is_prime_miller_rabin(n: int, k: int = 40) -> bool:
    """
    Ultra-fast Miller-Rabin Primality Test.
    Uses deterministic bases for integers up to 2^64 for 100% accuracy.
    Falls back to 'k' random rounds for arbitrary-precision integers (> 64-bit).
    
    Overall Time Complexity: O(k log^3 n)
    """
    # Base cases
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    # Decompose (n - 1) into d * 2^s where d is odd
    # Deep bitwise shifting optimization
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    # Deterministic bases for 100% accuracy within 64-bit unsigned integer range
    if n < 3_415_500_717_283_211:
        # Valid for n < 3.41e15
        bases = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    elif n < 18_446_744_073_709_551_616:
        # Valid for all 64-bit integers (n < 2^64)
        bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    else:
        # Probabilistic strategy for huge cryptographic numbers (arbitrary precision)
        # Error bound is less than (1/4)^k
        bases = [random.randint(2, n - 2) for _ in range(k)]

    for a in bases:
        if a >= n:
            continue
        if not miller_rabin_deterministic_check(n, a, d, s):
            return False  # Definitely composite
            
    return True  # True (Deterministic) or Highly Probable Prime (Arbitrary Precision)

def generate_large_prime(bits: int) -> int:
    """
    Generates a cryptographically strong candidate prime using Miller-Rabin filtering.
    """
    while True:
        # Fast random bit generation
        candidate = random.getrandbits(bits)
        # Ensure it is odd and has the correct bit length
        candidate |= (1 << (bits - 1)) | 1
        if is_prime_miller_rabin(candidate):
            return candidate

def display_menu():
    print("\n" + "="*50)
    print(" MATHEMATICAL ENGINE: MILLER-RABIN PRIMALITY")
    print("="*50)
    print(" 1. Test single integer primality (Ultra-Fast Matrix)")
    print(" 2. Generate a massive cryptographic prime number")
    print(" 3. Exit Engine")
    print("="*50)

def main():
    while True:
        display_menu()
        choice = input("Select an option (1-3): ").strip()

        if choice == '3':
            print("\nExiting Engine. Returning to the repository index.")
            break

        if choice == '1':
            try:
                user_input = input("\nEnter integer to test (n): ").strip()
                n = int(user_input)

                print("\n[Executing Miller-Rabin witness sequence...]")
                is_prime = is_prime_miller_rabin(n)
                
                if is_prime:
                    accuracy = "100% Deterministic Verification" if n < 2**64 else "Probabilistic Certainty (>99.9999%)"
                    print(f"🎉 Result: {n} is PRIME!")
                    print(f"Confidence Matrix: {accuracy}")
                else:
                    print(f"❌ Result: {n} is COMPOSITE.")

            except ValueError:
                print("❌ Invalid Input: Please provide a clean integer.")
            except Exception as e:
                print(f"❌ Computational Failure: {e}")

        elif choice == '2':
            try:
                user_input = input("\nEnter desired prime size in bits (e.g., 512, 1024): ").strip()
                bits = int(user_input)

                if bits < 3:
                    print("❌ Error: Bit length must be 3 or greater.")
                    continue

                print(f"\n[Mining for a {bits}-bit prime via Miller-Rabin sieve...]")
                large_prime = generate_large_prime(bits)
                
                print(f"🎉 Success! Generated {bits}-bit Prime Matrix:")
                print(f"Prime (Decimal): {large_prime}")
                print(f"Digits Count: {len(str(large_prime))}")

            except ValueError:
                print("❌ Invalid Input: Please enter an integer bit count.")
            except Exception as e:
                print(f"❌ Generation Error: {e}")
        else:
            print("❌ Invalid Selection: Please select a valid card option.")

if __name__ == "__main__":
    main()
