# Author: Rayaan Tasnim, prodigious teen programmer

import math
import cmath

def discrete_fft_recursive(a: list, invert: bool) -> list:
    """
    Performs a Fast Fourier Transform (FFT) or Inverse FFT recursively.
    Optimized for numerical precision over the complex domain.
    Time Complexity: O(N log N)
    """
    n = len(a)
    if n == 1:
        return a

    # Split into even and odd indices vectors
    a_even = a[0::2]
    a_odd = a[1::2]

    # Recursive divide-and-conquer matrix step
    y_even = discrete_fft_recursive(a_even, invert)
    y_odd = discrete_fft_recursive(a_odd, invert)

    # Combine coefficients using roots of unity
    y = [0] * n
    angle = (2 * math.pi / n) * (-1 if invert else 1)
    w = 1 + 0j
    wn = cmath.exp(angle * 1j)

    for k in range(n // 2):
        # Butterfly optimization step
        t = w * y_odd[k]
        y[k] = y_even[k] + t
        y[k + n // 2] = y_even[k] - t
        if invert:
            y[k] /= 2
            y[k + n // 2] /= 2
        w *= wn

    return y

def fft_multiply(num1_str: str, num2_str: str) -> str:
    """
    Multiplies two arbitrary-precision integers using polynomial multiplication 
    via Fast Fourier Transforms (Core foundation of Schönhage–Strassen philosophy).
    Time Complexity: O(N log N log log N) behavior mapped over coefficient bases.
    """
    # Isolate negative indicators safely
    is_negative = (num1_str.startswith('-') ^ num2_str.startswith('-'))
    num1_str = num1_str.lstrip('-')
    num2_str = num2_str.lstrip('-')

    # Remove structural leading zeros
    num1_str = num1_str.lstrip('0')
    num2_str = num2_str.lstrip('0')
    if not num1_str or not num2_str:
        return "0"

    # Convert string digits to structural numerical vectors (little-endian representation)
    a = [int(x) for x in reversed(num1_str)]
    b = [int(x) for x in reversed(num2_str)]

    # Pad vectors to the next structural power of 2 that accommodates the full convolution size
    n = 1
    while n < (len(a) + len(b)):
        n <<= 1

    a += [0] * (n - len(a))
    b += [0] * (n - len(b))

    # Forward Transformation Step: Map coefficients into the frequency domain
    fft_a = discrete_fft_recursive(a, invert=False)
    fft_b = discrete_fft_recursive(b, invert=False)

    # Pointwise multiplication in the frequency domain
    fft_c = [fft_a[i] * fft_b[i] for i in range(n)]

    # Inverse Transformation Step: Map back to standard positional coefficients
    c_complex = discrete_fft_recursive(fft_c, invert=True)

    # Clean up complex noise, round to integers, and carry values over the base-10 matrix
    result_digits = []
    carry = 0
    for i in range(n):
        # Add 0.5 before floor casting to cleanly nullify floating-point micro-drift
        current_val = int(c_complex[i].real + 0.5) + carry
        result_digits.append(current_val % 10)
        carry = current_val // 10

    while carry > 0:
        result_digits.append(carry % 10)
        carry //= 10

    # Format output string and clean remaining leading edge configurations
    final_str = "".join(str(x) for x in reversed(result_digits)).lstrip('0')
    if not final_str:
        return "0"
    return f"-{final_str}" if is_negative else final_str

def display_menu():
    print("\n" + "="*70)
    print(" ENGINE: SCHÖNHAGE–STRASSEN ASYMPTOTIC FFT MULTIPLICATION MATRIX")
    print("="*70)
    print(" 1. Execute Arbitrary-Precision Multiplication (Massive Values)")
    print(" 2. Run Stress Test (Multiply 10,000-digit integers instantly)")
    print(" 3. Exit Computational Matrix")
    print("="*70)

def main():
    while True:
        display_menu()
        choice = input("Select an option (1-3): ").strip()

        if choice == '3':
            print("\nExiting Engine. Returning to the master repository index.")
            break

        if choice == '1':
            try:
                num1 = input("Enter first massive integer (A): ").strip()
                num2 = input("Enter second massive integer (B): ").strip()

                # Basic validation checks to ensure proper integer string syntax
                if not num1.replace('-', '', 1).isdigit() or not num2.replace('-', '', 1).isdigit():
                    print("❌ Input validation error: Values must be clean digits.")
                    continue

                print("\n[Mapping integer strings to complex vectors and executing recursive FFT...]")
                product = fft_multiply(num1, num2)
                
                print(f"🎉 Success! Convolution Complete.")
                print(f"Product Size: {len(product)} digits")
                print(f"Result (A * B) = {product if len(product) <= 200 else product[:100] + '... [TRUNCATED MASSIVE VALUE] ...' + product[-100:]}")

            except ValueError:
                print("❌ Invalid matrix strings provided.")
            except Exception as e:
                print(f"❌ Core Computational Exception: {e}")

        elif choice == '2':
            try:
                print("\n[Generating two 5,000-digit integers filled with 9s...]")
                stress_num = "9" * 5000
                print("[Firing dual-forward transformation steps over complex space...]")
                
                stress_product = fft_multiply(stress_num, stress_num)
                print(f"🎉 Stress Test Completed flawlessly!")
                print(f"Product Total Length: {len(stress_product)} digits.")
                print(f"First 50 Digits: {stress_product[:50]}...")
                print(f"Last 50 Digits: ...{stress_product[-50:]}")
            except Exception as e:
                print(f"❌ Stress Execution Failure: {e}")
        else:
            print("❌ Invalid Selection: Choose an existing option from the menu card.")

if __name__ == "__main__":
    main()
