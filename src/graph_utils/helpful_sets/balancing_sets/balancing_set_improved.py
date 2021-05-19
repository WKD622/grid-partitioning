from src.graph_utils.helpful_sets.balancing_sets.helpers import (contains_proper_diff_values, filter_diff_values,
                                                                 contains_diff_values_greater_than_0,
                                                                 update_helpfulness_of_2_coll,
                                                                 _contains_sets_with_H_greater_or_equal_than_0,
                                                                 update_helpfulness_of_big_set,
                                                                 sort_2_coll_on_helpfulness, create_set_from_list)
from src.graph_utils.helpful_sets.helpers import (update_helpfulness_of_neighbours, sort_vertices_helpfulness,
                                                  pop_vertex_improved)


def search_for_balancing_set_improved(G, vertices_helpfulness, S_helpfulness, min_, max_):
    success = False

    S_dash, S_dash_helpfulness, S_dash_weight = phase_1_improved(G=G,
                                                                 vertices_helpfulness=vertices_helpfulness,
                                                                 S_helpfulness=S_helpfulness,
                                                                 max_=max_)
    S_dash, S_dash_helpfulness, S_dash_weight = phase_2_improved(G=G,
                                                                 S_dash=S_dash,
                                                                 S_dash_helpfulness=S_dash_helpfulness,
                                                                 S_dash_weight=S_dash_weight,
                                                                 big_set=vertices_helpfulness,
                                                                 S_helpfulness=S_helpfulness,
                                                                 max_=max_)

    if S_dash_helpfulness <= S_helpfulness - 1 and min_ <= S_dash_weight <= max_:
        success = True
    return S_dash, S_dash_helpfulness, success


def phase_1_improved(G, vertices_helpfulness, S_helpfulness, max_):
    set_helpfulness = 0
    set_weight = 0
    helpful_set = set()
    end = False
    while (not end
           and len(vertices_helpfulness) > 0):
        vertex_data = vertices_helpfulness.pop()
        vertex_helpfulness = vertex_data['helpfulness']
        vertex_num = vertex_data['v_num']
        vertex_weight = G.nodes[vertex_num]['data']['weight']
        if (vertex_helpfulness < 0
                or vertex_weight + set_weight > max_
                or set_helpfulness + vertex_helpfulness >= S_helpfulness - 1):
            end = True
        else:
            set_helpfulness += vertex_helpfulness
            set_weight += vertex_weight
            helpful_set.add(vertex_num)
            update_helpfulness_of_neighbours(G, vertex_num, vertices_helpfulness)
            sort_vertices_helpfulness(vertices_helpfulness)

    return helpful_set, set_helpfulness, set_weight


def phase_2_improved(G, S_dash, S_dash_helpfulness, S_dash_weight, big_set, S_helpfulness, max_):
    _2_coll = []

    while (S_dash_weight < max_
           and contains_proper_diff_values(big_set, S_helpfulness, S_dash_helpfulness)):
        vertices_to_consider = filter_diff_values(big_set, S_helpfulness, S_dash_helpfulness)

        # start building helpful set with the max helpful node
        v_num, v_helpfulness, v_weight = pop_vertex_b_s(G, vertices_to_consider, big_set)
        _2_set, _2_set_helpfulness, _2_set_weight = init_2_set_improved()
        _2_set_helpfulness, _2_set_weight = add_vertex_and_update_sets(G=G,
                                                                       v_num=v_num,
                                                                       v_helpfulness=v_helpfulness,
                                                                       v_weight=v_weight,
                                                                       helpful_set=_2_set,
                                                                       set_helpfulness=_2_set_helpfulness,
                                                                       set_weight=_2_set_weight,
                                                                       big_set=big_set)

        while (_2_set_helpfulness < 0
               and S_dash_weight + _2_set_weight <= max_
               and contains_diff_values_greater_than_0(big_set)):
            v_num, v_helpfulness, v_weight = pop_vertex_improved(G, big_set)
            _2_set_helpfulness, _2_set_weight = add_vertex_and_update_sets(G=G,
                                                                           v_num=v_num,
                                                                           v_helpfulness=v_helpfulness,
                                                                           v_weight=v_weight,
                                                                           helpful_set=_2_set,
                                                                           set_helpfulness=_2_set_helpfulness,
                                                                           set_weight=_2_set_weight,
                                                                           big_set=big_set)

        if _2_set_helpfulness >= 0:
            S_dash_weight = add_2_set_to_S_dash_improved(_2_set, _2_set_weight, S_dash, S_dash_weight)
            update_helpfulness_of_2_coll(G, _2_set, _2_coll)
            while (S_dash_weight < max_
                   and _contains_sets_with_H_greater_or_equal_than_0(_2_coll)):
                S_prim, S_prim_helpfulness, S_prim_weight = pop_2_set_improved(_2_coll)
                if S_prim_weight + S_dash_weight < max_:
                    S_dash_weight = add_2_set_to_S_dash_improved(S_prim, S_prim_weight, S_dash, S_dash_weight)
                else:
                    S_prim_weight = reduce_S_prim_improved(G, S_prim, S_prim_weight, max_ - S_dash_weight)
                    S_dash_weight = add_2_set_to_S_dash_improved(S_prim, S_prim_weight, S_dash, S_dash_weight)

        elif S_dash_weight + _2_set_weight <= max_:
            S_dash_weight = add_2_set_to_S_dash_improved(_2_set, _2_set_weight, S_dash, S_dash_weight)
            update_helpfulness_of_2_coll(G, _2_set, _2_coll)

        else:
            update_helpfulness_of_big_set(G, _2_set, big_set)
            add_set_to_2_coll_improved(_2_set, _2_set_helpfulness, _2_set_weight, _2_coll)
            sort_2_coll_on_helpfulness(_2_coll)

    return S_dash, S_dash_helpfulness, S_dash_weight


def reduce_S_prim_improved(G, S_prim, S_prim_weight, weight_to_remove):
    while len(S_prim) > 0 and S_prim_weight > weight_to_remove:
        node = S_prim.pop()
        S_prim_weight -= G.nodes[node['v_num']]['data']['weight']
    return S_prim_weight


def add_2_set_to_S_dash_improved(_2_set, _2_set_weight, S_dash, S_dash_weight):
    _set = create_set_from_list(_2_set)
    S_dash |= _set
    return S_dash_weight + _2_set_weight


def pop_2_set_improved(_2_coll):
    obj = _2_coll.pop()
    return obj['list'], obj['helpfulness'], obj['weight']


def add_set_to_2_coll_improved(_2_set, _2_set_helpfulness, _2_set_weight, _2_coll):
    obj = {'list': _2_set, 'helpfulness': _2_set_helpfulness, 'weight': _2_set_weight}
    _2_coll.append(obj)


def init_2_set_improved():
    return [], 0, 0


def pop_vertex_b_s(G, vertices_helpfulness, big_set):
    vertex_data = vertices_helpfulness.pop()
    vertex_helpfulness = vertex_data['helpfulness']
    vertex_num = vertex_data['v_num']
    vertex_weight = G.nodes[vertex_num]['data']['weight']
    big_set.remove(vertex_data)
    return vertex_num, vertex_helpfulness, vertex_weight


def add_vertex_and_update_sets(G, v_num, v_helpfulness, v_weight, helpful_set, set_helpfulness, set_weight, big_set):
    helpful_set.append({'v_num': v_num, 'helpfulness': v_helpfulness})
    set_helpfulness += v_helpfulness
    set_weight += v_weight
    update_helpfulness_of_neighbours(G, v_num, big_set)
    sort_vertices_helpfulness(big_set)
    return set_helpfulness, set_weight
