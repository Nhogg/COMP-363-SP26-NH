# Provided codebase
def sssp(s, G):
    n: int = len(G)  # Shortcut to size of graph
    no_edge = G[0][0]  # Shortcut to absence of edge
    oo = float("inf")  # Shortcut to infinity
    d: list = [oo for _ in range(n)]  # Assume looooong distances
    d[s] = 0  # Source distance to itself
    bag = [s]  # Start from source
    while len(bag) > 0:  # While bag not empty
        u = bag.pop()  # Take a vertex out of bag
        for v in range(n):  # Find u's neighbors
            if G[u][v] != no_edge:  # There is an edge (u,v)
                if d[v] > d[u] + G[u][v]:  # Is edge (u,v) tense?
                    d[v] = d[u] + G[u][v]  # Relax the edge
                    bag.append(v)  # Explore v next
    return d  # Shortest path distances


graph = [
    # 0   1   2   3   4   5   6   7
    [0, 5, 1, 5, 10, 0, 0, 0],  # 0
    [0, 0, 12, 5, 6, 0, 0, 0],  # 1
    [0, 0, 0, 1, 0, 0, 5, 0],  # 2
    [0, 0, 0, 0, 0, 1, 5, 0],  # 3
    [0, 0, 0, 6, 0, 5, 0, 5],  # 4
    [0, 0, 0, 0, 0, 0, 1, 5],  # 5
    [0, 0, 0, 0, 0, 0, 0, 1],  # 6
    [0, 0, 0, 0, 0, 0, 0, 0],  # 7
]


def reconstruct(d: list[int], s: int, graph: list[list[int]]) -> list[int]:
    """
    Reconstruct the path from source to destination.

    Args:
        d (list[int]): A list of shortest path distances from source s to every other
                       vertex (output from SSSP)
        s (int): The index of the source vertex.
        graph (list[list[int]]): The adjacency matrix of the graph where graph[u][v]
                                 is the weight of the edge u -> v.

    Returns:
        list[int]: A list p where p[u] is the predecessor of u in the shortest path.
                   Returns None for the source vertex or unreachable vertices.
    """
    n = len(graph)
    # Initialize p with None for all vertices
    p = [None] * n

    # Iterate through every possible parent (u)
    for u in range(n):
        # Iterate through every possible child (v)
        for v in range(n):
            weight = graph[u][v]

            # Check two things:
            # 1. An edge actually exists (weight != 0)
            # 2. The mathematical condition: d[v] == d[u] + weight
            # We also verify d[u] isn't infinity to avoid false positives with Unreachable nodes
            if weight != 0 and d[v] == d[u] + weight and d[u] != float('inf'):
                p[v] = u

    return p


def report_sssp(p: list[int], d: list[int], graph: list[list[int]]) -> None:
    """
    Prints the shortest path from the source to every vertex in the graph.

    Args:
        p (list[int]): The list of predecessors (output from reconstruct).
        d (list[int]): The list of shortest distances (output from SSSP).
        graph (list[list[int]]): The adjacency matrix of the graph.

    Returns:
        None: This function prints the paths directly to stdout.
    """
    n = len(graph)

    for target in range(n):
        # Handle unreachable vertices first
        if d[target] == float('inf'):
            print(f"Vertex {target}: Unreachable")
            continue

        # Reconstruct path by backtracking
        path = []
        curr = target

        # Traverse up the predecessor tree until we hit the source (None)
        while curr is not None:
            path.append(str(curr))
            curr = p[curr]

        # Reverse the path to get Source -> Target order
        path.reverse()

        path_str = " -> ".join(path)
        print(f"Vertex {target}: {path_str} (Distance: {d[target]})")


def main():
    """ testing SSSP and Reconstruct """

    print("Running SSSP on Source Node 0...")
    source = 0
    d = sssp(source, graph)

    print(f"Distances: {d}")
    print("\nTesting Reconstruct")
    p = reconstruct(d, source, graph)
    print(f"Predecessors List: {p}")
    expected_p = [None, 0, 0, 2, 0, 3, 5, 6]

    if p == expected_p:
        print(" Reconstruct list matches example.")
    else:
        print(f"Expected {expected_p}")

    print("\n---  Report SSSP ---")
    report_sssp(p, d, graph)


if __name__ == "__main__":
    main()
