import copy
from math import ceil, log

from src.graph_utils.helpful_sets.balancing_sets.balance_sets_greedily import balance_greedily
from src.graph_utils.helpful_sets.balancing_sets.balancing_set import search_for_balancing_set
from src.graph_utils.helpful_sets.balancing_sets.balancing_set_improved import search_for_balancing_set_improved
from src.graph_utils.helpful_sets.balancing_sets.helpers import determine_max_and_min_weight_for_balancing_set
from src.graph_utils.helpful_sets.helpers import set_helpfulness_for_vertices, count_cut_size, move_set, \
    swap_partitions, move_set_normal
from src.graph_utils.helpful_sets.helpful_set import search_for_helpful_set, search_for_helpful_set_improved


def improve_bisection(G, partitions, partition_a, partition_b, partitions_vertices, partitions_stats):
    a_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices[partition_a], partition_b, partitions)
    cut_size = count_cut_size(G, partitions, partitions_vertices, partition_a, partition_b)
    limit = cut_size / 2

    while limit > 1:
        S, S_helpfulness = search_for_helpful_set(G, a_vertices_helpfulness, limit, partitions)
        if limit > S_helpfulness > 0:
            limit = S_helpfulness
        elif S_helpfulness <= 0:
            S = set()
            limit = 0

        if len(S) > 0:
            move_set_normal(partitions=partitions,
                            current_partition=partition_a,
                            dest_partition=partition_b,
                            partitions_vertices=partitions_vertices,
                            to_be_moved=S,
                            weight=len(S),
                            partitions_stats=partitions_stats)
            b_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices[partition_b], partition_a,
                                                                  partitions)
            S_dash, S_dash_helpfulness, success = search_for_balancing_set(G, b_vertices_helpfulness, len(S),
                                                                           S_helpfulness, partitions, partition_a)
            if success:
                move_set_normal(partitions=partitions,
                                current_partition=partition_b,
                                dest_partition=partition_a,
                                partitions_vertices=partitions_vertices,
                                to_be_moved=S_dash,
                                weight=len(S_dash),
                                partitions_stats=partitions_stats)
                a_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices[partition_a], partition_b,
                                                                      partitions)
                limit *= 2
            else:
                move_set_normal(partitions=partitions,
                                current_partition=partition_b,
                                dest_partition=partition_a,
                                partitions_vertices=partitions_vertices,
                                to_be_moved=S,
                                weight=len(S),
                                partitions_stats=partitions_stats)
                a_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices[partition_a], partition_b,
                                                                      partitions)
                limit /= 2


def compute_areas_size(G, partitions, partition_a, partition_b):
    partition_a_weight = 0
    partition_b_weight = 0
    for v_num in G.nodes:
        if partitions.get(v_num) == partition_a:
            partition_b_weight += G.nodes[v_num]['data']['weight']
        if partitions.get(v_num) == partition_b:
            partition_a_weight += G.nodes[v_num]['data']['weight']
    return partition_a_weight, partition_b_weight


def improve_bisection_improved(G, partitions, all_vertices, partition_a, partition_b, partitions_vertices,
                               partitions_stats, bigger_dim, draw):
    partitions_vertices_c = copy.deepcopy(partitions_vertices)
    partitions_vertices_c[partition_a] = partitions_vertices_c[partition_a].intersection(all_vertices)
    partitions_vertices_c[partition_b] = partitions_vertices_c[partition_b].intersection(all_vertices)

    a_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices_c[partition_a], partition_b,
                                                          partitions)
    b_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices_c[partition_b], partition_a,
                                                          partitions)

    cut_size = count_cut_size(G, partitions, partitions_vertices_c, partition_a, partition_b)
    limit_a = cut_size / 2
    limit_b = cut_size / 2
    S_max = ((len(partitions_vertices_c[partition_a]) + len(partitions_vertices_c[partition_b])) / 2) * 0.25

    if cut_size <= 0:
        return

    while limit_a + limit_b > 1:

        if limit_a == 0 or (2 * limit_a) < limit_b:
            a_vertices_helpfulness, limit_a, partition_a, b_vertices_helpfulness, limit_b, partition_b = \
                swap_partitions(v_h_1=a_vertices_helpfulness, l_1=limit_a, p_1=partition_a,
                                v_h_2=b_vertices_helpfulness, l_2=limit_b, p_2=partition_b)

        S_a, S_a_helpfulness, S_a_weight = search_for_helpful_set_improved(G=G,
                                                                           vertices_helpfulness=a_vertices_helpfulness,
                                                                           limit=limit_a,
                                                                           s_max=S_max,
                                                                           partitions=partitions,
                                                                           adj_partition=partition_b,
                                                                           cur_partition=partition_a)

        if S_a_helpfulness < limit_a:
            limit_a = S_a_helpfulness
            if limit_b > S_a_helpfulness:

                S_b, S_b_helpfulness, S_b_weight = search_for_helpful_set_improved(G=G,
                                                                                   vertices_helpfulness=b_vertices_helpfulness,
                                                                                   limit=limit_b,
                                                                                   s_max=S_max,
                                                                                   partitions=partitions,
                                                                                   adj_partition=partition_a,
                                                                                   cur_partition=partition_b)
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

        move_set(G=G,
                 partitions=partitions,
                 current_partition=partition_a,
                 dest_partition=partition_b,
                 partitions_vertices=partitions_vertices,
                 partitions_vertices_c=partitions_vertices_c,
                 to_be_moved=S_a,
                 weight=S_a_weight,
                 partitions_stats=partitions_stats)

        b_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices_c[partition_b], partition_a,
                                                              partitions)
        min_, max_ = determine_max_and_min_weight_for_balancing_set(G, S_a_weight, partitions_vertices_c[partition_b])
        S_b, S_b_helpfulness, S_b_weight, success = search_for_balancing_set_improved(G=G,
                                                                                      vertices_helpfulness=b_vertices_helpfulness,
                                                                                      min_=min_,
                                                                                      max_=max_,
                                                                                      S_helpfulness=S_a_helpfulness,
                                                                                      adj_partition=partition_a,
                                                                                      cur_partition=partition_b,
                                                                                      partitions=partitions)

        if success and S_b_helpfulness > -S_a_helpfulness:
            move_set(G=G,
                     partitions=partitions,
                     current_partition=partition_b,
                     dest_partition=partition_a,
                     partitions_vertices=partitions_vertices,
                     partitions_vertices_c=partitions_vertices_c,
                     to_be_moved=S_b,
                     weight=S_b_weight,
                     partitions_stats=partitions_stats)
            limit_a += ceil(log(limit_a))
        else:
            move_set(G=G,
                     partitions=partitions,
                     current_partition=partition_b,
                     dest_partition=partition_a,
                     partitions_vertices=partitions_vertices,
                     partitions_vertices_c=partitions_vertices_c,
                     to_be_moved=S_a,
                     weight=S_a_weight,
                     partitions_stats=partitions_stats)
            limit_a /= 4
            limit_b /= 2

        a_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices_c[partition_a], partition_b,
                                                              partitions)
        b_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices_c[partition_b], partition_a,
                                                              partitions)

    balance_greedily(G=G, p=0.1,
                     partition_a=partition_a,
                     partition_b=partition_b,
                     partitions_vertices=partitions_vertices,
                     partitions_vertices_c=partitions_vertices_c,
                     partitions_stats=partitions_stats,
                     partitions=partitions)
    # if cut_size > 0.1 * bigger_dim:
    #     # draw(1, 50, 'before move')
    #
    #     # draw(1, 50, 'after move')
