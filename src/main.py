import networkx as nx

from src.definitions import NORMAL_AREA
from src.graph_utils.reduction import reduce_vertices
from src.grid import Grid
import time

# grid = Grid('grid.png')

G = nx.Graph()
G.add_node(1, data={"lvl": 0})
G.add_node(2, data={"lvl": 0})
G.add_node(3, data={"lvl": 0})
G.add_node(4, data={"lvl": 0})
G.add_edge(1, 2, w=1)
G.add_edge(2, 1, w=1)
G.add_edge(2, 3, w=1)
G.add_edge(2, 3, w=1)
G.add_edge(3, 1, w=1)
G.add_edge(1, 4, w=1)
G.add_edge(4, 1, w=1)
print(G.nodes)
print(G.edges)
print(G.adj[1])
print(G.adj[2])

reduce_vertices(G, {2, 3, 4}, NORMAL_AREA)

print(G.nodes)
print(G.edges)
print(G.adj[1])
print(G.nodes[2])