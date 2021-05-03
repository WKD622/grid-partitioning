import operator

from src.graph_utils.helpful_sets.helpers import update_helpfulness_of_neighbours, sort_vertices_helpfulness, \
    pop_vertex, add_vertex_and_update_sets


def compute_k_prime(S_helpfulness, S_dash_helpfulness):
    return S_helpfulness - S_dash_helpfulness


def min_diff_value_to_consider(S_helpfulness, S_dash_helpfulness):
    return max(-2, - S_helpfulness + 1 + S_dash_helpfulness)


def filter_diff_values(vertices_helpfulness, S_helpfulness, S_dash_helpfulness):
    min_diff_val = min_diff_value_to_consider(S_helpfulness, S_dash_helpfulness)
    return list(filter(lambda vertex: vertex['helpfulness'] > min_diff_val, vertices_helpfulness))


def contains_proper_diff_values(vertices_helpfulness, k_prime, S_dash_helpfulness):
    return len(filter_diff_values(vertices_helpfulness, k_prime, S_dash_helpfulness))


def _init_2_set():
    return set(), 0


def contains_diff_values_greater_than_0(vertices_helpfulness):
    return len(vertices_helpfulness) > 0 and vertices_helpfulness[-1]['helpfulness'] >= 0


def _contains_sets_with_H_greater_or_equal_than_0(_2_coll):
    return len(_2_coll) > 0 and _2_coll[-1]['helpfulness'] >= 0


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


def add_set_to_2_coll(_2_set, _2_set_helpfulness, _2_coll):
    obj = {'set': _2_set, 'helpfulness': _2_set_helpfulness}
    _2_coll.append(obj)


def sort_2_coll_on_helpfulness(_2_coll):
    _2_coll.sort(key=operator.itemgetter('helpfulness'))


def pop_2_set(_2_coll):
    _2_set = _2_coll.pop()
    return _2_set['set'], _2_set['helpfulness']


def phase_2(G, S_dash, S_dash_helpfulness, big_set, S_size, S_helpfulness):
    _2_coll = []
    while (len(S_dash) < S_size
           and contains_proper_diff_values(big_set, S_helpfulness, S_dash_helpfulness)):
        vertices_to_consider = filter_diff_values(big_set, S_helpfulness, S_dash_helpfulness)

        v_num, v_helpfulness = pop_vertex(vertices_to_consider)
        _2_set, _2_set_helpfulness = _init_2_set()
        _2_set_helpfulness = add_vertex_and_update_sets(G, v_num, v_helpfulness, _2_set, _2_set_helpfulness,
                                                        vertices_to_consider)

        while (_2_set_helpfulness < 0
               and len(_2_set) + len(S_dash) < S_size
               and contains_diff_values_greater_than_0(vertices_to_consider)):
            v_num, v_helpfulness = pop_vertex(vertices_to_consider)
            _2_set_helpfulness = add_vertex_and_update_sets(G, v_num, v_helpfulness, _2_set, _2_set_helpfulness,
                                                            vertices_to_consider)

        if _2_set_helpfulness >= 0:
            S_dash |= _2_set
            while len(S_dash) < S_size and _contains_sets_with_H_greater_or_equal_than_0(_2_coll):
                S_prim, S_prim_helpfulness = pop_2_set(_2_coll)
                if len(S_prim) + len(S_dash) < S_size:
                    S_dash |= S_prim
                else:
                    pass
        elif len(_2_set) + len(S_dash) == S_size:
            S_dash |= _2_set
        else:
            add_set_to_2_coll(_2_set, _2_set_helpfulness, _2_coll)
            sort_2_coll_on_helpfulness(_2_coll)

    return S_dash, S_dash_helpfulness
