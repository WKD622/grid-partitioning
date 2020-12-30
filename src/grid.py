import time

import matplotlib.pyplot as plt
import networkx as nx

from src.definitions import NORMAL_AREA
from src.graph_utils.reduction import reduce_areas as reduce_areas_helper, reduce_vertices as reduce_vertices_helper
from src.graph_utils.restoration import restore_area as restore_area_helper
from src.grid_to_image.draw import optimized_convert_graph_to_image_2
from src.image_to_graph.conversion import convert_image_to_graph
from src.utils import get_project_root


class Grid:

    def __init__(self, grid_name):
        start = time.time()
        G, areas = convert_image_to_graph(str(get_project_root()) + '/grids/' + grid_name)
        self.conversion_time = time.time() - start
        self.G = G
        self.areas = areas
        self.reductions = []
        self.drawing_initial_grid_time = None
        self.full_restoration_time = None
        self.areas_reduction_time = None
        self.drawing_graph_time = None

    def reduce(self, vertices_to_reduce):
        new_vertex_name = reduce_vertices_helper(self.G, vertices_to_reduce, NORMAL_AREA)
        self.reductions.append(new_vertex_name)

    def reduce_areas(self):
        print('reducing areas started...')
        start = time.time()
        new_vertices_names = reduce_areas_helper(self.G, self.areas)
        self.reductions = self.reductions + new_vertices_names
        self.areas_reduction_time = time.time() - start
        print('reducing areas finished')

    def restore_area(self, vertex):
        restore_area_helper(self.G, vertex)

    def fully_restore(self):
        print('full restoration started')
        start = time.time()
        while len(self.reductions) > 0:
            self.restore_one_step()
        self.full_restoration_time = time.time() - start
        print('full restoration finished')

    def restore_one_step(self):
        if len(self.reductions) > 0:
            self.restore_area(self.reductions.pop())
        else:
            print("No areas to restore")

    def draw_initial_grid(self, p, s):
        if len(self.reductions) == 0:
            print("drawing initial grid started...")
            start = time.time()
            optimized_convert_graph_to_image_2(self.G, self.areas, p, s)
            self.drawing_initial_grid_time = time.time() - start
        else:
            print("You cannot draw initial graph due to reductions")

    def draw_graph(self):
        print("drawing graph started...")
        start = time.time()
        nx.draw_spectral(self.G, with_labels=True, font_weight='bold')
        self.drawing_graph_time = time.time() - start
        plt.show()

    def print_execution_times(self):
        print('\n----------- EXECUTION TIMES -----------')
        if self.conversion_time:
            print('conversion ' + str(round(self.conversion_time, 6)) + ' s')
        if self.areas_reduction_time:
            print('areas reduction: ' + str(round(self.areas_reduction_time, 6)) + ' s')
        if self.full_restoration_time:
            print('full restoration time: ' + str(round(self.full_restoration_time, 6)) + ' s')
        if self.drawing_initial_grid_time:
            print('drawing initial grid: ' + str(round(self.drawing_initial_grid_time, 2)) + ' s')
        if self.drawing_graph_time:
            print('drawing graph: ' + str(round(self.drawing_graph_time, 6)) + ' s')
        print('---------------------------------------')
