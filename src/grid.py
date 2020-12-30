from src.grid_to_image.draw import optimized_convert_graph_to_image_2
from src.graph_utils.reduction import reduce_areas as reduce_areas_helper, reduce_vertices as reduce_vertices_helper
from src.definitions import NORMAL_AREA
from src.graph_utils.restoration import restore_area as restore_area_helper
from src.image_to_graph.conversion import convert_image_to_graph
from src.utils import get_project_root
import networkx as nx
import matplotlib.pyplot as plt


class Grid:

    def __init__(self, grid_name):
        G, areas = convert_image_to_graph(str(get_project_root()) + '/grids/' + grid_name)
        self.G = G
        self.areas = areas
        self.reductions = []

    def reduce(self, vertices_to_reduce):
        new_vertex_name = reduce_vertices_helper(self.G, vertices_to_reduce, NORMAL_AREA)
        self.reductions.append(new_vertex_name)

    def reduce_areas(self):
        new_vertices_names = reduce_areas_helper(self.G, self.areas)
        self.reductions = self.reductions + new_vertices_names

    def restore_area(self, vertex):
        restore_area_helper(self.G, vertex)

    def fully_restore(self):
        while len(self.reductions) > 0:
            self.restore_one_step()

    def restore_one_step(self):
        if len(self.reductions) > 0:
            self.restore_area(self.reductions.pop())
        else:
            print("No areas to restore")

    def draw_initial_grid(self, p, s):
        if len(self.reductions) == 0:
            optimized_convert_graph_to_image_2(self.G, self.areas, p, s)
        else:
            print("You cannot draw initial graph due to reductions")

    def draw_graph(self):
        print("drawing graph...")
        nx.draw_spectral(self.G, with_labels=True, font_weight='bold')
        plt.show()
