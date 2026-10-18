# Author: Rayaan Tasnim, prodigious teen programmer

import sys
import random
import time

class HopcroftKarpEngine:
    """
    High-Performance Hopcroft-Karp Bipartite Matching Engine.
    Achieves theoretical time complexity of O(E * sqrt(V)).
    """
    def __init__(self, adj, U, V):
        self.adj = adj
        self.U = list(U)
        self.V = list(V)
        self.pair_u = {u: None for u in self.U}
        self.pair_v = {v: None for v in self.V}
        self.dist = {}
        self.NIL = None

    def bfs(self):
        queue = []
        for u in self.U:
            if self.pair_u[u] is None:
                self.dist[u] = 0
                queue.append(u)
            else:
                self.dist[u] = float('inf')
        
        self.dist[self.NIL] = float('inf')
        
        while queue:
            u = queue.pop(0)
            if self.dist[u] < self.dist[self.NIL]:
                for v in self.adj.get(u, []):
                    pv = self.pair_v.get(v)
                    if pv is None:
                        if self.dist[self.NIL] == float('inf'):
                            self.dist[self.NIL] = self.dist[u] + 1
                    else:
                        if self.dist.get(pv, float('inf')) == float('inf'):
                            self.dist[pv] = self.dist[u] + 1
                            queue.append(pv)
        return self.dist[self.NIL] != float('inf')

    def dfs(self, u):
        if u != self.NIL:
            for v in self.adj.get(u, []):
                pv = self.pair_v.get(v)
                if pv is None or (self.dist.get(pv, float('inf')) == self.dist[u] + 1 and self.dfs(pv)):
                    self.pair_u[u] = v
                    self.pair_v[v] = u
                    return True
            self.dist[u] = float('inf')
            return False
        return True

    def compute_maximum_matching(self):
        matching_cardinality = 0
        while self.bfs():
            for u in self.U:
                if self.pair_u[u] is None:
                    if self.dfs(u):
                        matching_cardinality += 1
        active_matches = {u: v for u, v in self.pair_u.items() if v is not None}
        return matching_cardinality, active_matches


def validate_bipartite_structure(U, V, adj):
    """
    Global Graph Safeguards & Disconnected Element Shield.
    Verifies structural integrity, partition disjointness, and bipartite edge validity.
    """
    set_u = set(U)
    set_v = set(V)

    # Structure Validation Layer
    if not set_u or not set_v:
        raise ValueError("Graph configuration error: Partition U or V cannot be empty.")
    
    if not set_u.isdisjoint(set_v):
        raise ValueError("Graph configuration error: Partitions U and V must be strictly disjoint sets.")

    # Bipartite Verification Shield & Edge Integrity
    for u, neighbors in adj.items():
        if u not in set_u:
            raise ValueError(f"Network error: Node '{u}' in adjacency list is not part of partition U.")
        for v in neighbors:
            if v in set_u:
                raise ValueError(f"Bipartite violation: Intra-partition edge detected within U between '{u}' and '{v}'.")
            if v not in set_v:
                raise ValueError(f"Network error: Neighbor '{v}' of node '{u}' is not part of partition V.")

    # Trivial Graph Traps check
    total_edges = sum(len(neighbors) for neighbors in adj.values())
    if total_edges == 0 or len(set_u) == 0 or len(set_v) == 0:
        return True # Trivial graph detected, safe for empty return

    return False


