import math
import operator
import random
import time

from src.definitions import NORMAL_AREA
from src.graph_utils.helpful_sets.balancing_sets.balance_sets_greedily import balance_greedily_normal
from src.graph_utils.helpful_sets.helpers import (get_partitions_vertices, get_adjacent_partitions,
                                                  create_adjacent_partitions_without_repeats, move_set_normal)
from src.graph_utils.lam_algorithm import lam_algorithm
from src.graph_utils.reduction import reduce_vertices as reduce_vertices_helper
from src.graph_utils.restoration import restore_area as restore_area_helper
from src.utils import print_infos


class NodesPartitioner:

    def __init__(self, show_progress=True):
        self.show_progress = show_progress
        self.reductions = []
        self.areas_reductions = []
        self.full_restoration_time = None
        self.lam_reduction_time = None
        self.partitions_stats = {}
        self.partitions_vertices = None
        self.adjacent_partitions = None
        self.partitions = {}
        self.grid_size = None
        self.G = None
        self.last_number_of_partitions = None
        self.vertical_size = None
        self.horizontal_size = None
        self.bigger_dim = None
        self.smaller_dim = None

    def load_partitioned_graph_object(self, compact_G, number_of_partitions):
        self.G = compact_G['c_G']
        self.partitions = compact_G['partitions']
        self.partitions_vertices = compact_G['partitions_vertices']
        self.last_number_of_partitions = number_of_partitions
        self.reductions = compact_G['reductions']
        self.horizontal_size = compact_G['horizontal_size']
        self.vertical_size = compact_G['vertical_size']
        self.bigger_dim = self.horizontal_size if self.horizontal_size > self.vertical_size else self.vertical_size
        self.smaller_dim = self.horizontal_size if self.horizontal_size < self.vertical_size else self.vertical_size
        self._set_adjacent_partitions()

    @print_infos
    def get_equal_partitioning_by_lam(self, number_of_nodes):
        self.reduce_by_lam(number_of_nodes)
        self.create_partitions()
        if not self.are_partitions_equal():
            self.balance_areas()
        if not self.are_partitions_equal():
            self.additional_balancing()

        return self.partitions

    @print_infos
    def reduce_by_lam(self, number_of_partitions):
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
            matches = lam_algorithm(self.G, number_of_partitions, T, i, self.show_progress)
            matches = remove_unnecessary_matches(self.last_number_of_partitions, number_of_partitions)
            for match in matches:
                self._reduce(match)
                self.last_number_of_partitions = self.G.number_of_nodes()

            if self.show_progress:
                print('{}) reduce: {:<3} s | nodes: {}'.format(i, round(time.time() - start, 2),
                                                               self.G.number_of_nodes()))
            i += 1
        self.lam_reduction_time = time.time() - general_start

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

    def are_partitions_equal(self):
        if len(self.partitions_stats) > 1:
            first_partition_size = self.partitions_stats[0]
            for partition_number, size in self.partitions_stats.items():
                if size != first_partition_size:
                    return False
            return True

    def find_biggest_and_smallest_partition(self):
        max_ = max(self.partitions_stats.items(), key=operator.itemgetter(1))[0]
        min_ = min(self.partitions_stats.items(), key=operator.itemgetter(1))[0]
        return max_, min_

    def chose_vertex(self, partition_number):
        return random.choice(tuple(self.partitions_vertices[partition_number]))

    @print_infos
    def additional_balancing(self):
        while not self.are_partitions_equal():
            biggest_partition_number, smallest_partition_number = self.find_biggest_and_smallest_partition()
            vertex_to_move = self.chose_vertex(biggest_partition_number)
            move_set_normal(partitions=self.partitions,
                            current_partition=biggest_partition_number,
                            dest_partition=smallest_partition_number,
                            partitions_vertices=self.partitions_vertices,
                            to_be_moved={vertex_to_move},
                            weight=1,
                            partitions_stats=self.partitions_stats)

    @print_infos
    def balance_areas(self):
        """
        Balances areas for  without cut-size improvements.
        """
        for i in range(4):
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

    def print_execution_times(self):
        print('\n----------- EXECUTION TIMES -----------')
        if self.lam_reduction_time:
            print('lam reduction: {} s'.format(round(self.lam_reduction_time, 6)))
        if self.full_restoration_time:
            print('full restoration and improvement time: {} s'.format(round(self.full_restoration_time, 6)))
        print('---------------------------------------')

    def print_areas_stats(self):
        print('\n-------------------------- AREAS STATS --------------------------')
        if not len(self.partitions_stats):
            print("No partitions to print information about.")
            return

        for partition_number, size in self.partitions_stats.items():
            print('partition: {:>3} | size:  {}'.format(partition_number, size))
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

    def _calculate_maximal_number_of_episodes(self, number_of_partitions):
        i = 0
        graph_size = self.G.number_of_nodes()
        while graph_size / 2 > number_of_partitions:
            i += 1
            graph_size = graph_size / 2
        return i

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
