from math import ceil, log

from src.graph_utils.helpful_sets.balancing_sets.balance_sets_greedily import balance_greedily
from src.graph_utils.helpful_sets.balancing_sets.balancing_set import search_for_balancing_set
from src.graph_utils.helpful_sets.balancing_sets.balancing_set_improved import search_for_balancing_set_improved
from src.graph_utils.helpful_sets.balancing_sets.helpers import determine_max_and_min_weight_for_balancing_set
from src.graph_utils.helpful_sets.helpers import set_helpfulness_for_vertices, count_cut_size, move_set, swap_partitions
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
            move_set(G, partition_a, partition_b, partitions_vertices, S)
            b_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices[partition_b], partition_a)
            S_dash, S_dash_helpfulness, success = search_for_balancing_set(G, b_vertices_helpfulness, len(S),
                                                                           S_helpfulness)
            if success:
                move_set(G, partition_b, partition_a, partitions_vertices, S_dash)
                a_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices[partition_a], partition_b)
                limit *= 2
            else:
                move_set(G, partition_b, partition_a, partitions_vertices, S)
                a_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices[partition_a], partition_b)
                limit /= 2


def improve_bisection_improved(G, partition_a, partition_b, partitions_vertices, partitions_stats):
    a_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices[partition_a], partition_b)
    b_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices[partition_b], partition_a)
    cut_size = count_cut_size(G, partitions_vertices, partition_a, partition_b)
    limit_a = cut_size / 2
    limit_b = cut_size / 2
    S_max = 128

    while limit_a + limit_b > 0.5:

        if limit_a == 0 or (2 * limit_a) < limit_b:
            a_vertices_helpfulness, limit_a, partition_a, b_vertices_helpfulness, limit_b, partition_b = \
                swap_partitions(v_h_1=a_vertices_helpfulness, l_1=limit_a, p_1=partition_a,
                                v_h_2=b_vertices_helpfulness, l_2=limit_b, p_2=partition_b)

        S_a, S_a_helpfulness, S_a_weight = search_for_helpful_set_improved(G, a_vertices_helpfulness, limit_a, 0,
                                                                           S_max)

        if S_a_helpfulness < limit_a:
            limit_a = S_a_helpfulness
            if limit_b > S_a_helpfulness:

                S_b, S_b_helpfulness, S_b_weight = search_for_helpful_set_improved(G, b_vertices_helpfulness, limit_b,
                                                                                   0, S_max)
                if S_b_helpfulness >= S_a_helpfulness:
                    a_vertices_helpfulness, limit_a, partition_a, b_vertices_helpfulness, limit_b, partition_b = \
                        swap_partitions(v_h_1=a_vertices_helpfulness, l_1=limit_a, p_1=partition_a,
                                        v_h_2=b_vertices_helpfulness, l_2=limit_b, p_2=partition_b)
                    S_a = S_b
                    S_a_weight = S_b_weight
                    S_a_helpfulness = S_b_helpfulness
                else:
                    limit_b = S_b_helpfulness

        if S_a_helpfulness < 0 or len(S_a) == 0:
            limit_a = 0
            continue

        limit_a = min(limit_a, S_a_helpfulness)
        move_set(G,
                 current_partition=partition_a,
                 dest_partition=partition_b,
                 partitions_vertices=partitions_vertices,
                 to_be_moved=S_a,
                 weight=S_a_weight,
                 partitions_stats=partitions_stats)

        b_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices[partition_b], partition_a)
        min_, max_ = determine_max_and_min_weight_for_balancing_set(G, S_a_weight, partitions_vertices[partition_b])
        S_b, S_b_helpfulness, S_b_weight, success = search_for_balancing_set_improved(G=G,
                                                                                      vertices_helpfulness=b_vertices_helpfulness,
                                                                                      min_=min_,
                                                                                      max_=max_,
                                                                                      S_helpfulness=S_a_helpfulness,
                                                                                      adjacent_partition=partition_a)

        if success and S_b_helpfulness > -S_a_helpfulness:
            move_set(G,
                     current_partition=partition_b,
                     dest_partition=partition_a,
                     partitions_vertices=partitions_vertices,
                     to_be_moved=S_b,
                     weight=S_b_weight,
                     partitions_stats=partitions_stats)
            limit_a += ceil(log(limit_a))
            limit_b += 1

        else:
            move_set(G,
                     current_partition=partition_b,
                     dest_partition=partition_a,
                     partitions_vertices=partitions_vertices,
                     to_be_moved=S_a,
                     weight=S_a_weight,
                     partitions_stats=partitions_stats)
            limit_a /= 4
            limit_b /= 2

        a_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices[partition_a], partition_b)
        b_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices[partition_b], partition_a)

    balance_greedily(G, partition_a, partition_b, partitions_vertices)
