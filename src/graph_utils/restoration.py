def restore_area(G, vertex):
    if G.nodes[vertex]['data']['replaces']:
        replaces = G.nodes[vertex]['data']['replaces']
        G.remove_node(vertex)
        for vertex, data in replaces.items():
            G.add_node(vertex, data=data['data'])
        for vertex, data in replaces.items():
            for adj in data['adj']:
                G.add_edge(vertex, adj)
