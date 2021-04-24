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


def get_neighbouring_partitions(G):
    neighbouring_partitions = {}
    for node_num in G.nodes:
        neighbouring_partitions[G.nodes[node_num]['data']['partition']] = set()
        for adj_node in G.adj[node_num]:
            neighbouring_partitions[G.nodes[node_num]['data']['partition']].add(G.nodes[adj_node]['data']['partition'])
    return neighbouring_partitions


def set_helpfulness(G, helpful_set):
    helpfulness = 0
    for vertex_num in helpful_set:
        helpfulness += vertex_helpfulness(G, vertex_num, helpful_set)
    return helpfulness


def vertex_helpfulness(G, v_num, helpful_set):
    return v_ext(G, v_num) - v_int(G, v_num) + v_int_s(G, v_num, helpful_set)


def v_ext(G, node_num):
    counter = 0
    curr_vertex_partition = G.nodes[node_num]['data']['partition']
    for v in G.adj[node_num]:
        if G.nodes[v]['data']['partition'] != curr_vertex_partition:
            counter += 1

    return counter


def v_int(G, node_num):
    counter = 0
    curr_vertex_partition = G.nodes[node_num]['data']['partition']
    for v in G.adj[node_num]:
        if G.nodes[v]['data']['partition'] == curr_vertex_partition:
            counter += 1

    return counter


def v_int_s(G, node_num, helpful_set):
    counter = 0
    curr_vertex_partition = G.nodes[node_num]['data']['partition']
    for v in G.adj[node_num]:
        if G.nodes[v]['data']['partition'] == curr_vertex_partition and v in helpful_set:
            counter += 1

    return counter
