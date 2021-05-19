import operator

import networkx

from src.graph_utils.helpful_sets.helpers import update_helpfulness_of_neighbours, sort_vertices_helpfulness


def determine_partition_weight(G, partition_vertices):
    partition_weight = 0
    min_partition_weight = float("inf")
    max_partition_weight = -float("inf")
    for v_num in partition_vertices:
        v_weight = G.nodes[v_num]['data']['weight']
        partition_weight += v_weight
        if v_weight < min_partition_weight:
            min_partition_weight = v_weight
        if v_weight > max_partition_weight:
            max_partition_weight = v_weight
    grace = max_partition_weight / 2
    return partition_weight, max_partition_weight, min_partition_weight, grace


def determine_max_and_min_weight_for_balancing_set(G, S_a_weight, partition_vertices):
    partition_weight, max_weight, min_weight, grace = determine_partition_weight(G, partition_vertices)
    min_ = abs(S_a_weight - max_weight - grace)
    max_ = abs(S_a_weight - min_weight + grace)
    return min_, max_


def sort_2_coll_on_helpfulness(_2_coll):
    _2_coll.sort(key=operator.itemgetter('helpfulness'))


def create_set_from_list(_2_set):
    _set = set()
    for vertex in _2_set:
        _set.add(vertex['v_num'])
    return _set


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


def contains_diff_values_greater_than_0(vertices_helpfulness):
    return len(vertices_helpfulness) > 0 and vertices_helpfulness[-1]['helpfulness'] >= 0


def _contains_sets_with_H_greater_or_equal_than_0(_2_coll):
    return len(_2_coll) > 0 and _2_coll[-1]['helpfulness'] >= 0


def compute_k_prime(S_helpfulness, S_dash_helpfulness):
    return S_helpfulness - S_dash_helpfulness


def min_diff_value_to_consider(S_helpfulness, S_dash_helpfulness):
    return max(-2, - S_helpfulness + 1 + S_dash_helpfulness)


def filter_diff_values(vertices_helpfulness, S_helpfulness, S_dash_helpfulness):
    min_diff_val = min_diff_value_to_consider(S_helpfulness, S_dash_helpfulness)
    return list(filter(lambda vertex: vertex['helpfulness'] >= min_diff_val, vertices_helpfulness))


def contains_proper_diff_values(vertices_helpfulness, k_prime, S_dash_helpfulness):
    return len(filter_diff_values(vertices_helpfulness, k_prime, S_dash_helpfulness))


def add_vertex_and_update_sets(G, v_num, v_helpfulness, v_weight, helpful_set, set_helpfulness, set_weight, big_set):
    helpful_set.append({'v_num': v_num, 'helpfulness': v_helpfulness})
    set_helpfulness += v_helpfulness
    set_weight += v_weight
    update_helpfulness_of_neighbours(G, v_num, big_set)
    sort_vertices_helpfulness(big_set)
    return set_helpfulness, set_weight
