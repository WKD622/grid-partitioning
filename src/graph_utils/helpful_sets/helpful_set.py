from src.definitions import colors_for_partitions
from src.graph_utils.helpful_sets.helpers import update_helpfulness_of_neighbours, sort_vertices_helpfulness, \
    find_vertices_adj_to_another_partition, update_adjacent_vertices, \
    update_helpfulness_of_neighbours_improved
from src.grid_to_image.draw import plot, compute_fig_size


def pop_vertex(vertices_helpfulness):
    vertex_data = vertices_helpfulness.pop()
    vertex_helpfulness = vertex_data['helpfulness']
    vertex_num = vertex_data['v_num']
    return vertex_num, vertex_helpfulness


def pop_vertex_improved(vertices_helpfulness_to_consider, vertices_helpfulness):
    vertex_data = vertices_helpfulness_to_consider.pop()
    vertex_helpfulness = vertex_data['helpfulness']
    vertex_num = vertex_data['v_num']
    vertices_helpfulness.remove(vertex_data)
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


def draw_vertices(G, vertices_to_consider, color, title):
    X = []
    y = []
    colors = []

    for node in vertices_to_consider:
        X.append(G.nodes[node]['data']['x'])
        y.append(G.nodes[node]['data']['y'])
        colors.append(colors_for_partitions[color])

    plot(X, y, colors, 100, G, fig_size=(6, 6), name='name', title=title)


def draw_helpful_set(G, helpful_set, color, title):
    X = []
    y = []
    colors = []

    for node in helpful_set:
        X.append(G.nodes[node]['data']['x'])
        y.append(G.nodes[node]['data']['y'])
        colors.append(colors_for_partitions[color])
    fig_size = compute_fig_size(3, 3)
    plot(X, y, colors, 2, G, fig_size=fig_size, name='name', title=title)


def draw_helpfulness(G, vertices, title):
    colors_for_partitions = {
        4: '#FF0000',  # jasny zielony
        3: '#FF3333',  # jasny zielony
        2: '#FF6666',  # zielony
        1: '#FF9999',  # fioletowy
        0: '#FFCCCC',  # jasny niebieski
        -1: '#CCE5FF',  # bardzo jasny niebieski
        -2: '#99CCFF',  # żółty
        -3: '#66B2FF',  # pomarańczowy
        -4: '#3399FF',  # czerwony
    }
    X = []
    y = []
    colors = []

    for node in vertices:
        X.append(G.nodes[node['v_num']]['data']['x'])
        y.append(G.nodes[node['v_num']]['data']['y'])
        colors.append(colors_for_partitions[node['helpfulness']])

    plot(X, y, colors, 3, G, fig_size=(3, 3), name='name', title=title)


def search_for_helpful_set_improved(G, vertices_helpfulness, limit, s_max, partitions, adj_partition, cur_partition, draw_):
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
        # draw_helpfulness(G, vertices_helpfulness, '')
        # draw_helpfulness(G, vertices_helpfulness_to_consider, '')
        vertex_num, vertex_helpfulness = pop_vertex_improved(vertices_helpfulness_to_consider, vertices_helpfulness)
        if vertex_helpfulness < 0:
            end = True
        else:
            # draw_vertices(G, {vertex_num}, 1, '')
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
    if draw_:
        draw_helpful_set(G, helpful_set=helpful_set, color=3, title='helpfulset')
    return helpful_set, set_helpfulness, set_weight
