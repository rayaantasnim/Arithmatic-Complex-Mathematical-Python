# Author: Rayaan Tasnim, prodigious teen programmer

import sys
import time

# Dynamically safeguard against recursion depth overflow in deep linear chains
sys.setrecursionlimit(200005)

class TarjanSCCEngine:
    """
    High-Performance Tarjan's Strongly Connected Components (SCC) Algorithm.
    Achieves theoretical linear time complexity of O(V + E) using a single DFS pass.
    """
    def __init__(self, adj, nodes):
        self.adj = adj
        self.nodes = list(nodes)
        self.discovery_index = {}
        self.low_link = {}
        self.on_stack = set()
        self.stack = []
        self.sccs = []
        self.time_counter = 0

    def _dfs(self, u):
        # Initialize discovery index and low-link value
        self.discovery_index[u] = self.time_counter
        self.low_link[u] = self.time_counter
        self.time_counter += 1
        
        self.stack.append(u)
        self.on_stack.add(u)

        # Explore neighbors
        for v in self.adj.get(u, []):
            if v not in self.discovery_index:
                # Successor v has not been visited; recurse on it
                self._dfs(v)
                self.low_link[u] = min(self.low_link[u], self.low_link[v])
            elif v in self.on_stack:
                # Successor v is in stack and hence in the current SCC
                self.low_link[u] = min(self.low_link[u], self.discovery_index[v])

        # If u is the root of the SCC, pop the stack and generate the component
        if self.low_link[u] == self.discovery_index[u]:
            current_scc = []
            while True:
                v = self.stack.pop()
                self.on_stack.remove(v)
                current_scc.append(v)
                if v == u:
                    break
            self.sccs.append(current_scc)

    def compute_sccs(self):
        for node in self.nodes:
            if node not in self.discovery_index:
                self._dfs(node)
        return self.sccs


def validate_graph_structure(nodes, adj):
    """
    System Safeguards & Structure Validation Layer.
    Interceptors for empty nodes, invalid identifiers, and configuration errors.
    """
    node_set = set(nodes)

    if not node_set:
        raise ValueError("Graph configuration error: Node set cannot be empty.")

    # Trivial Graph Traps check
    total_edges = sum(len(neighbors) for neighbors in adj.values())
    if total_edges == 0:
        return True # Trivial graph detected (0 edges)

    # Validate edge endpoints reference valid nodes
    for u, neighbors in adj.items():
        if u not in node_set:
            raise ValueError(f"Network error: Node '{u}' in adjacency list is missing from the global node set.")
        for v in neighbors:
            if v not in node_set:
                raise ValueError(f"Network error: Target neighbor '{v}' of node '{u}' is missing from the global node set.")

    return False


def run_custom_graph_cli():
    print("\n--- DIRECTED GRAPH SCC PARTITION ENGINE ---")
    print("Format nodes and directed edges. Example nodes: A, B, C or 1, 2, 3")
    
    try:
        nodes_input = input("Enter all graph nodes (comma-separated): ").strip()
        if not nodes_input:
            raise ValueError("Node set cannot be empty.")
        nodes = [x.strip() for x in nodes_input.split(',')]

        print("\nEnter adjacency list for each node (e.g., node: v1, v2, v3).")
        print("Type 'done' when finished entering directed edges.")
        
        adj = {node: [] for node in nodes}
        while True:
            line = input("Directed Edge mapping (u: v1,v2 or 'done'): ").strip()
            if line.lower() == 'done' or not line:
                break
            if ':' not in line:
                print("Invalid format. Use format 'u: v1, v2'. Try again.")
                continue
            parts = line.split(':', 1)
            u_node = parts[0].strip()
            if u_node not in adj:
                print(f"Warning: Node '{u_node}' is not in the node set. Ignoring entry.")
                continue
            v_nodes = [v.strip() for v in parts[1].split(',') if v.strip()]
            adj[u_node] = v_nodes

        # Invoke Structure Safeguards
        is_trivial = validate_graph_structure(nodes, adj)
        
        if is_trivial:
            print("\n[Notice] Trivial graph detected (0 edges). Each node is its own isolated SCC.")
            sccs = [[n] for n in nodes]
        else:
            engine = TarjanSCCEngine(adj, nodes)
            start_time = time.perf_counter()
            sccs = engine.compute_sccs()
            elapsed = (time.perf_counter() - start_time) * 1000
            print(f"\n[SUCCESS] Tarjan SCC Matrix Computed in {elapsed:.4f} ms.")

        print(f"-> Total Strongly Connected Components Found: {len(sccs)}")
        for idx, scc in enumerate(sccs, 1):
            print(f"   Component {idx}: {scc}")

    except Exception as e:
        print(f"\n[ERROR INTERCEPTED] Topology processing halted safely: {e}")


