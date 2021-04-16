from src.definitions import OFF_AREA


def remove_vertices(G, vertices_to_remove):
    for vertex in vertices_to_remove:
        G.remove_node(vertex)


def get_replaces_map(G, vertices):
    adj = set()
    replaces = {}
    count = 0

    for v in vertices:
        node_data = G.nodes[v]
        v_adj = dict(G[v])
        node_data['adj'] = v_adj
        replaces[v] = node_data
        adj = adj | set(v_adj)
        count += node_data['data']['count']

    adj = adj - vertices
    adj_with_edges_weights = set()

    for v in adj:
        v_adj = set(G.adj[v].keys())
        r_adj = vertices & v_adj
        new_edge_weight = 0
        for v_r in r_adj:
            new_edge_weight += G[v][v_r]['w']
        adj_with_edges_weights.add((v, new_edge_weight))

    return replaces, adj, adj_with_edges_weights, count


def get_partition_lvl(G, adj):
    max_lvl = 0
    for v in adj:
        node_lvl = G.nodes[v]['data']['lvl']
        if node_lvl > max_lvl:
            max_lvl = node_lvl
    return max_lvl + 1


def add_edges(G, vertex, vertices):
    for v in vertices:
        v_num, edge_weight = v
        G.add_edge(vertex, v_num, w=edge_weight)
        G.add_edge(v_num, vertex, w=edge_weight)


def reduce_vertices(G, vertices_to_reduce, new_node_type):
    new_node_data = {}
    new_node_name = next(iter(vertices_to_reduce))
    replaces, adj, adj_with_edges_weights, count = get_replaces_map(G, vertices_to_reduce)
    remove_vertices(G, vertices_to_reduce)
    new_node_data['replaces'] = replaces
    new_node_data['type'] = new_node_type
    if new_node_type == OFF_AREA:
        count = 0
    new_node_data['count'] = count
    new_node_data['lvl'] = get_partition_lvl(G, adj)
    G.add_node(new_node_name, data=new_node_data)
    add_edges(G, new_node_name, adj_with_edges_weights)
    return new_node_name


def reduce_areas(G, areas):
    history = []
    for area_type in areas:
        for vertices in areas[area_type].values():
            history.append(reduce_vertices(G, set(vertices), area_type))
    return history
