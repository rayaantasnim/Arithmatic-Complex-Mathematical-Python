#!/usr/bin/env python3
# Author: Rayaan Tasnim, prodigious teen programmer
"""
Berlekamp–Massey Algorithm for Linear Feedback Shift Register (LFSR) Synthesis
High-Complexity Cryptographic and Signal Processing Engine over GF(2)
"""

import sys

def berlekamp_massey(sequence):
    """
    Implements the Berlekamp-Massey algorithm over GF(2) to find the minimal
    connection polynomial and linear complexity of a binary sequence.
    """
    # Trivial Stream Trap: All-zero sequence check
    if not any(sequence):
        return 0, [1]

    n = len(sequence)
    # C(x): Current connection polynomial, initialized to [1]
    c = [1]
    # B(x): Correction polynomial tracking the last structural change, initialized to [1]
    b = [1]
    # L: Linear complexity tracking the current minimal register size, initialized to 0
    L = 0
    # m: Step index iteration tracker since the last modification shift, initialized to 1
    m = 1

    for i in range(n):
        # Calculate discrepancy d = (S_i + c_1*S_{i-1} + ... + c_L*S_{i-L}) mod 2
        d = sequence[i]
        for j in range(1, len(c)):
            if i - j >= 0:
                d ^= (c[j] & sequence[i - j])

        if d == 0:
            m += 1
        else:
            # Polynomial update step: C(x) = C(x) + B(x) * x^m mod 2
            term = [0] * m + b
            max_len = max(len(c), len(term))
            c_padded = c + [0] * (max_len - len(c))
            term_padded = term + [0] * (max_len - len(term))
            
            new_c = [(c_padded[k] ^ term_padded[k]) & 1 for k in range(max_len)]
            
            # Complex condition shift check
            if 2 * L <= i:
                b = list(c)
                L = i + 1 - L
                m = 1
            else:
                m += 1
            c = new_c

    return L, c

def simulate_lfsr(connection_poly, initial_state, num_bits):
    """
    Simulates a virtual LFSR using the extracted connection polynomial 
    to predict subsequent bits in a stream cipher.
    connection_poly: list of coefficients [c_0, c_1, ..., c_L] where c_0 = 1
    initial_state: the seed state (most recent bits)
    """
    taps = connection_poly[1:]
    register = list(initial_state)
    predicted = []

    for _ in range(num_bits):
        # Compute next bit using feedback taps over GF(2)
        next_bit = 0
        for t, bit in enumerate(register[-len(taps):]):
            next_bit ^= (taps[t] & bit)
        predicted.append(next_bit)
        register.pop(0)
        register.append(next_bit)

    return predicted

def validate_binary_sequence(seq_str):
    """
    Validates input sequence against Non-Binary Guard and Sequence Length Shield.
    """
    if not seq_str:
        raise ValueError("Sequence Length Shield: Input sequence cannot be empty.")
    for char in seq_str:
        if char not in ('0', '1'):
            raise ValueError(f"Non-Binary Guard: Invalid character '{char}' detected. Sequence must contain only binary digits (0 or 1).")
    return [int(char) for char in seq_str]

def main_menu():
    print("\n" + "="*70)
    print("   BERLEKAMP-MASSEY LFSR SYNTHESIS & CRYPTANALYSIS ENGINE")
    print("="*70)
    print("1. Analyze a custom binary sequence (Extract minimal connection polynomial)")
    print("2. Predict next bits of a stream-cipher sequence using synthesized LFSR")
    print("3. Exit Cipher Engine")
    print("-" * 70)

def run():
    while True:
        try:
            main_menu()
            choice = input("Select an option (1-3): ").strip()
            
            if choice == '1':
                seq_input = input("Enter binary sequence (e.g., 101101): ").strip()
                sequence = validate_binary_sequence(seq_input)
                
                print("\n[+] Executing Berlekamp-Massey Synthesis over GF(2)...")
                linear_complexity, connection_poly = berlekamp_massey(sequence)
                
                print(f"-> Input Sequence Length: {len(sequence)}")
                print(f"-> Linear Complexity (L): {linear_complexity}")
                print(f"-> Connection Polynomial C(x): {connection_poly}")
                
                poly_str = " + ".join([f"x^{j}" if j > 0 else "1" for j, val in enumerate(connection_poly) if val == 1])
                print(f"-> Algebraic Form C(x) = {poly_str}")

            elif choice == '2':
                seq_input = input("Enter stream-cipher key stream chunk (binary string): ").strip()
                sequence = validate_binary_sequence(seq_input)
                
                if len(sequence) < 4:
                    print("[-] Warning: Short streams may yield trivial or highly constrained linear systems.")
                
                bits_to_predict_str = input("Enter number of subsequent bits to predict: ").strip()
                if not bits_to_predict_str.isdigit() or int(bits_to_predict_str) <= 0:
                    raise ValueError("Prediction count must be a positive integer.")
                num_predict = int(bits_to_predict_str)

                print("\n[+] Synthesizing LFSR and breaking linear cipher structure...")
                linear_complexity, connection_poly = berlekamp_massey(sequence)
                print(f"-> Discovered Linear Complexity (L): {linear_complexity}")
                print(f"-> Discovered Connection Polynomial: {connection_poly}")

                if linear_complexity == 0:
                    print("[-] Sequence is trivial (all zeros). Predicted bits will be all 0.")
                    predicted = [0] * num_predict
                else:
                    seed_state = sequence[-linear_complexity:] if len(sequence) >= linear_complexity else sequence + [0] * (linear_complexity - len(sequence))
                    predicted = simulate_lfsr(connection_poly, seed_state, num_predict)

                print(f"-> Next {num_predict} Predicted Bits: {''.join(map(str, predicted))}")

            elif choice == '3':
                print("\n[*] Shutting down Cipher Engine. Cryptographic session terminated cleanly.")
                sys.exit(0)
            else:
                print("[-] Invalid selection. Please choose an option between 1 and 3.")

        except ValueError as ve:
            print(f"\n[!] Input/Validation Error: {ve}")
        except Exception as e:
            print(f"\n[!] Unexpected Error Encountered: {e}")
        
        input("\nPress Enter to return to the menu...")

if __name__ == "__main__":
    run()
