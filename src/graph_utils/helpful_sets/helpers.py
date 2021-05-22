import operator

from src.definitions import INDIVISIBLE_AREA


def move_set(G, current_partition, dest_partition, partitions_vertices, to_be_moved):
    for vertex_num in to_be_moved:
        partitions_vertices[current_partition].remove(vertex_num)
        partitions_vertices[dest_partition].add(vertex_num)
        G.nodes[vertex_num]['data']['partition'] = dest_partition


def sort_vertices_helpfulness(vertices_helpfulness):
    vertices_helpfulness.sort(key=operator.itemgetter('helpfulness'))


def count_cut_size(G, partitions_vertices, partition_a_number, partition_b_number):
    partition_a_vertices = partitions_vertices[partition_a_number]
    partition_b_vertices = partitions_vertices[partition_b_number]
    if len(partition_a_vertices) > len(partition_b_vertices):
        partition_to_iterate = partition_b_vertices
        partition_number = partition_a_number
    else:
        partition_to_iterate = partition_a_vertices
        partition_number = partition_b_number

    border = set()
    for node_num in partition_to_iterate:
        for adjacent_node_num in G.adj[node_num]:
            if G.nodes[adjacent_node_num]['data']['partition'] == partition_number:
                border.add(adjacent_node_num)

    return len(border)


def get_partitions_vertices(G):
    partitions_vertices = {}
    for node_num in G.nodes:
        vertices = {node_num}
        get_partition_vertices(G.nodes[node_num]['data'], node_num, vertices)
        partitions_vertices[G.nodes[node_num]['data']['partition']] = vertices
    return partitions_vertices


def get_partition_vertices(vertices_data, vertex_num, vertices):
    vertices.add(vertex_num)
    if 'replaces' in vertices_data:
        for vertex, data in vertices_data['replaces'].items():
            get_partition_vertices(data['data'], vertex, vertices)


def get_adjacent_partitions(G):
    neighbouring_partitions = {}
    for node_num in G.nodes:
        neighbouring_partitions[G.nodes[node_num]['data']['partition']] = set()
        for adj_node in G.adj[node_num]:
            neighbouring_partitions[G.nodes[node_num]['data']['partition']].add(G.nodes[adj_node]['data']['partition'])
    return neighbouring_partitions


def create_adjacent_partitions_without_repeats(adjacent_partitions):
    new_adjacent_partitions = adjacent_partitions.copy()
    for partition, neighbours in new_adjacent_partitions.items():
        for vertex in neighbours:
            new_adjacent_partitions[vertex].remove(partition)
    return new_adjacent_partitions


def include_in_helpful_set(G, v_num, helpful_set):
    helpful_set.add(v_num)
    update_helpfulness_of_neighbours(G, v_num)


def update_helpfulness_of_neighbours(G, v_num, vertices_helpfulness):
    partition = G.nodes[v_num]['data']['partition']
    adjacent_vertices = set()
    for node_num in G.adj[v_num]:
        if G.nodes[node_num]['data']['partition'] == partition:
            adjacent_vertices.add(node_num)
    for vertex in vertices_helpfulness:
        if vertex['v_num'] in adjacent_vertices:
            vertex['helpfulness'] += 2


def count_set_helpfulness(G, helpful_set):
    helpfulness = 0
    for vertex_num in helpful_set:
        helpfulness += G.nodes[vertex_num]['data']['helpfulness']
    return helpfulness


def set_helpfulness_for_vertices(G, partition, adj_part):
    helpfulness_of_vertices = []
    for vertex in partition:
        vertex_helpfulness = count_vertex_helpfulness(G, vertex, adj_part, {})
        helpfulness_of_vertices.append({'v_num': vertex, 'helpfulness': vertex_helpfulness})

    sort_vertices_helpfulness(helpfulness_of_vertices)
    return helpfulness_of_vertices


def set_vertex_helpfulness(G, v_num, helpfulness):
    G.nodes[v_num]['data']['helpfulness'] = helpfulness


def count_adj_vertices(G, v_num, current_partition, adjacent_partition):
    counter = 0
    for v in G.adj[v_num]:
        if (G.nodes[v]['data']['partition'] == current_partition
                or G.nodes[v]['data']['partition'] == adjacent_partition):
            counter += 1
    return counter


def count_vertex_helpfulness(G, v_num, adj_part, helpful_set):
    if G.nodes[v_num]['data']['type'] == INDIVISIBLE_AREA:
        return float('-inf')
    curr_partition = G.nodes[v_num]['data']['partition']

    # print(v_ext(G, v_num, adj_part, helpful_set) - v_int(G, v_num, helpful_set) + v_int_s(G, v_num, helpful_set) - (
    #         4 - count_adj_vertices(G, v_num, curr_partition, adj_part)))
    return v_ext(G, v_num, adj_part, helpful_set) - v_int(G, v_num, helpful_set) + v_int_s(G, v_num, helpful_set)


def v_ext(G, node_num, adjacent_partition, helpful_set):
    counter = 0
    for v in G.adj[node_num]:
        if G.nodes[v]['data']['partition'] == adjacent_partition or v in helpful_set:
            counter += 1

    return counter


def v_int(G, node_num, helpful_set):
    counter = 0
    curr_vertex_partition = G.nodes[node_num]['data']['partition']
    for v in G.adj[node_num]:
        if G.nodes[v]['data']['partition'] == curr_vertex_partition and v not in helpful_set:
            counter += 1

    return counter


def v_int_s(G, node_num, helpful_set):
    counter = 0
    for v in G.adj[node_num]:
        if v in helpful_set:
            counter += 1

    return counter


def pop_vertex(vertices_helpfulness):
    vertex_data = vertices_helpfulness.pop()
    vertex_helpfulness = vertex_data['helpfulness']
    vertex_num = vertex_data['v_num']
    return vertex_num, vertex_helpfulness


def pop_vertex_improved(G, vertices_helpfulness):
    vertex_data = vertices_helpfulness.pop()
    vertex_helpfulness = vertex_data['helpfulness']
    vertex_num = vertex_data['v_num']
    vertex_weight = G.nodes[vertex_num]['data']['weight']
    return vertex_num, vertex_helpfulness, vertex_weight


def swap_partitions(v_h_1, l_1, p_1, v_h_2, l_2, p_2):
    return v_h_2, l_2, p_2, v_h_1, l_1, p_1


def undo_S_build(G, current_partition, dest_partition, partitions_vertices, vertices_set):
    if vertices_set:
        move_set(G, current_partition, dest_partition, partitions_vertices, vertices_set)
