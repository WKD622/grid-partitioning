from src.graph_utils.helpful_sets.helpers import update_helpfulness_of_neighbours, sort_vertices_helpfulness, pop_vertex


def search_for_helpful_set(G, vertices_helpfulness, limit):
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
            update_helpfulness_of_neighbours(G, vertex_num, vertices_helpfulness)
            sort_vertices_helpfulness(vertices_helpfulness)

    return helpful_set, set_helpfulness


