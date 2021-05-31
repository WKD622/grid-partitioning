from src.graph_utils.helpful_sets.helpers import update_helpfulness_of_neighbours, sort_vertices_helpfulness, \
    find_vertices_adj_to_another_partition, update_adjacent_vertices, \
    update_helpfulness_of_neighbours_improved


def pop_vertex(vertices_helpfulness):
    vertex_data = vertices_helpfulness.pop()
    vertex_helpfulness = vertex_data['helpfulness']
    vertex_num = vertex_data['v_num']
    return vertex_num, vertex_helpfulness


def search_for_helpful_set(G, vertices_helpfulness, limit, partitions):
    helpful_set = set()
    set_helpfulness = 0
    end = False
    while not end and set_helpfulness < limit and len(vertices_helpfulness) > 0:
        vertex_num, vertex_helpfulness = pop_vertex(vertices_helpfulness)
        if vertex_helpfulness < 0:
            end = True
        else:
            set_helpfulness += vertex_helpfulness
            helpful_set.add(vertex_num)
            update_helpfulness_of_neighbours(G, vertex_num, vertices_helpfulness, partitions)
            sort_vertices_helpfulness(G, vertices_helpfulness)

    return helpful_set, set_helpfulness


def search_for_helpful_set_improved(G, vertices_helpfulness, limit, s_max, partitions, adj_partition, cur_partition):
    helpful_set = set()
    set_weight = 0
    set_helpfulness = 0
    end = False

    vertices_helpfulness_to_consider, adj_set = find_vertices_adj_to_another_partition(G,
                                                                                       partitions,
                                                                                       vertices_helpfulness,
                                                                                       adj_partition,
                                                                                       cur_partition)

    while not end and set_helpfulness < limit and len(vertices_helpfulness_to_consider) > 0 and len(
            helpful_set) < s_max:
        vertex_num, vertex_helpfulness = pop_vertex(vertices_helpfulness_to_consider)
        if vertex_helpfulness < 0:
            end = True
        else:
            set_helpfulness += vertex_helpfulness
            set_weight += G.nodes[vertex_num]['data']['weight']
            helpful_set.add(vertex_num)
            update_adjacent_vertices(G=G,
                                     v_num=vertex_num,
                                     partitions=partitions,
                                     vertices_helpfulness=vertices_helpfulness,
                                     vertices_helpfulness_to_consider=vertices_helpfulness_to_consider,
                                     adj_set=adj_set,
                                     helpful_set=helpful_set,
                                     cur_partition=cur_partition)
            update_helpfulness_of_neighbours_improved(G, vertex_num, vertices_helpfulness,
                                                      vertices_helpfulness_to_consider, partitions)
            sort_vertices_helpfulness(G, vertices_helpfulness_to_consider)

    return helpful_set, set_helpfulness, set_weight
