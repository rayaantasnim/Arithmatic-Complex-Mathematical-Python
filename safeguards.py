import math

class FactorFound(Exception):
    """
    Custom exception to cleanly pass non-trivial factors up the call stack
    without relying on risky string parsing or global states.
    """
    def __init__(self, factor: int):
        self.factor = factor
        super().__init__(f"Factor discovered: {factor}")

def mathematical_preflight(n: int) -> dict:
    """
    Performs deep pre-processing on an integer to trap mathematical edge cases.
    Returns a dictionary indicating status and immediate tactical actions.
    
    Time Complexity: O(log n) for perfect power testing, O(1) for basic checks.
    """
    # 1. Trivial Domain Boundaries
    if n <= 1:
        return {"status": "invalid", "message": "Domain error: Input must be an integer greater than 1."}
    
    # 2. Trivial Prime Matrix Checks
    if n in (2, 3, 5, 7):
        return {"status": "prime", "result": [n], "message": f"{n} is a known trivial prime."}
        
    if n % 2 == 0:
        return {"status": "composite", "factor": 2, "message": "Divisible by trivial prime: 2"}
    if n % 3 == 0:
        return {"status": "composite", "factor": 3, "message": "Divisible by trivial prime: 3"}
    if n % 5 == 0:
        return {"status": "composite", "factor": 5, "message": "Divisible by trivial prime: 5"}
    if n % 7 == 0:
        return {"status": "composite", "factor": 7, "message": "Divisible by trivial prime: 7"}

    # 3. Perfect Square Edge Case (Critical for Pollard's Rho and ECM)
    root = math.isqrt(n)
    if root * root == n:
        return {"status": "composite", "factor": root, "message": f"Input is a perfect square of {root}."}

    # 4. Perfect Power Edge Case Matrix (Checks n = p^k for k >= 3)
    # Uses bit length limits to check all possible integer roots efficiently
    max_k = n.bit_length()
    for k in range(3, max_k + 1):
        # Quick check: if k is even, it's a perfect square (already caught above)
        if k % 2 == 0:
            continue
            
        # Binary search for the exact kth root of n
        low = 2
        high = int(math.ceil(n ** (1.0 / k))) + 2
        found_root = -1
        
        while low <= high:
            mid = (low + high) // 2
            val = pow(mid, k)
            if val == n:
                found_root = mid
                break
            elif val < n:
                low = mid + 1
            else:
                high = mid - 1
                
        if found_root != -1:
            return {
                "status": "composite", 
                "factor": found_root, 
                "message": f"Input is a perfect power: {found_root}^{k}."
            }

    # 5. Passed all traps - clear for highly complex algorithmic processing
    return {"status": "clear", "message": "Input passed all edge-case checks. Safe for complex engine analysis."}
