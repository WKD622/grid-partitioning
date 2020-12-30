from src.graph_utils.lam_algorithm import lam_algorithm
from src.grid import Grid

grid = Grid('grid4.png')

# grid.reduce_areas()

lam_algorithm(grid.G)

# grid.fully_restore()
#
# grid.print_execution_times()






















# grid.draw_initial_grid(0.01, 3)

# G = nx.Graph()
# G.add_node(1, data={"lvl": 0})
# G.add_node(2, data={"lvl": 0})
# G.add_node(3, data={"lvl": 0})
# G.add_node(4, data={"lvl": 0})
# G.add_node(5, data={"lvl": 0})
# G.add_edge(1, 2, w=1)
# G.add_edge(2, 1, w=1)
# G.add_edge(3, 1, w=1)
# G.add_edge(1, 3, w=1)
# G.add_edge(1, 4, w=1)
# G.add_edge(4, 1, w=1)
#
# G.add_edge(5, 2, w=1)
# G.add_edge(2, 5, w=1)
# G.add_edge(3, 5, w=1)
# G.add_edge(5, 3, w=1)
# G.add_edge(5, 4, w=1)
# G.add_edge(4, 5, w=1)
#
# G.add_edge(2, 3, w=1)
# G.add_edge(3, 2, w=1)
#
# print(G.nodes)
# print(G.edges)
#
# reduce_vertices(G, {2, 3, 4}, NORMAL_AREA)
#
# print(G.nodes)
# print(G.edges)
#
# restore_area(G, 2)
#
# print(G.nodes)
# print(G.edges)
