from src.graph_utils.helpful_sets.helpers import set_helpfulness_for_vertices, pop_vertex, \
    update_helpfulness_of_neighbours, sort_vertices_helpfulness, move_set


def balance_greedily(G, p, partition_a, partition_b, partitions_vertices, partitions_stats):
    a_partition_size = partitions_stats[partition_a]
    b_partition_size = partitions_stats[partition_b]
    partition_weight_diff = abs(a_partition_size - b_partition_size)
    weight_to_balance = p * partition_weight_diff
    if a_partition_size > b_partition_size:
        a_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices[partition_a], partition_b)
        vertices, vertices_weight = find_vertices_to_balance(G,
                                                             vertices_helpfulness=a_vertices_helpfulness,
                                                             weight_to_balance=weight_to_balance)
        move_set(G=G,
                 current_partition=partition_a,
                 dest_partition=partition_b,
                 partitions_vertices=partitions_vertices,
                 to_be_moved=vertices,
                 weight=vertices_weight,
                 partitions_stats=partitions_stats)
    else:
        b_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices[partition_b], partition_a)
        vertices, vertices_weight = find_vertices_to_balance(G,
                                                             vertices_helpfulness=b_vertices_helpfulness,
                                                             weight_to_balance=weight_to_balance)
        move_set(G=G,
                 current_partition=partition_b,
                 dest_partition=partition_a,
                 partitions_vertices=partitions_vertices,
                 to_be_moved=vertices,
                 weight=vertices_weight,
                 partitions_stats=partitions_stats)


def find_vertices_to_balance(G, weight_to_balance, vertices_helpfulness):
    vertices_to_balance = set()
    checked_vertices = set()
    i = 3
    set_weight = 0
    start = True

    while (len(checked_vertices) or start) and i > 0 and set_weight < weight_to_balance:
        start = False
        end = False
        checked_vertices = set()
        while not end and len(vertices_helpfulness) > 0 and set_weight < weight_to_balance:
            vertex_num, vertex_helpfulness = pop_vertex(vertices_helpfulness)
            vertex_weight = G.nodes[vertex_num]['data']['weight']
            if set_weight + vertex_weight > weight_to_balance:
                end = True
                checked_vertices.add(vertex_num)
            else:
                set_weight += G.nodes[vertex_num]['data']['weight']
                vertices_to_balance.add(vertex_num)
                update_helpfulness_of_neighbours(G, vertex_num, vertices_helpfulness)
                sort_vertices_helpfulness(vertices_helpfulness)

    return vertices_to_balance, set_weight
