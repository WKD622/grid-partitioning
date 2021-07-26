from src.graph_utils.helpful_sets.helpers import set_helpfulness_for_vertices, pop_vertex, \
    update_helpfulness_of_neighbours, sort_vertices_helpfulness, move_set, find_vertices_adj_to_another_partition, \
    update_adjacent_vertices, move_set_normal


def balance_greedily_weighted(G, p, partition_a, partition_b, partitions_vertices, partitions_vertices_c,
                              partitions_stats,
                              partitions):
    a_partition_size = partitions_stats[partition_a]
    b_partition_size = partitions_stats[partition_b]
    partition_weight_diff = abs(a_partition_size - b_partition_size)
    weight_to_balance = p * partition_weight_diff
    if a_partition_size > b_partition_size:
        cur_partition = partition_a
        dest_partition = partition_b
        a_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices_c[partition_a], partition_b,
                                                              partitions, sq=False)
        vertices, vertices_weight = find_vertices_to_balance_weighted(G,
                                                                      vertices_helpfulness=a_vertices_helpfulness,
                                                                      weight_to_balance=weight_to_balance,
                                                                      partitions=partitions,
                                                                      adj_partition=dest_partition,
                                                                      cur_partition=cur_partition)
    else:
        cur_partition = partition_b
        dest_partition = partition_a
        b_vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices_c[partition_b], partition_a,
                                                              partitions, sq=False)
        vertices, vertices_weight = find_vertices_to_balance_weighted(G,
                                                                      vertices_helpfulness=b_vertices_helpfulness,
                                                                      weight_to_balance=weight_to_balance,
                                                                      partitions=partitions,
                                                                      adj_partition=dest_partition,
                                                                      cur_partition=cur_partition)
    move_set(G=G,
             partitions=partitions,
             current_partition=cur_partition,
             dest_partition=dest_partition,
             partitions_vertices=partitions_vertices,
             to_be_moved=vertices,
             weight=vertices_weight,
             partitions_stats=partitions_stats,
             partitions_vertices_c=partitions_vertices_c)


def balance_greedily_normal(G, p, partition_a, partition_b, partitions_vertices,
                            partitions_stats,
                            partitions):
    a_partition_size = partitions_stats[partition_a]
    b_partition_size = partitions_stats[partition_b]
    partition_sizes_diff = abs(a_partition_size - b_partition_size)
    size_to_balance = p * partition_sizes_diff
    if a_partition_size > b_partition_size:
        cur_partition = partition_a
        dest_partition = partition_b
        vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices[partition_a], partition_b,
                                                            partitions, sq=True)
    else:
        cur_partition = partition_b
        dest_partition = partition_a
        vertices_helpfulness = set_helpfulness_for_vertices(G, partitions_vertices[partition_b], partition_a,
                                                            partitions, sq=True)

    vertices, set_size = find_vertices_to_balance_normal(G,
                                                         vertices_helpfulness=vertices_helpfulness,
                                                         size_to_balance=size_to_balance,
                                                         partitions=partitions,
                                                         adj_partition=dest_partition,
                                                         cur_partition=cur_partition)

    move_set_normal(partitions=partitions,
                    current_partition=cur_partition,
                    dest_partition=dest_partition,
                    partitions_vertices=partitions_vertices,
                    to_be_moved=vertices,
                    weight=set_size,
                    partitions_stats=partitions_stats)


def find_vertices_to_balance_weighted(G, weight_to_balance, vertices_helpfulness, partitions, adj_partition,
                                      cur_partition):
    vertices_helpfulness_to_consider, adj_set = find_vertices_adj_to_another_partition(G,
                                                                                       partitions,
                                                                                       vertices_helpfulness,
                                                                                       adj_partition,
                                                                                       cur_partition)

    vertices_to_balance = set()

    set_weight = 0
    end = False

    while not end and len(vertices_helpfulness_to_consider) > 0 and set_weight < weight_to_balance:
        vertex_num, vertex_helpfulness = pop_vertex(vertices_helpfulness_to_consider)
        vertex_weight = G.nodes[vertex_num]['data']['weight']
        if set_weight + vertex_weight > weight_to_balance:
            end = True
        else:
            set_weight += G.nodes[vertex_num]['data']['weight']
            vertices_to_balance.add(vertex_num)
            update_adjacent_vertices(G=G,
                                     v_num=vertex_num,
                                     partitions=partitions,
                                     vertices_helpfulness=vertices_helpfulness,
                                     vertices_helpfulness_to_consider=vertices_helpfulness_to_consider,
                                     adj_set=adj_set,
                                     helpful_set=vertices_to_balance,
                                     cur_partition=cur_partition)
            update_helpfulness_of_neighbours(G, vertex_num, vertices_helpfulness_to_consider, partitions)
            sort_vertices_helpfulness(G, vertices_helpfulness_to_consider)

    return vertices_to_balance, set_weight


def find_vertices_to_balance_normal(G, size_to_balance, vertices_helpfulness, partitions, adj_partition, cur_partition):
    vertices_helpfulness_to_consider, adj_set = find_vertices_adj_to_another_partition(G,
                                                                                       partitions,
                                                                                       vertices_helpfulness,
                                                                                       adj_partition,
                                                                                       cur_partition)

    vertices_to_balance = set()

    set_size = 0
    end = False

    while not end and len(vertices_helpfulness_to_consider) > 0 and set_size < size_to_balance:
        vertex_num, vertex_helpfulness = pop_vertex(vertices_helpfulness_to_consider)
        if set_size + 1 > size_to_balance:
            end = True
        else:
            set_size += 1
            vertices_to_balance.add(vertex_num)
            update_adjacent_vertices(G=G,
                                     v_num=vertex_num,
                                     partitions=partitions,
                                     vertices_helpfulness=vertices_helpfulness,
                                     vertices_helpfulness_to_consider=vertices_helpfulness_to_consider,
                                     adj_set=adj_set,
                                     helpful_set=vertices_to_balance,
                                     cur_partition=cur_partition)
            update_helpfulness_of_neighbours(G, vertex_num, vertices_helpfulness_to_consider, partitions)
            sort_vertices_helpfulness(G, vertices_helpfulness_to_consider)

    return vertices_to_balance, set_size
