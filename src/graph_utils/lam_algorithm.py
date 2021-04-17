import math
import random


def is_free(M, v):
    return v not in M


def is_matched(M, v):
    return v in M


def get_unchecked_edges(G, U, v):
    adj_vertices = set(G.adj[v])
    adj_edges = set()
    for x in adj_vertices:
        adj_edges.add((x, v))
        adj_edges.add((v, x))
    return U.intersection(adj_edges)


def get_adj_unchecked_vertex(G, U, v):
    (k, l) = get_unchecked_edges(G, U, v).pop()
    if k == v:
        return l
    return k


def there_are_unchecked_edges(G, U, v):
    return bool(get_unchecked_edges(G, U, v))


def can_be_matched(G, a, b, h_weight, s_weight, T, t, number_of_partitions):
    sum_weight_of_nodes = G.nodes[a]['data']['weight'] + G.nodes[b]['data']['weight']
    return (sum_weight_of_nodes <= (t / (T * (h_weight / (s_weight + 1)) * math.log(number_of_partitions))) *
            (h_weight + s_weight))


def match(M, a, b):
    M[a] = b
    M[b] = a


def edge_ab_in_set(S, a, b):
    return (a, b) in S or (b, a) in S


def get_weight(G, a, b):
    return G[a][b]['w']


def remove_edge_from_set(S, a, b):
    if (a, b) in S:
        S.remove((a, b))
    if (b, a) in S:
        S.remove((b, a))


def move_edge(from_, to_, a, b):
    if edge_ab_in_set(from_, a, b):
        remove_edge_from_set(from_, a, b)
        to_.add((a, b))
    else:
        raise Exception("No edge: (" + a + ", " + b + ") to move.")


def to_remove(R, C):
    for a, b in C:
        R.add((a, b))
    C.clear()


def remove_all_matched_edges(R, M, C, v):
    for k, l in C:
        if (is_matched(M, k) and l == v) or (is_matched(M, l) and k == v):
            move_edge(C, R, k, l)


def all_adj_matched(G, M, v):
    all_matched = True
    for w in set(G.adj[v].keys()):
        all_matched = all_matched and w in M
    return all_matched


def restore_all_free_edges(U, M, C, v):
    edges_to_be_moved = []
    for k, l in C:
        if (is_free(M, k) and l == v) or (is_free(M, l) and k == v):
            edges_to_be_moved.append((k, l))

    for k, l in edges_to_be_moved:
        move_edge(C, U, k, l)


def get_smallest_and_highest_degrees(G):
    degrees = sorted((d, n) for n, d in G.degree())
    highest_degree, _ = degrees[-1]
    smallest_degree, node_number = degrees[0]
    return highest_degree, smallest_degree, node_number


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
    index = random.randint(0, len(edges) - 1)
    return list(edges)[index]


def convert_matched_for_return(M):
    M_out = []
    for key, value in M.items():
        if {key, value} not in M_out and {value, key} not in M_out:
            M_out.append({key, value})
    return M_out


def print_progress(U, G):
    if len(U) % 1000 == 0:
        print("lam progress: " + str(round((1 - len(U) / int(G.number_of_edges())) * 100)) + "%")


def finish(M, G, number_of_partitions):
    return (G.number_of_nodes() - len(M) / 2) == number_of_partitions


def try_match(G, a, b, U, M, h_weight, s_weight, T, t, number_of_partitions):
    C_a = set()
    C_b = set()
    while is_free(M, a) and is_free(M, b) and (
            there_are_unchecked_edges(G, U, a) or there_are_unchecked_edges(G, U, b)):
        if is_free(M, a) and there_are_unchecked_edges(G, U, a):
            c = get_adj_unchecked_vertex(G, U, a)
            move_edge(U, C_a, a, c)
            if get_weight(G, a, c) > get_weight(G, a, b):
                try_match(G, a, c, U, M, h_weight, s_weight, T, t, number_of_partitions)
        if is_free(M, b) and there_are_unchecked_edges(G, U, b):
            d = get_adj_unchecked_vertex(G, U, b)
            move_edge(U, C_b, b, d)
            if get_weight(G, b, d) > get_weight(G, a, b):
                try_match(G, b, d, U, M, h_weight, s_weight, T, t, number_of_partitions)
    is_free_a = is_free(M, a)
    is_free_b = is_free(M, b)
    if is_free_a and is_free_b and can_be_matched(G, a, b, h_weight, s_weight, T, t, number_of_partitions):
        match(M, a, b)
    elif is_matched(M, a) and is_free_b:
        restore_all_free_edges(U, M, C_b, b)
    elif is_matched(M, b) and is_free_a:
        restore_all_free_edges(U, M, C_a, a)


def lam_algorithm(G, number_of_partitions, T, t):
    print("lam started...")
    M = {}
    U = set(G.edges)
    h_weight, s_weight = get_smallest_and_highest_weights(G)

    while len(U) != 0:
        print_progress(U, G)
        a, b = draw_an_edge(U)
        try_match(G, a, b, U, M, h_weight, s_weight, T, t, number_of_partitions)
        if finish(M, G, number_of_partitions):
            break

    print("lam finished")
    return convert_matched_for_return(M)


def greedy_matching(grid):
    while grid.G.number_of_nodes() > 50000:
        a, b, w = grid.get_edge_with_highest_weight()
        grid.reduce([a, b])
