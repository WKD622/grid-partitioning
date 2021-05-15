import operator

import networkx

from src.graph_utils.helpful_sets.helpers import update_helpfulness_of_neighbours, sort_vertices_helpfulness, \
    add_vertex_and_update_sets, pop_vertex_b_s, pop_vertex


def compute_k_prime(S_helpfulness, S_dash_helpfulness):
    return S_helpfulness - S_dash_helpfulness


def min_diff_value_to_consider(S_helpfulness, S_dash_helpfulness):
    return max(-2, - S_helpfulness + 1 + S_dash_helpfulness)


def filter_diff_values(vertices_helpfulness, S_helpfulness, S_dash_helpfulness):
    min_diff_val = min_diff_value_to_consider(S_helpfulness, S_dash_helpfulness)
    return list(filter(lambda vertex: vertex['helpfulness'] >= min_diff_val, vertices_helpfulness))


def contains_proper_diff_values(vertices_helpfulness, k_prime, S_dash_helpfulness):
    return len(filter_diff_values(vertices_helpfulness, k_prime, S_dash_helpfulness))


def _init_2_set():
    return [], 0


def contains_diff_values_greater_than_0(vertices_helpfulness):
    return len(vertices_helpfulness) > 0 and vertices_helpfulness[-1]['helpfulness'] >= 0


def _contains_sets_with_H_greater_or_equal_than_0(_2_coll):
    return len(_2_coll) > 0 and _2_coll[-1]['helpfulness'] >= 0


def search_for_balancing_set(G, vertices_helpfulness, S_size, S_helpfulness):
    success = False

    S_dash, S_dash_helpfulness = phase_1(G, vertices_helpfulness, S_size, S_helpfulness)
    S_dash, S_dash_helpfulness = phase_2(G, S_dash, S_dash_helpfulness, vertices_helpfulness, S_size,
                                         S_helpfulness)

    if S_dash_helpfulness <= S_helpfulness - 1 and len(S_dash) == S_size:
        success = True
    return S_dash, S_dash_helpfulness, success


def search_for_balancing_set_improved(G, vertices_helpfulness, S_size, S_helpfulness, min_, max_):
    success = False

    S_dash, S_dash_helpfulness = phase_1_improved(G, vertices_helpfulness, S_size, S_helpfulness, min_, max_)
    S_dash, S_dash_helpfulness = phase_2_improved(G, S_dash, S_dash_helpfulness, vertices_helpfulness, S_size,
                                                  S_helpfulness, min_, max_)

    if S_dash_helpfulness <= S_helpfulness - 1 and len(S_dash) == S_size:
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


def phase_1_improved(G, vertices_helpfulness, S_size, S_helpfulness, min_, max_):
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
    obj = {'list': _2_set, 'helpfulness': _2_set_helpfulness}
    _2_coll.append(obj)


def sort_2_coll_on_helpfulness(_2_coll):
    _2_coll.sort(key=operator.itemgetter('helpfulness'))


def pop_2_set(_2_coll):
    obj = _2_coll.pop()
    return obj['list'], obj['helpfulness']


def create_set_from_list(_2_set):
    _set = set()
    for vertex in _2_set:
        _set.add(vertex['v_num'])
    return _set


def add_2_set_to_S_dash(_2_set, S_dash):
    _set = create_set_from_list(_2_set)
    S_dash |= _set


def get_vertices_to_update_helpfulness(G, _2_set):
    vertices_set = create_set_from_list(_2_set)
    vertices_to_update = set()
    for v_num in vertices_set:
        vertices_to_update |= set(networkx.all_neighbors(G, v_num))

    return vertices_to_update


def update_helpfulness_of_2_coll(G, _2_set, _2_coll):
    to_update = get_vertices_to_update_helpfulness(G, _2_set)
    for _set in _2_coll:
        count = 0
        for vertex in _set['list']:
            if vertex['v_num'] in to_update:
                vertex['helpfulness'] += 2
                count += 2
        _set['helpfulness'] += count
    sort_2_coll_on_helpfulness(_2_coll)


def update_helpfulness_of_big_set(G, _2_set, big_set):
    to_update = get_vertices_to_update_helpfulness(G, _2_set)
    for vertex in big_set:
        if vertex['v_num'] in to_update:
            vertex['helpfulness'] -= 2


def reduce_S_prim(S_prim, number_of_elements_to_pop):
    while len(S_prim) > 0 and len(S_prim) > number_of_elements_to_pop:
        S_prim.pop()


