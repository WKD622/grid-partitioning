import copy

from src.definitions import INDIVISIBLE_AREA


def update_partitions_stats(current_partition, dest_partition, to_be_moved_weight, partitions_stats):
    partitions_stats[dest_partition] += to_be_moved_weight
    partitions_stats[current_partition] -= to_be_moved_weight
    # if partitions_stats[current_partition] < 0:
    #     print('ERROR')
    #     sleep(100)


def get_offspring_vertices(G, vertex_num):
    offspring = set()
    vertex_data = G.nodes[vertex_num]['data']
    look_for_offspring(vertex_data, offspring)
    return offspring


def look_for_offspring(vertex_data, offspring):
    if 'replaces' in vertex_data:
        for vertex, data in vertex_data['replaces'].items():
            offspring.add(vertex)
            if data['data']:
                look_for_offspring(data['data'], offspring)
    else:
        offspring.add(vertex_data['num'])


def count_sum_weight(G, partition_n, partitions_vertices):
    weight = 0
    for v in partitions_vertices[partition_n]:
        print(v, G.nodes[v]['data']['weight'])
        weight += G.nodes[v]['data']['weight']


def move_set_normal(partitions, current_partition, dest_partition, partitions_vertices, to_be_moved,
                    weight, partitions_stats):
    for vertex_num in to_be_moved:
        partitions_vertices[current_partition].remove(vertex_num)
        partitions_vertices[dest_partition].add(vertex_num)
        partitions[vertex_num] = dest_partition
    update_partitions_stats(current_partition, dest_partition, weight, partitions_stats)


def move_set(G, partitions, current_partition, dest_partition, partitions_vertices_c, partitions_vertices, to_be_moved,
             weight, partitions_stats):
    for vertex_num in to_be_moved:
        offspring = get_offspring_vertices(G, vertex_num)
        offspring.add(vertex_num)
        partitions_vertices_c[current_partition].remove(vertex_num)
        partitions_vertices_c[dest_partition].add(vertex_num)
        for v in offspring:
            partitions_vertices[current_partition].remove(v)
            partitions_vertices[dest_partition].add(v)
            partitions[v] = dest_partition

    update_partitions_stats(current_partition, dest_partition, weight, partitions_stats)


def sort_vertices_helpfulness(G, vertices_helpfulness):
    vertices_helpfulness.sort(key=lambda x: (x['helpfulness'], G.nodes[x['v_num']]['data']['weight']))


def count_cut_size(G, partitions, partitions_vertices, partition_a_number, partition_b_number):
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
            if partitions[adjacent_node_num] == partition_number:
                border.add(adjacent_node_num)

    return len(border)


def get_partitions_vertices(G, partitions):
    partitions_vertices = {}
    for node_num in G.nodes:
        vertices = {node_num}
        get_partition_vertices(G.nodes[node_num]['data'], node_num, vertices, partitions[node_num], partitions)
        partitions_vertices[partitions[node_num]] = vertices
    return partitions_vertices


def get_partition_vertices(vertices_data, vertex_num, vertices, father_partition, partitions):
    vertices.add(vertex_num)
    if 'replaces' in vertices_data:
        for vertex, data in vertices_data['replaces'].items():
            partitions[vertex] = father_partition
            get_partition_vertices(data['data'], vertex, vertices, father_partition, partitions)


def get_adjacent_partitions(G, partitions):
    neighbouring_partitions = {}
    for node_num in G.nodes:
        neighbouring_partitions[partitions[node_num]] = set()
        for adj_node in G.adj[node_num]:
            neighbouring_partitions[partitions[node_num]].add(partitions[adj_node])
    return neighbouring_partitions


def create_adjacent_partitions_without_repeats(adjacent_partitions):
    new_adjacent_partitions = copy.deepcopy(adjacent_partitions)
    for partition, neighbours in new_adjacent_partitions.items():
        for vertex in neighbours:
            new_adjacent_partitions[vertex].remove(partition)
    return new_adjacent_partitions


def include_in_helpful_set(G, v_num, helpful_set):
    helpful_set.add(v_num)
    update_helpfulness_of_neighbours(G, v_num)


def update_helpfulness_of_neighbours(G, v_num, vertices_helpfulness, partitions):
    partition = partitions[v_num]
    adjacent_vertices = set()
    for node_num in G.adj[v_num]:
        if partitions[node_num] == partition:
            adjacent_vertices.add(node_num)
    for vertex in vertices_helpfulness:
        if vertex['v_num'] in adjacent_vertices:
            vertex['helpfulness'] += 2