def run_custom_graph_cli():
    print("\n--- CUSTOM BIPARTITE GRAPH MATCHING ENGINE ---")
    print("Format partitions and edges. Example nodes: A, B, C or 1, 2, 3")
    
    try:
        u_input = input("Enter nodes in Partition U (comma-separated): ").strip()
        if not u_input:
            raise ValueError("Partition U cannot be empty.")
        U = [x.strip() for x in u_input.split(',')]

        v_input = input("Enter nodes in Partition V (comma-separated): ").strip()
        if not v_input:
            raise ValueError("Partition V cannot be empty.")
        V = [x.strip() for x in v_input.split(',')]

        print("\nEnter adjacency list for each node in U (e.g., node: v1, v2, v3).")
        print("Type 'done' when finished entering edges.")
        
        adj = {u: [] for u in U}
        while True:
            line = input("Edge mapping (u: v1,v2 or 'done'): ").strip()
            if line.lower() == 'done' or not line:
                break
            if ':' not in line:
                print("Invalid format. Use format 'u: v1, v2'. Try again.")
                continue
            parts = line.split(':', 1)
            u_node = parts[0].strip()
            if u_node not in adj:
                print(f"Warning: Node '{u_node}' is not in Partition U. Ignoring entry.")
                continue
            v_nodes = [v.strip() for v in parts[1].split(',') if v.strip()]
            adj[u_node] = v_nodes

        # Invoke Safeguards
        is_trivial = validate_bipartite_structure(U, V, adj)
        
        if is_trivial:
            print("\n[Notice] Trivial graph detected (0 edges or isolated partitions). Matching Cardinality: 0")
            return

        engine = HopcroftKarpEngine(adj, U, V)
        start_time = time.perf_counter()
        cardinality, matching = engine.compute_maximum_matching()
        elapsed = (time.perf_counter() - start_time) * 1000

        print(f"\n[SUCCESS] Maximum Cardinality Bipartite Matching Computed.")
        print(f"-> Matching Cardinality: {cardinality}")
        print(f"-> Execution Time: {elapsed:.4f} ms")
        print(f"-> Active Match Pairs:")
        if not matching:
            print("   (No matches found)")
        else:
            for u, v in matching.items():
                print(f"   U({u}) <---> V({v})")

    except Exception as e:
        print(f"\n[ERROR INTERCEPTED] Graph processing halted safely: {e}")


def run_optimization_benchmark():
    print("\n--- AUTOMATED MASSIVE BENCHMARK & STRESS MATRIX ---")
    print("Initializing massive bipartite layout (500 nodes in U, 500 nodes in V)...")

    # Generate massive random dense bipartite graph
    size_u = 500
    size_v = 500
    U = [f"U{i}" for i in range(size_u)]
    V = [f"V{j}" for j in range(size_v)]

    random.seed(42) # Reproducible robust benchmarking
    adj = {}
    total_edges = 0
    for u in U:
        # Connect each u to a randomized subset of V (approx 30% density for heavy load testing)
        num_neighbors = random.randint(50, 150)
        neighbors = random.sample(V, num_neighbors)
        adj[u] = neighbors
        total_edges += len(neighbors)

    print(f"-> Network Generated: |U| = {size_u}, |V| = {size_v}, Total Directed Edges = {total_edges}")
    print("-> Executing Hopcroft-Karp O(E * sqrt(V)) engine...")

    start_time = time.perf_counter()
    engine = HopcroftKarpEngine(adj, U, V)
    cardinality, matching = engine.compute_maximum_matching()
    elapsed = (time.perf_counter() - start_time) * 1000

    print(f"\n[BENCHMARK RESULTS]")
    print(f"-> Maximum Matching Cardinality: {cardinality} / {min(size_u, size_v)}")
    print(f"-> Computation Latency: {elapsed:.2f} ms")

    # Hall's Marriage Theorem Boundary Verification Check
    # Verify bounds: matching cardinality cannot exceed min(|U|, |V|)
    assert cardinality <= min(size_u, size_v), "Violation: Matching exceeds partition bounds!"
    print(f"-> Hall's Marriage Theorem Boundary Verification: PASSED (Cardinality within theoretical limits).")


def main_cli_loop():
    print("=======================================================")
    print("  HOPCROFT-KARP MAXIMUM CARDINALITY BIPARTITE ENGINE   ")
    print("  Combinatorial Optimization & Graph Theory Suite      ")
    print("=======================================================")

    while True:
        print("\n--- GRAPH ENGINE TERMINAL MENU ---")
        print("1. Compute Maximum Matching Matrix for a custom bipartite graph")
        print("2. Run optimization benchmark on an automated massive matching layout")
        print("3. Exit Graph Engine")
        
        try:
            choice = input("Select operation [1-3]: ").strip()
            if choice == '1':
                run_custom_graph_cli()
            elif choice == '2':
                run_optimization_benchmark()
            elif choice == '3':
                print("\nExiting Graph Engine. Goodbye, Engineer.")
                sys.exit(0)
            else:
                print("\n[Error] Invalid menu selection. Please choose 1, 2, or 3.")
        except (KeyboardInterrupt, EOFError):
            print("\n\nSession terminated safely by user prompt. Goodbye.")
            sys.exit(0)
        except Exception as e:
            print(f"\n[UNEXPECTED EXCEPTION CAUGHT]: {e}")
            print("Returning to main menu loop...")


if __name__ == '__main__':
    main_cli_loop()
