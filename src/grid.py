import time
from math import floor

import matplotlib.pyplot as plt
import networkx as nx

from src.definitions import NORMAL_AREA
from src.graph_utils.helpful_sets.algorithm import improve_bisection, improve_bisection_improved
from src.graph_utils.helpful_sets.helpers import (get_partitions_vertices, get_adjacent_partitions,
                                                  create_adjacent_partitions_without_repeats)
from src.graph_utils.lam_algorithm import lam_algorithm, greedy_matching as greedy_matching_helper
from src.graph_utils.reduction import reduce_areas as reduce_areas_helper, reduce_vertices as reduce_vertices_helper
from src.graph_utils.restoration import restore_area as restore_area_helper
from src.grid_to_image.draw import optimized_convert_graph_to_image_2, convert_partitioned_graph_to_image
from src.image_to_graph.conversion import convert_image_to_graph
from src.parse_partitioning.parse_partitioning import parse_partitioning
from src.utils import get_project_root, print_infos


class Grid:

    def __init__(self, grid_name, show_progress=True):
        self.show_progress = show_progress
        if grid_name:
            start = time.time()
            G, areas, grid_size, dim_1, dim_2 = convert_image_to_graph(str(get_project_root()) + '/grids/' + grid_name,
                                                                       self.show_progress)
            self.conversion_time = time.time() - start
            self.grid_size = grid_size
            self.G = G
            self.areas = areas
            self.last_number_of_partitions = G.number_of_nodes()
        self.dim_1 = dim_1
        self.dim_2 = dim_2
        self.bigger_dim = dim_1 if dim_1 > dim_2 else dim_2
        self.reductions = []
        self.drawing_initial_grid_time = None
        self.full_restoration_time = None
        self.lam_reduction_time = None
        self.areas_reduction_time = None
        self.drawing_graph_time = None
        self.drawing_partitioned_grid_time = None
        self.partitions_stats = {}
        self.partitions_vertices = None
        self.adjacent_partitions = None
        self.partitions = {}

    def parse_ready_partitioning(self, partitioning_name):
        G, grid_size, partitions_vertices = parse_partitioning(
            str(get_project_root()) + '/partitionings/' + partitioning_name)
        self.G = G
        self.last_number_of_partitions = 2
        self.adjacent_partitions = {1: [2], 2: [1]}
        self.partitions_vertices = partitions_vertices

    def reduce(self, vertices_to_reduce):
        new_vertex_name = reduce_vertices_helper(self.G, vertices_to_reduce, NORMAL_AREA)
        self.reductions.append(new_vertex_name)

    @print_infos
    def reduce_areas(self):
        start = time.time()
        new_vertices_names = reduce_areas_helper(self.G, self.areas)
        self.reductions = self.reductions + new_vertices_names
        self.areas_reduction_time = time.time() - start

    def restore_area(self, vertex):
        restore_area_helper(self.G, vertex)

    @print_infos
    def fully_restore(self):
        start = time.time()
        while len(self.reductions) > 0:
            self.restore_one_step()
        self.full_restoration_time = time.time() - start

    @print_infos
    def fully_restore_with_partitions_improvement(self):
        start = time.time()
        number_of_reductions_done = 0
        init_red_length = len(self.reductions)
        while len(self.reductions) > 0:
            if (number_of_reductions_done / init_red_length > 0.7
                    and floor(len(self.reductions) % (init_red_length * 0.05)) == 0):
                self.improve_partitioning_improved()
            self.restore_one_step()
            number_of_reductions_done += 1
        self.improve_partitioning_normal()
        self.full_restoration_time = time.time() - start

    @print_infos
    def draw_one_step_of_restoration(self, p, s, title=''):
        G = self.G.copy()
        reductions = self.reductions.copy()
        while len(reductions) > 0:
            restore_area_helper(G, reductions.pop())
        convert_partitioned_graph_to_image(G, p, s, self.last_number_of_partitions, self.partitions, 'name', save=False,
                                           title=title)

    def restore_one_step(self):
        if len(self.reductions) > 0:
            self.restore_area(self.reductions.pop())
        else:
            print("No areas to restore")

    @print_infos
    def draw_initial_grid(self, p, s, name='initial'):
        if len(self.reductions) == 0:
            start = time.time()
            optimized_convert_graph_to_image_2(self.G, self.areas, p, s, name)
            self.drawing_initial_grid_time = time.time() - start
        else:
            print("You cannot draw initial graph due to reductions")

    @print_infos
    def draw_partitioned_grid(self, p, s, name='output', save=False):
        start = time.time()
        convert_partitioned_graph_to_image(self.G, p, s, self.last_number_of_partitions, self.partitions, name, save)
        self.drawing_partitioned_grid_time = time.time() - start

    @print_infos
    def draw_graph(self):
        start = time.time()
        nx.draw(self.G, with_labels=True, font_weight='bold')
        self.drawing_graph_time = time.time() - start
        plt.show()

    def calculate_maximal_number_of_episodes(self, number_of_partitions):
        i = 0
        graph_size = self.G.number_of_nodes()
        while graph_size / 2 > number_of_partitions:
            i += 1
            graph_size = graph_size / 2
        return i

    @print_infos
    def draw_partitioning_step(self, p, s, title='', save=False, name='name'):
        partition_number = 0
        G_copy = self.G.copy()

        for node in G_copy.nodes:
            G_copy.nodes[node]['data']['partition'] = partition_number
            partition_number += 1

        last_number_of_partitions = 2

        reductions_copy = self.reductions.copy()
        while len(reductions_copy) > 0:
            if len(reductions_copy) > 0:
                restore_area_helper(G_copy, reductions_copy.pop())

        convert_partitioned_graph_to_image(G_copy, p, s, last_number_of_partitions, self.partitions, name=name,
                                           save=save,
                                           title=title)

    @print_infos
    def reduce_by_lam(self, number_of_partitions, draw_steps=False):
        general_start = time.time()
        i = 1
        T = self.calculate_maximal_number_of_episodes(number_of_partitions)
        while self.G.number_of_nodes() > number_of_partitions:
            start = time.time()
            for match in lam_algorithm(self.G, number_of_partitions, T, i, self.grid_size, self.show_progress):
                self.reduce(match)
                self.last_number_of_partitions = self.G.number_of_nodes()
            if draw_steps:
                self.draw_partitioning_step()

            if self.show_progress:
                print('{}) reduce: {:<3} s | nodes: {}'.format(i, round(time.time() - start, 2),
                                                               self.G.number_of_nodes()))
            i += 1
        self.lam_reduction_time = time.time() - general_start

    def add_to_partitions_stats(self, partition_number, partition_weight):
        self.partitions_stats[partition_number] = partition_weight

    def partition(self):
        partition_number = 0
        for node in self.G.nodes:
            self.partitions[node] = partition_number
            partition_number += 1

        self.fill_stats()
        self.set_adjacent_partitions()
        self.set_partitions_and_partitions_vertices()

    def fill_stats(self):
        partition_number = 0
        for node in self.G.nodes:
            self.add_to_partitions_stats(partition_number,
                                         self.G.nodes[node]['data']['weight'])
            partition_number += 1

    def set_adjacent_partitions(self):
        self.adjacent_partitions = get_adjacent_partitions(self.G, self.partitions)

    def set_partitions_and_partitions_vertices(self):
        self.partitions_vertices = get_partitions_vertices(self.G, self.partitions)

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
        print('greedy matching time: {} s'.format(round(time.time() - start, 6)))

    @print_infos
    def improve_partitioning_normal(self):
        for partition, neighbours in self.adjacent_partitions.items():
            for vertex in neighbours:
                improve_bisection(self.G, self.partitions, vertex, partition, self.partitions_vertices,
                                  self.partitions_stats)

    @print_infos
    def improve_partitioning_improved(self):
        adjacent_partitions = create_adjacent_partitions_without_repeats(self.adjacent_partitions)
        for partition, neighbours in adjacent_partitions.items():
            for vertex in neighbours:
                improve_bisection_improved(G=self.G,
                                           bigger_dim=self.bigger_dim,
                                           partitions=self.partitions,
                                           all_vertices=set(self.G.nodes),
                                           partition_a=vertex,
                                           partition_b=partition,
                                           partitions_vertices=self.partitions_vertices,
                                           partitions_stats=self.partitions_stats,
                                           draw=self.draw_partitioning_step,
                                           print_stats=self.print_areas_stats)

    def print_execution_times(self):
        print('\n----------- EXECUTION TIMES -----------')
        if self.conversion_time:
            print('conversion: {} s'.format(round(self.conversion_time, 6)))
        if self.areas_reduction_time:
            print('areas reduction: {} s'.format(round(self.areas_reduction_time, 6)))
        if self.lam_reduction_time:
            print('lam reduction: {} s'.format(round(self.lam_reduction_time, 6)))
        if self.full_restoration_time:
            print('full restoration time: {} s'.format(round(self.full_restoration_time, 6)))
        if self.drawing_initial_grid_time:
            print('drawing initial grid: {} s'.format(round(self.drawing_initial_grid_time, 2)))
        if self.drawing_graph_time:
            print('drawing graph: {} s'.format(round(self.drawing_graph_time, 6)))
        if self.drawing_partitioned_grid_time:
            print('drawing partitioned grid: {} s'.format(round(self.drawing_partitioned_grid_time, 6)))
        print('---------------------------------------')

    def print_areas_stats(self):
        print('\n-------------------------- AREAS STATS --------------------------')
        if not len(self.partitions_stats):
            print("No partitions to print information about.")
            return

        for partition_number, weight in self.partitions_stats.items():
            print('partition: {:>3} | proportional size: {:>3}% | size:  {}'.format(partition_number, round(
                weight / self.grid_size * 100), weight))
        print('-----------------------------------------------------------------')

    def count_diff_between_smallest_and_biggest_partition(self):
        if not len(self.partitions_stats):
            print("No partitions.")
            return

        smallest = float('inf')
        biggest = -float('inf')
        for partition_number, weight in self.partitions_stats.items():
            if weight > biggest:
                biggest = weight
            if weight < smallest:
                smallest = weight

        return biggest - smallest
