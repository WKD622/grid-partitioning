from src.graph_utils.helpful_sets.helpers import update_helpfulness_of_neighbours, sort_vertices_helpfulness, pop_vertex


def compute_k_prime(S_helpfulness, S_dash_helpfulness):
    return S_helpfulness - S_dash_helpfulness


def min_diff_value_to_consider(k_prime):
    return max(-2, -k_prime + 1)


def filter_diff_values(vertices_helpfulness, k_prime):
    min_diff_val = min_diff_value_to_consider(k_prime)
    return list(filter(lambda vertex: vertex['helpfulness'] > min_diff_val, vertices_helpfulness))


def contains_proper_diff_values(vertices_helpfulness, k_prime):
    return len(filter_diff_values(vertices_helpfulness, k_prime))


def _init_2_set():
    return set(), 0


def contains_diff_values_greater_than_0(vertices_helpfulness):
    return vertices_helpfulness[-1]['helpfulness'] >= 0


def search_for_balancing_set(G, vertices_helpfulness, S_size, S_helpfulness):
    success = False

    S_dash, S_dash_helpfulness = phase_1(G, vertices_helpfulness, S_size, S_helpfulness)

    phase_2(G, S_dash, S_dash_helpfulness, vertices_helpfulness, S_size,
            S_helpfulness)

    if S_dash_helpfulness <= S_helpfulness - 1:
        success = True
    return S_dash, S_dash_helpfulness, success


def phase_1(G, vertices_helpfulness, S_size, S_helpfulness):
    set_helpfulness = 0
    helpful_set = set()
    end = False
    while (not end
           and len(helpful_set) < S_size
           and set_helpfulness < S_helpfulness - 1
           and len(vertices_helpfulness) > 0):
        vertex_data = vertices_helpfulness.pop()
        vertex_helpfulness = vertex_data['helpfulness']
        vertex_num = vertex_data['v_num']
        if vertex_helpfulness < 0:
            end = True
        else:
            set_helpfulness += vertex_helpfulness
            helpful_set.add(vertex_num)
            update_helpfulness_of_neighbours(G, vertex_num, vertices_helpfulness)
            sort_vertices_helpfulness(vertices_helpfulness)

    return helpful_set, set_helpfulness


def phase_2(G, S_dash, S_dash_helpfulness, big_set, S_size, S_helpfulness):
    _2_coll = set()
    end = False
    while (not end
           and len(S_dash) < S_size
           and contains_proper_diff_values(big_set, -2)):
        vertices_to_consider = filter_diff_values(big_set, -2)

        vertex_num, vertex_helpfulness = pop_vertex(vertices_to_consider)
        _2_set, _2_set_helpfulness = _init_2_set()
        _2_set.add(vertex_num)
        _2_set_helpfulness += vertex_helpfulness

        while (_2_set_helpfulness < 0
               and len(_2_set) + S_dash < S_size
               and contains_diff_values_greater_than_0(vertices_to_consider)):
            vertex_num, vertex_helpfulness = pop_vertex(vertices_to_consider)
            _2_set.add(vertex_num)
            _2_set_helpfulness += vertex_helpfulness

        if _2_set_helpfulness >= 0:
            pass
        elif len(_2_set) + len(S_dash) == S_size:
            pass
        else:
            _2_coll.add(_2_set)

    return S_dash, S_dash_helpfulness
