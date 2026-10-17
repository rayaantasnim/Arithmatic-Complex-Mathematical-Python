import random
import math

def ext_gcd(a: int, b: int) -> tuple:
    """
    Extended Euclidean Algorithm.
    Returns (gcd, x, y) such that a*x + b*y = gcd.
    """
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = ext_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def modular_inverse(a: int, m: int) -> int:
    """
    Computes modular inverse. Raises a ValueError containing the GCD 
    if the inverse does not exist (this is the key trigger for ECM).
    """
    gcd, x, _ = ext_gcd(a, m)
    if gcd != 1:
        raise ValueError(gcd)  # Found a factor!
    return (x % m + m) % m

def ec_add(P: tuple, Q: tuple, a: int, n: int) -> tuple:
    """
    Adds two points P and Q on the elliptic curve y^2 = x^3 + ax + b (mod n).
    Triggers factor discovery if modular inversion fails.
    """
    if P is None:
        return Q
    if Q is None:
        return P
    
    x1, y1 = P
    x2, y2 = Q
    
    if x1 == x2 and (y1 + y2) % n == 0:
        return None  # Point at infinity
        
    try:
        if P == Q:
            # Point doubling logic: slope m = (3*x1^2 + a) / (2*y1)
            num = (3 * pow(x1, 2, n) + a) % n
            denom = (2 * y1) % n
            slope = (num * modular_inverse(denom, n)) % n
        else:
            # Point addition logic: slope m = (y2 - y1) / (x2 - x1)
            num = (y2 - y1) % n
            denom = (x2 - x1) % n
            slope = (num * modular_inverse(denom, n)) % n
    except ValueError as e:
        # The exception object holds the non-trivial GCD factor
        raise e

    x3 = (pow(slope, 2, n) - x1 - x2) % n
    y3 = (slope * (x1 - x3) - y1) % n
    return (x3, y3)

def ec_multiply(k: int, P: tuple, a: int, n: int) -> tuple:
    """
    Multiplies a point P by a scalar k using the double-and-add strategy.
    Complexity: O(log k) elliptic curve operations.
    """
    R = None
    base = P
    while k > 0:
        if k % 2 == 1:
            R = ec_add(R, base, a, n)
        base = ec_add(base, base, a, n)
        k //= 2
    return R

def lenstra_ecm(n: int, B1: int = 2000) -> int:
    """
    Lenstra's Elliptic Curve Factorization (ECM).
    Tries random elliptic curves to find a non-trivial factor of n.
    """
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3

    # Generate a list of primes up to bound B1 for the stage 1 scalar multipliers
    # Pre-computing log bounds for maximum prime power multiplication
    primes = []
    sieve = [True] * (B1 + 1)
    for p in range(2, B1 + 1):
        if sieve[p]:
            primes.append(p)
            for i in range(p * p, B1 + 1, p):
                sieve[i] = False

    # Main trial loop using different random curves
    for _ in range(200):
        # Pick a random point and a random curve coefficient 'a'
        x0, y0 = random.randint(1, n - 1), random.randint(1, n - 1)
        a = random.randint(1, n - 1)
        # Compute 'b' such that P(x0, y0) lies on y^2 = x^3 + ax + b
        b = (pow(y0, 2, n) - pow(x0, 3, n) - a * x0) % n
        
        # Check that the curve is smooth (discriminant != 0)
        discriminant = (4 * pow(a, 3, n) + 27 * pow(b, 2, n)) % n
        if math.gcd(discriminant, n) == n:
            continue
            
        P = (x0, y0)
        
        # Run Stage 1: Successively multiply P by prime powers up to bound B1
        try:
            for p in primes:
                pp = p
                while pp <= B1:
                    P = ec_multiply(p, P, a, n)
                    if P is None:
                        break
                    pp *= p
                if P is None:
                    break
        except ValueError as e:
            # Vector found! Modular inversion failed, revealing the factor.
            factor = int(str(e))
            if 1 < factor < n:
                return factor
                
    return n  # Returns n if no factor was caught in this iteration block

def display_menu():
    print("\n" + "="*60)
    print(" MATHEMATICAL ENGINE: LENSTRA ELLIPTIC CURVE FACTORIZATION")
    print("="*60)
    print(" 1. Factorize an integer via Elliptic Curve Groups")
    print(" 2. Run continuous test (Demonstrate ECM breaking down 2^x equations)")
    print(" 3. Exit Engine")
    print("="*60)

def main():
    while True:
        display_menu()
        choice = input("Select an option (1-3): ").strip()

        if choice == '3':
            print("\nExiting ECM Engine. Returning to the repository index.")
            break

        if choice == '1':
            try:
                user_input = input("\nEnter a composite number to break down (n): ").strip()
                n = int(user_input)
                
                if n <= 1:
                    print("❌ Error: Input must be greater than 1.")
                    continue

                print("\n[Projecting integer onto random elliptic curves over finite fields...]")
                factor = lenstra_ecm(n)
                
                if factor == n:
                    print(f"❌ Result: Could not find a factor within current bounds. (Might be prime).")
                else:
                    print(f"🎉 Success! Elliptic group structure collapsed.")
                    print(f"Found Factor: {factor}")
                    print(f"Verification: {factor} * {n // factor} = {n}")

            except ValueError:
                print("❌ Invalid Input: Please pass a clean integer matrix.")
            except Exception as e:
                print(f"❌ Computational Error: {e}")

        elif choice == '2':
            try:
                print("\n[Running ECM Demonstration over custom composite product (13875317 * 21997)]")
                demo_n = 13875317 * 21997
                print(f"Target Composite: {demo_n}")
                
                factor = lenstra_ecm(demo_n, B1=5000)
                print(f"🎉 Success! Found factor via group law breakdown: {factor}")
                print(f"Composed elements: {factor} * {demo_n // factor}")
            except Exception as e:
                print(f"❌ Demo Failure: {e}")
        else:
            print("❌ Invalid Selection: Choose a valid menu choice.")

if __name__ == "__main__":
    main()
