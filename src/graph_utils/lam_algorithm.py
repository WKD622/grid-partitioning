import random


def is_free(M, v):
    return v not in M


def is_matched(M, v):
    return v in M


def get_unchecked_edges(G, U, v):
    adj_vertices = set(G.adj[v].keys())
    adj_edges = set()
    for x in adj_vertices:
        adj_edges.add((v, x))
    return U & adj_edges


def get_adj_unchecked_vertex(G, U, v):
    (k, l) = get_unchecked_edges(G, U, v).pop()
    if k == v:
        return l
    return k


def there_are_unchecked_edges(G, U, v):
    return bool(get_unchecked_edges(G, U, v))


def can_be_matched(G, a, b, m_c):
    return G.degree[a] + G.degree[b] < m_c


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
        S.remove(b, a)


def move_edge(from_, to_, a, b):
    if edge_ab_in_set(from_, a, b):
        remove_edge_from_set(from_, a, b)
        to_.add((a, b))
    else:
        raise Exception("No edge: (" + a + ", " + b + ") to move.")


def to_remove(R, C):
    for x in C:
        a, b = x
        R.add((a, b))
    C.clear()


def remove_all_matched_edges(R, M, C, v):
    for x in C:
        k, l = x
        if (is_matched(M, k) and l == v) or (is_matched(M, l) and k == v):
            move_edge(C, R, k, l)


def all_adj_matched(G, M, v):
    all_matched = True
    for w in set(G.adj[v].keys()):
        all_matched = all_matched and w in M
    return all_matched


def restore_all_free_edges(U, M, C, v):
    edges_to_be_moved = []
    for x in C:
        k, l = x
        if (is_free(M, k) and l == v) or is_free(M, l) and k == v:
            edges_to_be_moved.append((k, l))

    for x in edges_to_be_moved:
        k, l = x
        move_edge(C, U, k, l)


def get_smallest_and_highest_degrees(G):
    degrees = sorted((d, n) for n, d in G.degree())
    highest_degree, _ = degrees[-1]
    smallest_degree, _ = degrees[0]
    return highest_degree, smallest_degree


def remove_adj_edges(G, U, v):
    for x in get_unchecked_edges(G, U, v):
        k, l = x
        remove_edge_from_set(U, k, l)


def try_match(G, a, b, R, U, M, m_c):
    C_a = set()
    C_b = set()
    while is_free(M, a) and is_free(M, b) and (
            there_are_unchecked_edges(G, U, a) or there_are_unchecked_edges(G, U, b)):
        if is_free(M, a) and there_are_unchecked_edges(G, U, a):
            c = get_adj_unchecked_vertex(G, U, a)
            move_edge(U, C_a, a, c)
            if get_weight(G, a, c) > get_weight(G, a, b):
                try_match(G, a, c, R, U, M, m_c)
        if is_free(M, b) and there_are_unchecked_edges(G, U, b):
            d = get_adj_unchecked_vertex(G, U, b)
            move_edge(U, C_b, b, d)
            if get_weight(G, b, d) > get_weight(G, a, b):
                try_match(G, b, d, R, U, M, m_c)

    is_free_a = is_free(M, a)
    is_free_b = is_free(M, b)
    if is_matched(M, a) and is_free_b:
        restore_all_free_edges(U, M, C_b, b)
        if all_adj_matched(G, M, b):
            remove_adj_edges(G, U, b)
    elif is_matched(M, b) and is_free_a:
        restore_all_free_edges(U, M, C_a, a)
        if all_adj_matched(G, M, a):
            remove_adj_edges(G, U, a)
    elif is_free_a and is_free_b and can_be_matched(G, a, b, m_c):
        match(M, a, b)


def draw_an_edge(edges):
    index = random.randint(0, len(edges) - 1)
    return list(edges)[index]


def convert_matched_for_return(M):
    M_out = []
    for key, value in M.items():
        if {key, value} not in M_out and {value, key} not in M_out:
            M_out.append({key, value})
    return M_out


def lam_algorithm(G):
    M = {}
    U = set(G.edges)
    R = set()
    i = 10
    h_deg, s_deg = get_smallest_and_highest_degrees(G)
    m_c = 2 * s_deg + h_deg

    while len(U) != 0:
        print(U)
        print(convert_matched_for_return(M))
        # prev_U = U.copy()
        a, b = draw_an_edge(U)
        try_match(G, a, b, R, U, M, m_c)
        # if i == 0:
        #     break
        # if len(prev_U) == len(U):
        #     i -= 1
        # if len(prev_U) != len(U):
        #     i = 5
    return convert_matched_for_return(M)
