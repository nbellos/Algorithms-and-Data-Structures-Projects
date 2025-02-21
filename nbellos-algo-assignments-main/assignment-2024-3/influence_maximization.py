import sys
import argparse
import random
from collections import deque, defaultdict

def maxepirroi(G, p, k, mc):
    """ Implements greedy selection for influence maximization """
    if not G:
        print("Error: The graph is empty or not loaded properly.")
        sys.exit(1)

    S = set()
    e = []
    nodes = list(G.keys())  # Convert to list to avoid dictionary modification issue

    for _ in range(k):
        max_influence = float('-inf')
        best_node = None

        for node in nodes:  
            if node not in S:
                candidate_set = S | {node}
                influence = ektimhsh(G, candidate_set, p, mc)
                if influence > max_influence:
                    max_influence = influence
                    best_node = node

        if best_node is None:
            break

        S.add(best_node)
        e.append(max_influence)

    return list(S), e


def ektimhsh(G, sporoi, p, mc):
    """ Estimates influence spread using Monte Carlo simulation """
    total_influence = 0

    for _ in range(mc):
        active_nodes = set(sporoi)
        queue = deque(sporoi)
        processed_edges = set()

        while queue:
            u = queue.popleft()
            for v in G[u]:
                if (u, v) not in processed_edges and v not in active_nodes:
                    processed_edges.add((u, v))
                    if random.random() < p:
                        active_nodes.add(v)
                        queue.append(v)

        total_influence += len(active_nodes)

    return total_influence / mc

def build_graph(filename):
    """ Constructs graph from edge list file """
    graph = defaultdict(set)  
    try:
        with open(filename, 'r') as file:
            for line in file:
                if line.strip():
                    nodes = line.split()
                    if len(nodes) != 2:
                        print(f"Warning: Skipping malformed line -> {line.strip()}")
                        continue
                    u, v = map(int, nodes)
                    graph[u].add(v)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        sys.exit(1)
    
    if not graph:
        print(f"Error: Graph file '{filename}' is empty or improperly formatted.")
        sys.exit(1)

    return graph


def maxsporoi(G, k):
    """ Selects k nodes with the highest out-degree """
    return sorted(G, key=lambda node: len(G[node]), reverse=True)[:k]

def evaluate_influence(G, sporoi, p, mc):
    """ Computes influence spread for selected seed nodes """
    influences = []
    for i in range(len(sporoi)):
        influence = ektimhsh(G, set(sporoi[:i+1]), p, mc)
        influences.append(influence)
    return influences

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Influence Maximization in Social Networks")
    parser.add_argument("graph", type=str, help="Graph file with edges.")
    parser.add_argument("k", type=int, help="Number of seed nodes to select.")
    parser.add_argument("strategy", type=str, choices=["greedy", "max_degree"], help="Seed selection method.")
    parser.add_argument("probability", type=float, help="Probability of influence spread.")
    parser.add_argument("mc", type=int, help="Number of Monte Carlo simulations.")
    parser.add_argument("-r", "--random_seed", type=int, help="Random seed for reproducibility.", default=None)
    args = parser.parse_args()

    # Set random seed for reproducibility
    if args.random_seed is not None:
        random.seed(args.random_seed)

    G = build_graph(args.graph)
    k = args.k
    p = args.probability
    mc = args.mc

    if args.strategy == "greedy":
        sporoi, influences = maxepirroi(G, p, k, mc)
    else:  # max_degree strategy
        sporoi = maxsporoi(G, k)
        influences = evaluate_influence(G, sporoi, p, mc)

    print("Seeds:", sporoi)
    print("Influences:", influences)