def run_topology_simulation():
    print("\n--- AUTOMATED COMPLEX CYCLIC NETWORK SIMULATION ---")
    print("Constructing a 20-node benchmark network with interwoven cycles and structural dead-ends...")

    # Define 20 nodes (0 to 19) structured into multiple cyclic clusters and terminal dead-ends
    nodes = [str(i) for i in range(20)]
    adj = {str(i): [] for i in range(20)}

    # Cluster 1: Cycle 0 -> 1 -> 2 -> 0, with exit to 3
    adj['0'] = ['1']
    adj['1'] = ['2']
    adj['2'] = ['0', '3']

    # Cluster 2: Cycle 3 -> 4 -> 5 -> 3, with bridge to Cluster 3
    adj['3'] = ['4']
    adj['4'] = ['5']
    adj['5'] = ['3', '6']

    # Cluster 3: Simple cycle 6 -> 7 -> 6, and linear sink 7 -> 8 -> 9 (dead-end)
    adj['6'] = ['7']
    adj['7'] = ['6', '8']
    adj['8'] = ['9']
    adj['9'] = []

    # Cluster 4: Self-loop and independent cycle 10 <-> 11, routing to 12
    adj['10'] = ['11', '10'] # self-loop + cycle
    adj['11'] = ['10', '12']
    adj['12'] = ['13']
    adj['13'] = ['14']
    adj['14'] = ['12'] # Cycle 12 -> 13 -> 14 -> 12

    # Cluster 5: Interwoven complex 15, 16, 17, 18, 19
    adj['15'] = ['16']
    adj['16'] = ['17']
    adj['17'] = ['15', '18']
    adj['18'] = ['19']
    adj['19'] = ['15'] # Forms a massive loop across 15-19

    print("-> Network Topology Constructed: 20 Nodes with Multiple Interwoven Cyclic Superstructures.")
    print("-> Executing Tarjan O(V + E) Discovery Engine...")

    start_time = time.perf_counter()
    engine = TarjanSCCEngine(adj, nodes)
    sccs = engine.compute_sccs()
    elapsed = (time.perf_counter() - start_time) * 1000

    print(f"\n[TOPOLOGY SIMULATION RESULTS]")
    print(f"-> Computation Latency: {elapsed:.4f} ms")
    print(f"-> Total Strongly Connected Components: {len(sccs)}")
    
    for idx, scc in enumerate(sccs, 1):
        component_type = "Cyclic / Multi-node SCC" if len(scc) > 1 else "Acyclic / Isolated Node"
        print(f"   [SCC #{idx}] Type: {component_type} | Nodes: {scc}")

    print("\n-> Network Data Stream Routing Analysis:")
    print("   The DAG condensation of these components maps downstream flow from terminal sinks to root clusters.")


def main_cli_loop():
    print("=======================================================")
    print("      TARJAN'S STRONGLY CONNECTED COMPONENTS ENGINE    ")
    print("      Combinatorial Graph Topology & Matrix Suite      ")
    print("=======================================================")

    while True:
        print("\n--- TOPOLOGY ENGINE TERMINAL MENU ---")
        print("1. Partition a directed graph into Strongly Connected Components (SCC Matrix)")
        print("2. Run topology simulation on a dense cyclic network mapping dependencies")
        print("3. Exit Topology Engine")
        
        try:
            choice = input("Select operation [1-3]: ").strip()
            if choice == '1':
                run_custom_graph_cli()
            elif choice == '2':
                run_topology_simulation()
            elif choice == '3':
                print("\nExiting Topology Engine. Goodbye, Engineer.")
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
