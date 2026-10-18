# 🧠 Computational Matrix: Elite Mathematical Algorithms in Python

**Computational Matrix** is an enterprise-grade suite of 15 highly optimized, production-ready, interactive command-line interface (CLI) algorithm engines written in pure Python. Engineered for deep exploration in high-complexity number theory, abstract cryptography, algebraic geometry, lattice theory, and advanced graph algorithms, this library provides precise mathematical implementations capable of handling multi-precision integer arithmetic and complex structures.

Every algorithm in the suite integrates a centralized pre-flight shield module (`safeguards.py`). This module acts as an automated validation barrier, gracefully intercepting mathematical edge cases, domain errors, non-prime modulus exceptions, perfect powers, and trivial factors before engine initialization, guaranteeing complete execution stability.

---

## 📐 Global Architecture & Repo Blueprint

The table below outlines the core mathematical paradigms implemented in this matrix along with their respective amortized asymptotic time complexities.

| Core Mathematical Algorithm | Amortized Time Complexity |
| :--- | :--- |
| **Brent's Optimized Pollard's Rho Factorization** | $\mathcal{O}(n^{0.25})$ |
| **Two-Tier Deterministic & Probabilistic Miller-Rabin Primality Test** | $\mathcal{O}(k \log^3 n)$ |
| **Lenstra Elliptic Curve Factorization Engine (ECM)** | $\mathcal{O}(\exp(\sqrt{(2+o(1)) \ln p \ln \ln p}))$ |
| **Schönhage–Strassen Asymptotic FFT Multiplication Matrix** | $\mathcal{O}(N \log N \log \log N)$ |
| **Lenstra–Lenstra–Lovász Lattice Basis Reduction (LLL)** | $\mathcal{O}(d^5 \log^3 B)$ |
| **Schoof's Point-Counting Algorithm for Elliptic Curves** | $\mathcal{O}(\log^8 p)$ |
| **Coppersmith's Method via LLL Modular Root Finder** | $\text{Poly}(\log N, d)$ |
| **Berlekamp–Massey LFSR Linear Complexity Synthesis** | $\mathcal{O}(N^2)$ |
| **Quadratic Sieve Sub-Exponential Factorization Framework** | $\mathcal{O}(\exp(\sqrt{\ln n \ln \ln n}))$ |
| **Pohlig-Hellman Smooth Cyclic Group Logarithm Solver** | $\mathcal{O}\left(\sum e_i \sqrt{q_i}\right)$ |
| **Shanks' Tonelli-Shanks Modular Square Root Solver** | $\mathcal{O}(s^2 \log p)$ |
| **Hopcroft-Karp Bipartite Matching Optimizer** | $\mathcal{O}(E \sqrt{V})$ |
| **Tarjan's Linear-Time Strongly Connected Components Matrix** | $\mathcal{O}(V + E)$ |
| **Standard Pollard's Rho Factorization Variant** | $\mathcal{O}(\sqrt{p})$ |
| **Standard Brent's Cycle Detection Benchmark** | $\mathcal{O}(\lambda + \mu)$ |

---

## 🔬 Domain Profile Drilldown

### 📂 Core Number Theory & Factorization Engines

<details>
<summary><b>1. Brent's Optimized Pollard's Rho Factorization</b></summary>

<br>

* **Mathematical Overview:** An enhancement of Pollard's $\rho$ algorithm incorporating Richard Brent's cycle-finding strategy. Replaces Floyd's tortoise-and-hare algorithm with a powers-of-two sliding step window and batch gcd accumulators, drastically reducing the number of costly greatest common divisor calculations.
* **Console Inputs:** Target composite integer $N$ ($N > 1$).
* **Console Outputs:** Non-trivial prime factor $p$ dividing $N$, total iteration count, and polynomial shift parameter $c$.
* **Corner Case Resilience:** Intercepts small primes, prime powers $N = p^k$, and even numbers via `safeguards.py` prior to loop entry, preventing infinite loops on prime or square inputs.
</details>