def update_helpfulness_of_neighbours_improved(G, v_num, vertices_helpfulness, vertices_helpfulness_to_consider,
                                              partitions):
    partition = partitions[v_num]
    adjacent_vertices = set()
    for node_num in G.adj[v_num]:
        if partitions[node_num] == partition:
            adjacent_vertices.add(node_num)
    for vertex in vertices_helpfulness:
        if vertex['v_num'] in adjacent_vertices:
            vertex['helpfulness'] += 2
    for vertex in vertices_helpfulness_to_consider:
        if vertex['v_num'] in adjacent_vertices:
            vertex['helpfulness'] += 2


def check_if_can_be_added(G, vertex, partitions, partition, cur_partition):
    def adjacent_to_other_partition():
        for v_ in G.adj[vertex]:
            if partitions[v_] != partition and partitions[v_] != cur_partition:
                return True
        return False

    for v in G.adj[vertex]:
        if partitions[v] == partition:
            return True
    return False


def find_vertices_adj_to_another_partition(G, partitions, vertices_helpfulness, adj_partition, cur_partition):
    vertices_to_check = list(filter(lambda x: x['helpfulness'] >= -2, vertices_helpfulness))
    result = []
    result_set = set()
    for vertex in vertices_to_check:
        if check_if_can_be_added(G, vertex['v_num'], partitions, adj_partition, cur_partition):
            result.append(vertex)
            result_set.add(vertex['v_num'])
    return result, result_set


def update_adjacent_vertices(G, v_num, partitions, vertices_helpfulness, vertices_helpfulness_to_consider, adj_set,
                             cur_partition, helpful_set):
    adj_set.remove(v_num)
    to_add = set()
    for v in G.adj[v_num]:
        if v not in adj_set and v not in helpful_set and partitions[v] == cur_partition:
            adj_set.add(v)
            to_add.add(v)
    for v in vertices_helpfulness:
        if v['v_num'] in to_add:
            vertices_helpfulness_to_consider.append(v)


def count_set_helpfulness(G, helpful_set):
    helpfulness = 0
    for vertex_num in helpful_set:
        helpfulness += G.nodes[vertex_num]['data']['helpfulness']
    return helpfulness


def set_helpfulness_for_vertices(G, partition, adj_part, partitions, sq=True):
    helpfulness_of_vertices = []
    for vertex in partition.intersection(set(G.nodes)):
        vertex_helpfulness = count_vertex_helpfulness(G, vertex, adj_part, {}, partitions, sq)
        helpfulness_of_vertices.append({'v_num': vertex, 'helpfulness': vertex_helpfulness})

    sort_vertices_helpfulness(G, helpfulness_of_vertices)
    return helpfulness_of_vertices


def set_vertex_helpfulness(G, v_num, helpfulness):
    G.nodes[v_num]['data']['helpfulness'] = helpfulness


def count_adj_vertices(G, partitions, v_num, current_partition, adjacent_partition):
    counter = 0
    for v in G.adj[v_num]:
        if (partitions[v] == current_partition
                or partitions[v] == adjacent_partition):
            counter += 1
    return counter


def count_vertex_helpfulness(G, v_num, adj_part, helpful_set, partitions, sq=True):
    if G.nodes[v_num]['data']['type'] == INDIVISIBLE_AREA:
        return float('-inf')

    a = 0
    if not sq:
        curr_partition = partitions[v_num]
        a = (4 - count_adj_vertices(G, partitions, v_num, curr_partition, adj_part))
    return (v_ext(G, v_num, adj_part, helpful_set, partitions)
            - v_int(G, v_num, helpful_set, partitions)
            + v_int_s(G, v_num, helpful_set)
            - a)


def v_ext(G, node_num, adjacent_partition, helpful_set, partitions):
    counter = 0
    for v in G.adj[node_num]:
        if partitions[v] == adjacent_partition or v in helpful_set:
            counter += 1

    return counter


def v_int(G, node_num, helpful_set, partitions):
    counter = 0
    curr_vertex_partition = partitions[node_num]
    for v in G.adj[node_num]:
        if partitions[v] == curr_vertex_partition and v not in helpful_set:
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
