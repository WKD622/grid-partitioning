import time
from math import floor

import matplotlib.pyplot as plt
import networkx as nx

from src.definitions import NORMAL_AREA
from src.graph_utils.helpful_sets.algorithm import improve_bisection, improve_bisection_improved
from src.graph_utils.helpful_sets.balancing_sets.balance_sets_greedily import balance_greedily_normal
from src.graph_utils.helpful_sets.helpers import (get_partitions_vertices, get_adjacent_partitions,
                                                  create_adjacent_partitions_without_repeats)
from src.graph_utils.lam_algorithm import greedy_matching as greedy_matching_helper, lam_algorithm
from src.graph_utils.noises_removal import remove_noises
from src.graph_utils.reduction import reduce_areas as reduce_areas_helper, reduce_vertices as reduce_vertices_helper
from src.graph_utils.restoration import restore_area as restore_area_helper
from src.grid_to_image.draw import optimized_convert_graph_to_image_2, convert_partitioned_graph_to_image
from src.image_to_graph.conversion import convert_image_to_graph
from src.parse_partitioning.parse_partitioning import parse_partitioning
from src.utils import get_project_root, print_infos


class Grid:

    def __init__(self, show_progress=True):
        self.show_progress = show_progress
        self.reductions = []
        self.areas_reductions = []
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
        self.conversion_time = None
        self.grid_size = None
        self.G = None
        self.areas = None
        self.last_number_of_partitions = None
        self.vertical_size = None
        self.horizontal_size = None
        self.bigger_dim = None
        self.smaller_dim = None

    @print_infos
    def load_image(self, grid_name):
        if grid_name:
            start = time.time()
            G, areas, grid_size, dim_1, dim_2 = convert_image_to_graph(str(get_project_root()) + '/grids/' + grid_name,
                                                                       self.show_progress)
            self.conversion_time = time.time() - start
            self.grid_size = grid_size
            self.G = G
            self.areas = areas
            self.last_number_of_partitions = G.number_of_nodes()
            self.vertical_size = dim_1
            self.horizontal_size = dim_2
            self.bigger_dim = dim_1 if dim_1 > dim_2 else dim_2
            self.smaller_dim = dim_1 if dim_1 < dim_2 else dim_2

    def load_graph(self, G):
        self.G = G

    @print_infos
    def load_ready_partitioning(self, partitioning_name):
        G, grid_size, partitions_vertices = parse_partitioning(
            str(get_project_root()) + '/partitionings/' + partitioning_name)
        self.G = G
        self.last_number_of_partitions = 2
        self.adjacent_partitions = {1: [2], 2: [1]}
        self.partitions_vertices = partitions_vertices

    @print_infos
    def reduce_areas(self):
        """
        Reduces all specific areas like indivisible area. Should happen after parsing the initial grid.
        """
        start = time.time()
        new_vertices_names = reduce_areas_helper(self.G, self.areas)
        self.areas_reductions = self.areas_reductions + new_vertices_names
        self.areas_reduction_time = time.time() - start

    @print_infos
    def reduce_by_lam(self, number_of_partitions, draw_steps=False):
        def remove_unnecessary_matches(last_number_of_partitions, number_of_partitions):
            if last_number_of_partitions - len(matches) < number_of_partitions:
                while last_number_of_partitions - len(matches) != number_of_partitions:
                    matches.pop()
            return matches

        general_start = time.time()
        i = 1
        T = self._calculate_maximal_number_of_episodes(number_of_partitions)
        while self.G.number_of_nodes() > number_of_partitions:
            start = time.time()
            matches = lam_algorithm(self.G, number_of_partitions, T, i, self.grid_size, self.show_progress)
            matches = remove_unnecessary_matches(self.last_number_of_partitions, number_of_partitions)
            for match in matches:
                self._reduce(match)
                self.last_number_of_partitions = self.G.number_of_nodes()
            if draw_steps:
                self._draw_partitioning_step()

            if self.show_progress:
                print('{}) reduce: {:<3} s | nodes: {}'.format(i, round(time.time() - start, 2),
                                                               self.G.number_of_nodes()))
            i += 1
        self.lam_reduction_time = time.time() - general_start

    @print_infos
    def greedy_matching(self):
        """
        Same function as lam_algorithm, much simpler though. Just matches vertices greedily where the highest weight
        edge appears.
        """
        start = time.time()
        greedy_matching_helper(self)
        print('greedy matching time: {} s'.format(round(time.time() - start, 6)))

    @print_infos
    def create_partitions(self):
        partition_number = 0
        for node in self.G.nodes:
            self.partitions[node] = partition_number
            partition_number += 1

        self._fill_stats()
        self._set_adjacent_partitions()
        self._set_partitions_and_partitions_vertices()

    @print_infos
    def fully_restore(self):
        """
        Restores graph completely without any modification.
        """
        start = time.time()
        while len(self.reductions) > 0:
            self._restore_one_step()
        self.full_restoration_time = time.time() - start

    @print_infos
    def fully_restore_with_partitions_improvement(self):
        """
        Restores graph completely with improvements.
        """
        start = time.time()
        number_of_reductions_done = 0
        init_red_length = len(self.reductions)
        while len(self.reductions) > 0:
            self._restore_one_step()
            number_of_reductions_done += 1
            if (number_of_reductions_done / init_red_length > 0.90
                    and floor(len(self.reductions) % (init_red_length * 0.03)) == 0):
                pass
                self._improve_partitioning_improved()
        self._improve_partitioning_improved()
        while len(self.areas_reductions) > 0:
            self._restore_areas_one_step()
        self.full_restoration_time = time.time() - start

    @print_infos
    def improve_partitioning_normal(self):
        """
        Improves partitioning. Works only with vertices without weights.
        """
        for partition, neighbours in self.adjacent_partitions.items():
            for vertex in neighbours:
                improve_bisection(self.G, self.partitions, vertex, partition, self.partitions_vertices,
                                  self.partitions_stats)

    @print_infos
    def _improve_partitioning_improved(self):
        """
        Improves partitioning. Multilevel algorithm for weighted graphs.
        """
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
                                           draw=self._draw_one_step_of_restoration)

    @print_infos
    def balance_areas(self):
        """
        Balances areas without cut-size improvements.
        """
        adjacent_partitions = create_adjacent_partitions_without_repeats(self.adjacent_partitions)
        for partition, neighbours in adjacent_partitions.items():
            for vertex in neighbours:
                balance_greedily_normal(G=self.G,
                                        p=0.5,
                                        partition_a=partition,
                                        partition_b=vertex,
                                        partitions_vertices=self.partitions_vertices,
                                        partitions_stats=self.partitions_stats,
                                        partitions=self.partitions)

    @print_infos
    def remove_noises(self):
        remove_noises(G=self.G,
                      horizontal_size=self.horizontal_size,
                      partitions=self.partitions,
                      partitions_vertices=self.partitions_vertices,
                      number_of_partitions=self.last_number_of_partitions,
                      partitions_stats=self.partitions_stats)

    @print_infos
    def draw_initial_grid(self, p, s, name='initial'):
        if len(self.reductions) == 0:
            start = time.time()
            optimized_convert_graph_to_image_2(G=self.G,
                                               areas=self.areas,
                                               p=p,
                                               s=s,
                                               vertical_size=self.vertical_size,
                                               horizontal_size=self.horizontal_size,
                                               name=name)
            self.drawing_initial_grid_time = time.time() - start
        else:
            print("You cannot draw initial graph due to reductions")

    @print_infos
    def draw_partitioned_grid(self, p, s, name='output', save=False, title=''):
        start = time.time()
        convert_partitioned_graph_to_image(G=self.G,
                                           p=p,
                                           s=s,
                                           number_of_partitions=self.last_number_of_partitions,
                                           partitions=self.partitions,
                                           vertical_size=self.vertical_size,
                                           horizontal_size=self.horizontal_size,
                                           name=name,
                                           save=save,
                                           title=title)
        self.drawing_partitioned_grid_time = time.time() - start

    @print_infos
    def get_compact_graph(self):
        compact_G = self.G.copy()
        print(compact_G)
        print(self.G)
        for partition_number, vertices in self.partitions_vertices.items():
            reduce_vertices_helper(compact_G, vertices, NORMAL_AREA)
        return compact_G

    def print_execution_times(self):
        print('\n----------- EXECUTION TIMES -----------')
        if self.conversion_time:
            print('conversion: {} s'.format(round(self.conversion_time, 6)))
        if self.areas_reduction_time:
            print('areas reduction: {} s'.format(round(self.areas_reduction_time, 6)))
        if self.lam_reduction_time:
            print('lam reduction: {} s'.format(round(self.lam_reduction_time, 6)))
        if self.full_restoration_time:
            print('full restoration and improvement time: {} s'.format(round(self.full_restoration_time, 6)))
        if self.drawing_initial_grid_time:
            print('drawing initial grid: {} s'.format(round(self.drawing_initial_grid_time, 2)))
        if self.drawing_graph_time:
            print('drawing graph: {} s'.format(round(self.drawing_graph_time, 6)))
        if self.drawing_partitioned_grid_time:
            print('drawing partitioned grid: {} s'.format(round(self.drawing_partitioned_grid_time, 6)))
        print('---------------------------------------')

    def print_areas_stats(self):
        print('\n-------------------------- AREAS STATS --------------------------')
        print("CUT SIZE: ", self._get_cut_size())
        if not len(self.partitions_stats):
            print("No partitions to print information about.")
            return

        for partition_number, weight in self.partitions_stats.items():
            print('partition: {:>3} | proportional size: {:>3}% | size:  {}'.format(partition_number, round(
                weight / self.grid_size * 100), weight))
        print('-----------------------------------------------------------------')

    """
    Methods to be used internally
    """

    def _reduce(self, vertices_to_reduce):
        """
        Does one step of reduction of specified vertices_to_reduce which should be a set.
        """
        new_vertex_name = reduce_vertices_helper(self.G, vertices_to_reduce, NORMAL_AREA)
        self.reductions.append(new_vertex_name)

    def _restore_area(self, vertex):
        """
        Restores given reduction.
        """
        restore_area_helper(self.G, vertex)

    def _restore_one_step(self):
        if len(self.reductions) > 0:
            self._restore_area(self.reductions.pop())
        else:
            print("No areas to restore")

    def _restore_areas_one_step(self):
        if len(self.areas_reductions) > 0:
            self._restore_area(self.areas_reductions.pop())
        else:
            print("No areas to restore")

    @print_infos
    def _draw_graph(self):
        """
        Draws graph with vertices numbers. Recommended only for small graphs.
        """
        start = time.time()
        nx.draw(self.G, with_labels=True, font_weight='bold')
        self.drawing_graph_time = time.time() - start
        plt.show()

    def _calculate_maximal_number_of_episodes(self, number_of_partitions):
        i = 0
        graph_size = self.G.number_of_nodes()
        while graph_size / 2 > number_of_partitions:
            i += 1
            graph_size = graph_size / 2
        return i

    def _draw_partitioning_step(self, p, s, title='', save=False, name='name'):
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

        convert_partitioned_graph_to_image(G=G_copy,
                                           p=p,
                                           s=s,
                                           number_of_partitions=last_number_of_partitions,
                                           partitions=self.partitions,
                                           vertical_size=self.vertical_size,
                                           horizontal_size=self.horizontal_size,
                                           name=name,
                                           save=save,
                                           title=title)

    def _draw_one_step_of_restoration(self, p, s, title=''):
        G = self.G.copy()
        reductions = self.reductions.copy()
        areas_reductions = self.areas_reductions.copy()
        while len(reductions) > 0:
            restore_area_helper(G, reductions.pop())
        while len(areas_reductions) > 0:
            restore_area_helper(G, areas_reductions.pop())
        convert_partitioned_graph_to_image(G=G,
                                           p=p,
                                           s=s,
                                           number_of_partitions=self.last_number_of_partitions,
                                           partitions=self.partitions,
                                           vertical_size=self.vertical_size,
                                           horizontal_size=self.horizontal_size,
                                           name='name',
                                           save=False,
                                           title=title)

    def _add_to_partitions_stats(self, partition_number, partition_weight):
        self.partitions_stats[partition_number] = partition_weight

    def _fill_stats(self):
        self.partitions_stats = {}
        partition_number = 0
        for node in self.G.nodes:
            self._add_to_partitions_stats(partition_number,
                                          self.G.nodes[node]['data']['weight'])
            partition_number += 1

    def _set_adjacent_partitions(self):
        self.adjacent_partitions = get_adjacent_partitions(self.G, self.partitions)

    def _set_partitions_and_partitions_vertices(self):
        self.partitions_vertices = get_partitions_vertices(self.G, self.partitions)

    def _get_highest_degree(self):
        degrees = sorted(d for n, d in self.G.degree())
        return degrees[-1]

    def _get_smallest_degree(self):
        degrees = sorted(d for n, d in self.G.degree())
        return degrees[0]

    def _get_edge_with_smallest_weight(self):
        return sorted(self.G.edges.data('w'), key=lambda x: x[2])[0]

    def _get_edge_with_highest_weight(self):
        return sorted(self.G.edges.data('w'), key=lambda x: x[2])[len(self.G.edges) - 1]

    def _get_cut_size(self):
        counter = 0
        for a, b in self.G.edges:
            if self.partitions[a] != self.partitions[b]:
                counter += 1
        return counter

    def _count_diff_between_smallest_and_biggest_partition(self):
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