<details>
<summary><b>2. Two-Tier Deterministic & Probabilistic Miller-Rabin Primality Test</b></summary>

<br>

* **Mathematical Overview:** Evaluates primality by writing $n - 1 = 2^s \cdot d$ and testing witness conditions $a^d \equiv 1 \pmod n$ or $a^{2^r d} \equiv -1 \pmod n$. Uses deterministic base sets for 64-bit integers and configurable pseudo-random witness iterations for arbitrary-precision integers.
* **Console Inputs:** Candidate integer $n$, target confidence parameter $k$ (for probabilistic checks).
* **Console Outputs:** Boolean primality verdict, deterministic/probabilistic classification mode, and strong witness composite proof (if composite).
* **Corner Case Resilience:** Handles $n \le 3$, even integers, negative integers, and perfect squares gracefully through pre-flight filtering.
</details>

<details>
<summary><b>3. Lenstra Elliptic Curve Factorization Engine (ECM)</b></summary>

<br>

* **Mathematical Overview:** Computes scalar multiplication of points on random elliptic curves over $\mathbb{Z}/N\mathbb{Z}$ via Weierstrass parameters $y^2 = x^3 + ax + b$. Factorization succeeds when a slope calculation fails due to a non-invertible denominator $\pmod N$, yielding a non-trivial factor via $\gcd(\text{denom}, N)$.
* **Console Inputs:** Target integer $N$, stage 1 bound $B_1$, stage 2 bound $B_2$, maximum curve attempts.
* **Console Outputs:** Discovered non-trivial factor, singular elliptic curve parameters $(a, b, P_0)$, and curve evaluation count.
* **Corner Case Resilience:** Filters out prime inputs, perfect powers, and inputs with $\gcd(6, N) > 1$ before curve generation.
</details>

<details>
<summary><b>4. Standard Pollard's Rho Factorization Variant</b></summary>

<br>

* **Mathematical Overview:** Employs Floyd's cycle-detection mechanism ($x_{i+1} = (x_i^2 + c) \pmod N$) with dual pointers advancing at differential speeds ($x$ step 1, $y$ step 2) to identify periodicities modulo unknown factors of $N$.
* **Console Inputs:** Composite candidate $N$, initial polynomial seed $x_0$, polynomial constant $c$.
* **Console Outputs:** Extracted non-trivial factor $d = \gcd(|x - y|, N)$, iteration count.
* **Corner Case Resilience:** Automatically resets polynomial parameter $c$ when sequence collapses into trivial cycles or prime inputs are passed.
</details>

<details>
<summary><b>5. Standard Brent's Cycle Detection Benchmark</b></summary>

<br>

* **Mathematical Overview:** Pure functional implementation of Brent's cycle-finding algorithm for functional mapping $f: S \to S$. Computes exact sequence periodicity $\lambda$ (cycle length) and memory offset $\mu$ (tail length) using $2^i$ step sizing.
* **Console Inputs:** Arbitrary iterative function mapping parameter, initial sequence seed $x_0$.
* **Console Outputs:** Tail length $\mu$, cycle period length $\lambda$, first element of cycle repetition.
* **Corner Case Resilience:** Safely handles identity mappings, non-periodic fixed points, and instantaneous cycles ($\lambda = 1$).
</details>

---

### 📂 Cryptanalytic Math & Lattice Geometry

<details>
<summary><b>1. Lenstra–Lenstra–Lovász Lattice Basis Reduction (LLL)</b></summary>

<br>

* **Mathematical Overview:** Reduces an arbitrary linearly independent basis $B = \{b_1, b_2, \dots, b_d\} \subset \mathbb{Z}^n$ into a geometrically nearly-orthogonal Lovász-reduced basis using Gram-Schmidt orthogonalization vectors $b_i^*$ and size-reduction parameter $\delta \in (1/2, 1)$.
* **Console Inputs:** Dimension $d$, input basis matrix vectors, reduction parameter $\delta$ (default $0.75$).
* **Console Outputs:** Reduced basis matrix, original vs reduced basis determinant comparison, orthogonality defect metric.
* **Corner Case Resilience:** Detects linearly dependent input vectors and zero vectors, raising clean linear independence exception alerts before matrix operations.
</details>