def phase_2(G, S_dash, S_dash_helpfulness, big_set, S_size, S_helpfulness):
    _2_coll = []

    while (len(S_dash) < S_size
           and contains_proper_diff_values(big_set, S_helpfulness, S_dash_helpfulness)):
        vertices_to_consider = filter_diff_values(big_set, S_helpfulness, S_dash_helpfulness)

        v_num, v_helpfulness = pop_vertex_b_s(vertices_to_consider, big_set)
        _2_set, _2_set_helpfulness = _init_2_set()
        _2_set_helpfulness = add_vertex_and_update_sets(G=G,
                                                        v_num=v_num,
                                                        v_helpfulness=v_helpfulness,
                                                        helpful_set=_2_set,
                                                        set_helpfulness=_2_set_helpfulness,
                                                        big_set=big_set)

        while (_2_set_helpfulness < 0
               and len(_2_set) + len(S_dash) < S_size
               and contains_diff_values_greater_than_0(big_set)):
            v_num, v_helpfulness = pop_vertex(big_set)
            _2_set_helpfulness = add_vertex_and_update_sets(G=G,
                                                            v_num=v_num,
                                                            v_helpfulness=v_helpfulness,
                                                            helpful_set=_2_set,
                                                            set_helpfulness=_2_set_helpfulness,
                                                            big_set=big_set)

        if _2_set_helpfulness >= 0:
            add_2_set_to_S_dash(_2_set, S_dash)
            update_helpfulness_of_2_coll(G, _2_set, _2_coll)
            while len(S_dash) < S_size and _contains_sets_with_H_greater_or_equal_than_0(_2_coll):
                S_prim, S_prim_helpfulness = pop_2_set(_2_coll)
                if len(S_prim) + len(S_dash) < S_size:
                    add_2_set_to_S_dash(S_prim, S_dash)
                else:
                    reduce_S_prim(S_prim, S_size - len(S_dash))
                    add_2_set_to_S_dash(S_prim, S_dash)
        elif len(_2_set) + len(S_dash) == S_size:
            add_2_set_to_S_dash(_2_set, S_dash)
            update_helpfulness_of_2_coll(G, _2_set, _2_coll)
        else:
            update_helpfulness_of_big_set(G, _2_set, big_set)
            add_set_to_2_coll(_2_set, _2_set_helpfulness, _2_coll)
            sort_2_coll_on_helpfulness(_2_coll)

    return S_dash, S_dash_helpfulness


def phase_2_improved(G, S_dash, S_dash_helpfulness, big_set, S_size, S_helpfulness, min_, max_):
    _2_coll = []

    while (len(S_dash) < S_size
           and contains_proper_diff_values(big_set, S_helpfulness, S_dash_helpfulness)):
        vertices_to_consider = filter_diff_values(big_set, S_helpfulness, S_dash_helpfulness)

        v_num, v_helpfulness = pop_vertex_b_s(vertices_to_consider, big_set)
        _2_set, _2_set_helpfulness = _init_2_set()
        _2_set_helpfulness = add_vertex_and_update_sets(G=G,
                                                        v_num=v_num,
                                                        v_helpfulness=v_helpfulness,
                                                        helpful_set=_2_set,
                                                        set_helpfulness=_2_set_helpfulness,
                                                        big_set=big_set)

        while (_2_set_helpfulness < 0
               and len(_2_set) + len(S_dash) < S_size
               and contains_diff_values_greater_than_0(big_set)):
            v_num, v_helpfulness = pop_vertex(big_set)
            _2_set_helpfulness = add_vertex_and_update_sets(G=G,
                                                            v_num=v_num,
                                                            v_helpfulness=v_helpfulness,
                                                            helpful_set=_2_set,
                                                            set_helpfulness=_2_set_helpfulness,
                                                            big_set=big_set)

        if _2_set_helpfulness >= 0:
            add_2_set_to_S_dash(_2_set, S_dash)
            update_helpfulness_of_2_coll(G, _2_set, _2_coll)
            while len(S_dash) < S_size and _contains_sets_with_H_greater_or_equal_than_0(_2_coll):
                S_prim, S_prim_helpfulness = pop_2_set(_2_coll)
                if len(S_prim) + len(S_dash) < S_size:
                    add_2_set_to_S_dash(S_prim, S_dash)
                else:
                    reduce_S_prim(S_prim, S_size - len(S_dash))
                    add_2_set_to_S_dash(S_prim, S_dash)
        elif len(_2_set) + len(S_dash) == S_size:
            add_2_set_to_S_dash(_2_set, S_dash)
            update_helpfulness_of_2_coll(G, _2_set, _2_coll)
        else:
            update_helpfulness_of_big_set(G, _2_set, big_set)
            add_set_to_2_coll(_2_set, _2_set_helpfulness, _2_coll)
            sort_2_coll_on_helpfulness(_2_coll)

    return S_dash, S_dash_helpfulness
