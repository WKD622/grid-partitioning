from src.graph_utils.helpful_sets.balancing_sets.helpers import (create_set_from_list, sort_2_coll_on_helpfulness,
                                                                 update_helpfulness_of_big_set,
                                                                 update_helpfulness_of_2_coll,
                                                                 _contains_sets_with_H_greater_or_equal_than_0,
                                                                 contains_diff_values_greater_than_0,
                                                                 contains_proper_diff_values, filter_diff_values)
from src.graph_utils.helpful_sets.helpers import (update_helpfulness_of_neighbours, sort_vertices_helpfulness,
                                                  pop_vertex)


def search_for_balancing_set(G, vertices_helpfulness, S_size, S_helpfulness, partitions, adjacent_partition):
    success = False

    S_dash, S_dash_helpfulness = phase_1(G, vertices_helpfulness, S_size, S_helpfulness, partitions)
    S_dash, S_dash_helpfulness = phase_2(G, S_dash, S_dash_helpfulness, vertices_helpfulness, S_size,
                                         S_helpfulness, partitions, adjacent_partition)

    if S_dash_helpfulness <= S_helpfulness - 1 and len(S_dash) == S_size:
        success = True
    return S_dash, S_dash_helpfulness, success


def phase_1(G, vertices_helpfulness, S_size, S_helpfulness, partitions):
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
            update_helpfulness_of_neighbours(G, vertex_num, vertices_helpfulness, partitions)
            sort_vertices_helpfulness(G, vertices_helpfulness)

    return helpful_set, set_helpfulness


def phase_2(G, S_dash, S_dash_helpfulness, big_set, S_size, S_helpfulness, partitions, adjacent_partition):
    _2_coll = []

    while (len(S_dash) < S_size
           and contains_proper_diff_values(G, big_set, S_helpfulness, S_dash_helpfulness, adjacent_partition,
                                           partitions)):
        vertices_to_consider = filter_diff_values(G, big_set, S_helpfulness, S_dash_helpfulness, adjacent_partition,
                                                  partitions)

        v_num, v_helpfulness = pop_vertex_b_s(vertices_to_consider, big_set)
        _2_set, _2_set_helpfulness = init_2_set()
        _2_set_helpfulness = add_vertex_and_update_sets(G=G,
                                                        v_num=v_num,
                                                        v_helpfulness=v_helpfulness,
                                                        helpful_set=_2_set,
                                                        set_helpfulness=_2_set_helpfulness,
                                                        big_set=big_set,
                                                        partitions=partitions)

        while (_2_set_helpfulness < 0
               and len(_2_set) + len(S_dash) < S_size
               and contains_diff_values_greater_than_0(big_set)):
            v_num, v_helpfulness = pop_vertex(big_set)
            _2_set_helpfulness = add_vertex_and_update_sets(G=G,
                                                            v_num=v_num,
                                                            v_helpfulness=v_helpfulness,
                                                            helpful_set=_2_set,
                                                            set_helpfulness=_2_set_helpfulness,
                                                            big_set=big_set,
                                                            partitions=partitions)

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


def add_set_to_2_coll(_2_set, _2_set_helpfulness, _2_coll):
    obj = {'list': _2_set, 'helpfulness': _2_set_helpfulness}
    _2_coll.append(obj)


def init_2_set():
    return [], 0


def pop_2_set(_2_coll):
    obj = _2_coll.pop()
    return obj['list'], obj['helpfulness']


def add_2_set_to_S_dash(_2_set, S_dash):
    _set = create_set_from_list(_2_set)
    S_dash |= _set


def reduce_S_prim(S_prim, number_of_elements_to_pop):
    while len(S_prim) > 0 and len(S_prim) > number_of_elements_to_pop:
        S_prim.pop()


def pop_vertex_b_s(vertices_helpfulness, big_set):
    vertex_data = vertices_helpfulness.pop()
    vertex_helpfulness = vertex_data['helpfulness']
    vertex_num = vertex_data['v_num']
    big_set.remove(vertex_data)
    return vertex_num, vertex_helpfulness


def add_vertex_and_update_sets(G, v_num, v_helpfulness, helpful_set, set_helpfulness, big_set, partitions):
    helpful_set.append({'v_num': v_num, 'helpfulness': v_helpfulness})
    set_helpfulness += v_helpfulness
    update_helpfulness_of_neighbours(G, v_num, big_set, partitions)
    sort_vertices_helpfulness(G, big_set)
    return set_helpfulness