<details>
<summary><b>2. Coppersmith's Method via LLL Modular Root Finder</b></summary>

<br>

* **Mathematical Overview:** Finds small integer roots $x_0$ of monic polynomial $f(x) \pmod N$ where $|x_0| < N^{1/d}$. Construct Howgrave-Graham lattice polynomials and applies LLL to find short vectors corresponding to equations over $\mathbb{Z}$.
* **Console Inputs:** Monic polynomial coefficients, composite modulus $N$, degree $d$, upper root bound $X$.
* **Console Outputs:** Small integer root $x_0$ satisfying $f(x_0) \equiv 0 \pmod N$.
* **Corner Case Resilience:** Validates bound parameters against theoretical Coppersmith thresholds ($X < N^{1/d - \epsilon}$); rejects non-monic or trivial polynomials.
</details>

<details>
<summary><b>3. Schönhage–Strassen Asymptotic FFT Multiplication Matrix</b></summary>

<br>

* **Mathematical Overview:** Performs arbitrary-precision large integer multiplication using Fast Fourier Transforms (FFT) over complex roots of unity or Fermat rings $\mathbb{Z}/(2^{2^k}+1)\mathbb{Z}$. Transforms linear convolutions into point-wise multiplication vectors in $\mathcal{O}(N \log N \log \log N)$.
* **Console Inputs:** Large integer $A$, large integer $B$.
* **Console Outputs:** Exact product $C = A \cdot B$, bit length execution logs, precision deviation checks.
* **Corner Case Resilience:** Evaluates sign bits separately, handles zero products immediately, and falls back to Karatsuba or naive arithmetic for sub-threshold bit lengths.
</details>

---

### 📂 Cyclic Groups & Congruence Solvers

<details>
<summary><b>1. Schoof's Point-Counting Algorithm for Elliptic Curves</b></summary>

<br>

* **Mathematical Overview:** Determines the cardinality of the group of rational points on elliptic curves $E(\mathbb{F}_p)$ over finite fields. Computes $t \pmod \ell$ (trace of Frobenius) for small primes $\ell$ using division polynomials $\psi_\ell$, combining results via the Chinese Remainder Theorem (CRT).
* **Console Inputs:** Field prime $p$ ($p > 3$), curve coefficients $a, b \in \mathbb{F}_p$.
* **Console Outputs:** Total point count $\#E(\mathbb{F}_p) = p + 1 - t$, trace of Frobenius $t$.
* **Corner Case Resilience:** Checks non-singularity condition $\Delta = -16(4a^3 + 27b^2) \not\equiv 0 \pmod p$ before initializing division polynomials.
</details>

<details>
<summary><b>2. Berlekamp–Massey LFSR Linear Complexity Synthesis</b></summary>

<br>

* **Mathematical Overview:** Computes the minimal polynomial $C(x)$ and linear complexity $L$ of a given binary sequence $s$, yielding the shortest Linear Feedback Shift Register (LFSR) capable of generating $s$.
* **Console Inputs:** Binary stream vector $(s_0, s_1, \dots, s_{N-1})$.
* **Console Outputs:** Minimal polynomial coefficients $C(x)$, linear complexity $L$, discrepancy evaluation traces.
* **Corner Case Resilience:** Supports arbitrary sequence lengths, correctly processing all-zero sequences ($L=0$) and alternating bit patterns without index out-of-bound errors.
</details>

<details>
<summary><b>3. Pohlig-Hellman Smooth Cyclic Group Logarithm Solver</b></summary>

<br>

