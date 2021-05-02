from src.graph_utils.helpful_sets.balancing_set import search_for_balancing_set
from src.graph_utils.helpful_sets.helpers import set_helpfulness_for_vertices, count_cut_size, \
    move_set_to_another_partition
from src.graph_utils.helpful_sets.helpful_set import search_for_helpful_set


def improve_bisection(G, partition_a, partition_b, partitions_vertices, draw):
    a_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices[partition_a], partition_b)
    a_vertices_helpfulness_copy = a_vertices_helpfulness.copy()
    cut_size = count_cut_size(G, partitions_vertices, partition_a, partition_b)
    limit = cut_size / 4

    while limit > 0:
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
                a_vertices_helpfulness = a_vertices_helpfulness_copy
                limit /= 2
