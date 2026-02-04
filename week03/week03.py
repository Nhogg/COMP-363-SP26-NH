
def reachability(s: int, G: list[list[int]]) -> list:
    """
    Finds all vertices reachable from a start note in a graph.

    Args:
        s (int): The index of the starting vertex.
        G (list[list[int]]): An adjacency matrix representing the graph,
                             where G[u][v] == 1 indicates an edge exists
                             from u to v.

    Returns:
        list: A list of integers representing the indices of all reachable
              vertices.

    """"
    reachable_vertices = set()
    visit_next = [s]

    while len(visit_next) > 0:
        current = visit_next.pop()

        reachable_vertices.add(current)

        for idx, is_connected in enumerate(G[current]):
            if is_connected == 1 and idx not in reachable_vertices:
                visit_next.append(idx)

    return list(reachable_vertices)


def main():
    graph = [
    # 0  1  2  3  4  5  6  7
    [ 0, 0, 0, 1, 0, 0, 1, 0],  # vertex 0
    [ 0, 0, 0, 0, 0, 1, 0, 0],  # vertex 1
    [ 0, 0, 0, 0, 1, 0, 0, 0],  # vertex 2
    [ 1, 0, 0, 0, 0, 1, 0, 0],  # vertex 3
    [ 0, 0, 1, 0, 0, 0, 0, 0],  # vertex 4
    [ 0, 1, 0, 1, 0, 0, 0, 0],  # vertex 5
    [ 1, 0, 0, 0, 0, 0, 0, 0],  # vertex 6
    [ 0, 0, 0, 0, 0, 0, 0, 0]   # vertex 7
]

    print(reachability(3, graph))

main()
