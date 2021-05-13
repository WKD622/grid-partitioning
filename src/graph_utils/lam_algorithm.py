import random

from src.utils import print_infos


def is_free(M, v):
    """
    Returns true if vertex hasn't been matched, false otherwise.
    """
    return v not in M


def is_matched(M, v):
    """
    Returns true if vertex has been matched, false otherwise.
    """
    return v in M


def get_unchecked_edges(G, U, v):
    """
    1) Gets all adjacent vertices to vertex v
    2) Creates all adjacent edges to vertex v based on those adjacent vertices
    3) Does intersection with all unmatched edges (U)
    """
    adj_vertices = set(G.adj[v])
    adj_edges = set()
    for x in adj_vertices:
        adj_edges.add((x, v))
        adj_edges.add((v, x))
    return U.intersection(adj_edges)


def get_adj_unchecked_vertex(G, U, v):
    """
    Returns one, random, unchecked, adjacent vertex to vertex v.
    """
    unchecked_edges = get_unchecked_edges(G, U, v)
    (k, l) = list(unchecked_edges)[random.randint(0, len(unchecked_edges) - 1)]
    if k == v:
        return l
    return k


def there_are_unchecked_edges(G, U, v):
    """
    Returns true if there are unchecked edges starting from vertex v, false otherwise.
    """
    return bool(get_unchecked_edges(G, U, v))


def match(M, a, b):
    """
    Matches edge (a, b).
    """
    M[a] = b
    M[b] = a


def edge_ab_in_set(S, a, b):
    return (a, b) in S or (b, a) in S


def get_edge_weight(G, a, b):
    """
    Returns weight of an edge (a, b).
    """
    return G[a][b]['w']


def remove_edge_from_set(S, a, b):
    if (a, b) in S:
        S.remove((a, b))
    if (b, a) in S:
        S.remove((b, a))


def move_edge(from_, to_, a, b):
    """
    Moves edge (a, b) or (b, a) (checks both options) from set 'from_' to set 'to_'
    """
    if edge_ab_in_set(from_, a, b):
        remove_edge_from_set(from_, a, b)
        to_.add((a, b))
    else:
        raise Exception("No edge: (" + a + ", " + b + ") to move.")


def restore_all_free_edges(U, M, C, v):
    """
    (Vertex v is not matched)
    Moves all edges which include vertex 'v' and have the other vertex also not matched back to U set,
    so that they can be matched in further process of the algorithm execution.
    """
    edges_to_be_moved = []
    for k, l in C:
        if (is_free(M, k) and l == v) or (is_free(M, l) and k == v):
            edges_to_be_moved.append((k, l))

    for k, l in edges_to_be_moved:
        move_edge(from_=C, to_=U, a=k, b=l)


def get_smallest_and_highest_weights(G):
    weights = sorted(G.nodes.data(), key=lambda k: k[1]['data']['weight'])
    highest_weight = weights[-1][1]['data']['weight']
    smallest_weight = weights[0][1]['data']['weight']
    return highest_weight, smallest_weight


def remove_adj_edges(G, U, v):
    for x in get_unchecked_edges(G, U, v):
        k, l = x
        remove_edge_from_set(U, k, l)


def draw_an_edge(edges):
    """
    Draws random edge from given set of edges. It is extremely inefficient.
    """
    return random.choice(tuple(edges))


def convert_matched_for_return(M):
    """
    Creates output format which is in more suitable form to do reductions in graph.
    """
    M_out = []
    for key, value in M.items():
        if {key, value} not in M_out and {value, key} not in M_out:
            M_out.append({key, value})
    return M_out


def print_progress(U, G):
    if len(U) % 1000 == 0:
        print("lam progress: " + str(round((1 - len(U) / int(G.number_of_edges())) * 100)) + "%")


def finish(M, G, number_of_partitions):
    """
    The condition to check whether lam_algorithm can be finished - because we have enough matchings to reduce our graph
    to expected size.
    """
    return (G.number_of_nodes() - len(M) / 2) == number_of_partitions


def can_be_matched(G, a, b, weights):
    """
    Here the condition is checked whether vertex 'a' can be matched with vertex 'b' based on their weights.
    """
    h_weight = weights['h_weight']
    s_weight = weights['s_weight']
    sum_weight_of_nodes = G.nodes[a]['data']['weight'] + G.nodes[b]['data']['weight']
    return sum_weight_of_nodes <= h_weight + (2 * s_weight)


def update_highest_weight(G, a, b, weights):
    """
    If combined weight of vertex 'a' and 'b' is bigger than highest, recorded weight - the highest, recorded
    weights is updated.
    """
    if G.nodes[a]['data']['weight'] + G.nodes[b]['data']['weight'] > weights['h_weight']:
        weights['h_weight'] = G.nodes[a]['data']['weight'] + G.nodes[b]['data']['weight']


def try_match(G, a, b, U, M, weights):
    C_a = set()
    C_b = set()

    while (is_free(M, a) and
           is_free(M, b) and
           (there_are_unchecked_edges(G, U, a) or there_are_unchecked_edges(G, U, b))):

        if is_free(M, a) and there_are_unchecked_edges(G, U, a):
            c = get_adj_unchecked_vertex(G, U, a)
            move_edge(from_=U, to_=C_a, a=a, b=c)
            if get_edge_weight(G, a, c) > get_edge_weight(G, a, b):
                try_match(G, a, c, U, M, weights)

        if is_free(M, b) and there_are_unchecked_edges(G, U, b):
            d = get_adj_unchecked_vertex(G, U, b)
            move_edge(from_=U, to_=C_b, a=b, b=d)
            if get_edge_weight(G, b, d) > get_edge_weight(G, a, b):
                try_match(G, b, d, U, M, weights)

    if is_free(M, a) and is_free(M, b) and can_be_matched(G, a, b, weights):
        match(M, a, b)
        update_highest_weight(G, a, b, weights)
    elif is_matched(M, a) and is_free(M, b):
        restore_all_free_edges(U, M, C_b, b)
    elif is_matched(M, b) and is_free(M, a):
        restore_all_free_edges(U, M, C_a, a)


@print_infos
def lam_algorithm(G, number_of_partitions):
    """
    Vertices in graph are represent by numbers.

    M - dictionary with matched vertices. If vertex 'a' is matched with vertex 'b' then it looks like this:
        M = {'a': 'b', 'b': 'a'}

    U - set with unmatched edges, at the beginning all edges from graph are here. Looks like this:
        U = {(a, b), (b, c), (f, a)} - edges are represented by tuples. Each element of a tuple represents vertex.

    h_weight, s_weight - highest and smallest weight of a vertex in a graph. Edges also have weights and they are used
    by this algorithm, in other places though.
    """
    M = {}
    U = set(G.edges)
    h_weight, s_weight = get_smallest_and_highest_weights(G)
    weights = {'h_weight': h_weight, 's_weight': s_weight}

    while len(U) != 0:
        print_progress(U, G)
        a, b = draw_an_edge(U)
        try_match(G, a, b, U, M, weights)
        if finish(M, G, number_of_partitions):
            break

    return convert_matched_for_return(M)
