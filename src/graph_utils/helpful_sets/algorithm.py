from math import log, ceil

from src.graph_utils.helpful_sets.balance_sets_greedily import balance_greedily
from src.graph_utils.helpful_sets.balancing_set import search_for_balancing_set, search_for_balancing_set_improved
from src.graph_utils.helpful_sets.helpers import (set_helpfulness_for_vertices,
                                                  count_cut_size,
                                                  move_set_to_another_partition, swap_partitions,
                                                  determine_max_and_min_weight_for_balancing_set)
from src.graph_utils.helpful_sets.helpful_set import search_for_helpful_set, search_for_helpful_set_improved


def improve_bisection(G, partition_a, partition_b, partitions_vertices):
    a_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices[partition_a], partition_b)
    cut_size = count_cut_size(G, partitions_vertices, partition_a, partition_b)
    limit = cut_size / 2

    while limit > 1:
        S, S_helpfulness = search_for_helpful_set(G, a_vertices_helpfulness, limit)
        if limit > S_helpfulness > 0:
            limit = S_helpfulness
        elif S_helpfulness <= 0:
            S = set()
            limit = 0

        if len(S) > 0:
            move_set_to_another_partition(G, partition_a, partition_b, partitions_vertices, S)
            b_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices[partition_b], partition_a)
            S_dash, S_dash_helpfulness, success = search_for_balancing_set(G, b_vertices_helpfulness, len(S),
                                                                           S_helpfulness)
            if success:
                move_set_to_another_partition(G, partition_b, partition_a, partitions_vertices, S_dash)
                a_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices[partition_a], partition_b)
                limit *= 2
            else:
                move_set_to_another_partition(G, partition_b, partition_a, partitions_vertices, S)
                a_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices[partition_a], partition_b)
                limit /= 2


def improve_bisection_improved(G, partition_a, partition_b, partitions_vertices):
    a_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices[partition_a], partition_b)
    b_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices[partition_a], partition_b)
    cut_size = count_cut_size(G, partitions_vertices, partition_a, partition_b)
    limit_a = cut_size / 2
    limit_b = limit_a
    S_max = 128

    while limit_a + limit_b > 1:
        if limit_a == 0 or (2 * limit_a) < limit_b:
            b_vertices_helpfulness, limit_b, partition_b, a_vertices_helpfulness, limit_a, partition_a = \
                swap_partitions(a_vertices_helpfulness, limit_a, partition_a,
                                b_vertices_helpfulness, limit_b, partition_b)

        S_a, S_a_helpfulness = search_for_helpful_set_improved(G, a_vertices_helpfulness, limit_a, -2, S_max)

        if S_a_helpfulness < limit_a:
            limit_a = S_a_helpfulness
            if limit_b > S_a_helpfulness:

                S_b, S_b_helpfulness = search_for_helpful_set_improved(G, b_vertices_helpfulness, limit_b, -2, S_max)
                if S_b_helpfulness >= S_a_helpfulness:
                    b_vertices_helpfulness, limit_b, partition_b, a_vertices_helpfulness, limit_a, partition_a = \
                        swap_partitions(a_vertices_helpfulness, limit_a, partition_a,
                                        b_vertices_helpfulness, limit_b, partition_b)
                else:
                    limit_b = S_b_helpfulness

        if S_a_helpfulness < 0:
            limit_a = a_vertices_helpfulness
            continue

        limit_a = min(limit_a, S_a_helpfulness)
        move_set_to_another_partition(G, partition_a, partition_b, partitions_vertices, S_a)
        min_, max_ = determine_max_and_min_weight_for_balancing_set(G, partitions_vertices[partition_b])
        S_b, S_b_helpfulness = search_for_balancing_set_improved(G, b_vertices_helpfulness, len(S_a), S_a_helpfulness,
                                                                 min_, max_)
        if S_b_helpfulness > S_a_helpfulness:
            # TODO
            move_set_to_another_partition(G, partition_b, partition_a, partitions_vertices, S_b)
            limit_a += ceil(log(limit_a))
            limit_b += 1
        else:
            move_set_to_another_partition(G, partition_b, partition_a, partitions_vertices, S_a)
            limit_a /= 4
            limit_b /= 2

    balance_greedily(G, partition_a, partition_b, partitions_vertices)
