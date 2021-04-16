import time

import matplotlib.pyplot as plt
import networkx as nx

from src.definitions import NORMAL_AREA
from src.graph_utils.lam_algorithm import lam_algorithm, greedy_matching as greedy_matching_helper
from src.graph_utils.reduction import reduce_areas as reduce_areas_helper, reduce_vertices as reduce_vertices_helper
from src.graph_utils.restoration import restore_area as restore_area_helper
from src.grid_to_image.draw import optimized_convert_graph_to_image_2, convert_partitioned_graph_to_image
from src.image_to_graph.conversion import convert_image_to_graph
from src.utils import get_project_root


class Grid:

    def __init__(self, grid_name):
        start = time.time()
        G, areas, grid_size = convert_image_to_graph(str(get_project_root()) + '/grids/' + grid_name)
        self.conversion_time = time.time() - start
        self.grid_size = grid_size
        self.G = G
        self.areas = areas
        self.reductions = []
        self.drawing_initial_grid_time = None
        self.full_restoration_time = None
        self.areas_reduction_time = None
        self.drawing_graph_time = None
        self.drawing_partitioned_grid_time = None
        self.last_number_of_partitions = len(G.nodes)

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

    def draw_initial_grid(self, p, s, name='initial'):
        if len(self.reductions) == 0:
            print("drawing initial grid started...")
            start = time.time()
            optimized_convert_graph_to_image_2(self.G, self.areas, p, s, name)
            self.drawing_initial_grid_time = time.time() - start
        else:
            print("You cannot draw initial graph due to reductions")

    def draw_partitioned_grid(self, p, s, name):
        print("drawing partitioned grid started...")
        start = time.time()
        convert_partitioned_graph_to_image(self.G, p, s, self.last_number_of_partitions, name)
        self.drawing_partitioned_grid_time = time.time() - start

    def draw_graph(self):
        print("drawing graph started...")
        start = time.time()
        nx.draw(self.G, with_labels=True, font_weight='bold')
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
        if self.drawing_partitioned_grid_time:
            print('drawing partitioned grid: ' + str(round(self.drawing_partitioned_grid_time, 6)) + ' s')
        print('---------------------------------------')

    def reduce_by_lam(self, number_of_parts):
        print('lam reduction stared (number of nodes: ' + str(self.G.number_of_nodes()) + ")...")
        i = 1
        while self.G.number_of_nodes() > number_of_parts:
            start = time.time()
            for match in lam_algorithm(self.G, number_of_parts):
                self.reduce(match)
                self.last_number_of_partitions = self.G.number_of_nodes()
            print(str(i) + ') reduce: (time: ' + str(round(time.time() - start, 2)) + " s, number of nodes: " + str(
                self.G.number_of_nodes()) + ")")
            i += 1
        print('lam reduction finished')

    def test_dividing(self, number_of_parts):

        def divide(G):
            partition_number = 0
            for node in G:
                G.nodes[node]['data']['partition'] = partition_number
                partition_number += 1
            return partition_number

        def fully_restore(G, reductions):
            while len(reductions) > 0:
                restore_area_helper(G, reductions.pop())

        while self.G.number_of_nodes() > number_of_parts:
            for match in lam_algorithm(self.G, number_of_parts):
                self.reduce(match)
                c_G = self.G.copy()
                partitions_number = divide(c_G)
                if partitions_number < 20:
                    c_reductions = self.reductions.copy()
                    c_G = self.G.copy()
                    divide(c_G)
                    fully_restore(c_G, c_reductions)
                    convert_partitioned_graph_to_image(c_G, 1, 40)

    def divide(self):
        partition_number = 0
        for node in self.G.nodes:
            self.G.nodes[node]['data']['partition'] = partition_number
            partition_number += 1

    def get_highest_degree(self):
        degrees = sorted(d for n, d in self.G.degree())
        return degrees[-1]

    def get_smallest_degree(self):
        degrees = sorted(d for n, d in self.G.degree())
        return degrees[0]

    def get_edge_with_smallest_weight(self):
        return sorted(self.G.edges.data('w'), key=lambda x: x[2])[0]

    def get_edge_with_highest_weight(self):
        return sorted(self.G.edges.data('w'), key=lambda x: x[2])[len(self.G.edges) - 1]

    def greedy_matching(self):
        start = time.time()
        greedy_matching_helper(self)
        print('greedy matching time: ' + str(round(time.time() - start, 6)) + ' s')
