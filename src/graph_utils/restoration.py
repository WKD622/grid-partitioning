def restore_area(G, vertex):
    if G.nodes[vertex]['data']['replaces']:
        replaces = G.nodes[vertex]['data']['replaces']
        partition_number = G.nodes[vertex]['data']['partition']
        G.remove_node(vertex)
        for vertex, data in replaces.items():
            data['data']['partition'] = partition_number
            G.add_node(vertex, data=data['data'])
        for vertex, data in replaces.items():
            for adj, weight in data['adj'].items():
                G.add_edge(vertex, adj, w=weight['w'])