* **Mathematical Overview:** Solves the Discrete Logarithm Problem (DLP) $g^x \equiv h \pmod p$ when the order of the group $|G| = p - 1$ is smooth (factors into small primes). Computes sub-logs modulo prime powers $q_i^{e_i}$ using Baby-Step Giant-Step and reconstructs $x \pmod{|G|}$ using CRT.
* **Console Inputs:** Generator $g$, target element $h$, modulus prime $p$.
* **Console Outputs:** Exponent $x$, prime factorization of order $p-1$, sub-congruence solution matrix.
* **Corner Case Resilience:** Verifies $g$ is a valid primitive root/generator, checking that $h$ lies within the generated cyclic subgroup before starting decomposition.
</details>

<details>
<summary><b>4. Shanks' Tonelli-Shanks Modular Square Root Solver</b></summary>

<br>

* **Mathematical Overview:** Solves quadratic congruences $r^2 \equiv a \pmod p$ for odd primes $p$. Expresses $p - 1 = Q \cdot 2^s$ with $Q$ odd, finds a quadratic non-residue $z$, and updates powers iteratively until $r^2 a^{-1} \equiv 1 \pmod p$.
* **Console Inputs:** Integer $a$, prime modulus $p$.
* **Console Outputs:** Quadratic roots $r$ and $p - r$ satisfying $r^2 \equiv a \pmod p$.
* **Corner Case Resilience:** Computes Legendre symbol $\left(\frac{a}{p}\right)$ during pre-flight; halts cleanly if $a$ is a quadratic non-residue ($\left(\frac{a}{p}\right) = -1$).
</details>

---

### 📂 Advanced Graph Theory & Network Optimization

<details>
<summary><b>1. Hopcroft-Karp Bipartite Matching Optimizer</b></summary>

<br>

* **Mathematical Overview:** Finds maximum cardinality matchings in bipartite graphs $G = (L \cup R, E)$. Uses Breadth-First Search (BFS) to build layered graphs of shortest augmenting paths, followed by Depth-First Search (DFS) to extract maximal sets of vertex-disjoint augmenting paths in $\mathcal{O}(E \sqrt{V})$.
* **Console Inputs:** Left set vertices $L$, right set vertices $R$, edge array list.
* **Console Outputs:** Maximum matching size, matched pair array, vertex cover equivalence matrix.
* **Corner Case Resilience:** Validates strict bipartite input structure; safely returns empty matching for disconnected or edge-less graph inputs.
</details>

<details>
<summary><b>2. Tarjan's Linear-Time Strongly Connected Components Matrix</b></summary>

<br>

* **Mathematical Overview:** Identifies all Strongly Connected Components (SCCs) in a directed graph using a single DFS traversal. Tracks node discovery indices and lowest reachable link values (`lowlink`) via an explicit execution stack.
* **Console Inputs:** Directed graph adjacency list or node-edge tuple set.
* **Console Outputs:** Partitioned array of strongly connected components, condensation graph topology.
* **Corner Case Resilience:** Seamlessly processes self-loops, disconnected components, parallel edges, and acyclic DAG configurations.
</details>

---

## 🚀 Installation & Operational Workflow

### Prerequisites
* **Python 3.10+** (Vanilla standard library; zero third-party dependencies required).

### Execution Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/rayaantasnim/Arithmatic-Complex-Mathematical-Python.git
   cd Arithmatic-Complex-Mathematical-Python
   ```

2. **Run Pre-Flight Self-Test:**
   Verify shield safeguards and mathematical integrity across engines:
   ```bash
   python -m unittest discover tests
   ```

3. **Launch an Algorithm Engine:**
   Run any engine interactively via the CLI:
   ```bash
   # Launch Brent's Pollard Rho Engine
   Pollard's Rho with Brent's Optimization.py

   # Launch LLL Lattice Reduction Engine
   LLL Lattice Basis Reduction.py

   # Launch Pohlig-Hellman Discrete Log Solver
   Pohlig-Hellman Algorithm.py
   ```

---

<p align="center">
  Authorized by Rayaan Tasnim<br>
  Powered by Olympiad Edge<br>
  &copy; All rights reserved
</p>
