def restore_area(G, vertex):
    if 'replaces' in G.nodes[vertex]['data']:
        replaces = G.nodes[vertex]['data']['replaces']
        G.remove_node(vertex)
        for vertex, data in replaces.items():
            G.add_node(vertex, data=data['data'])
        for vertex, data in replaces.items():
            for adj, weight in data['adj'].items():
                G.add_edge(vertex, adj, w=weight['w'])
