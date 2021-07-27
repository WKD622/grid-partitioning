import time

import numpy

from src.grid import Grid
from src.nodes_partitioner import NodesPartitioner


class Partitioner:

    def __init__(self, grid_name):
        self.grid_name = grid_name

    def partition_for_computations(self, number_of_cores, number_of_nodes, s, p=1, show_progress=False,
                                   remove_off=False):
        grid1 = Grid(show_progress=show_progress)
        grid1.load_image(self.grid_name, remove_off=remove_off)
        grid1.draw_initial_grid(p, s)
        grid1.reduce_areas()
        grid1.reduce_by_lam(number_of_cores * number_of_nodes)
        grid1.create_partitions()
        grid1.fully_restore_with_partitions_improvement(0.5)
        grid1.remove_noises()
        grid1.draw_partitioned_grid(p, s)
        compact_G = grid1.create_compact_graph()

        nodes_partitioner = NodesPartitioner(show_progress=show_progress)
        nodes_partitioner.load_partitioned_graph_object(compact_G=compact_G,
                                                        number_of_partitions=number_of_nodes * number_of_cores)
        partitions = nodes_partitioner.get_equal_partitioning_by_lam(number_of_nodes)

        grid1.load_new_partitions(partitions)
        grid1.fully_restore()
        grid1.print_areas_stats()
        grid1.draw_partitioned_grid(p, s)
        grid1.print_areas_stats()

    def normal_partitioning(self, number_of_partitions, s, p=1, grid_base_size=5, show_progress=False,
                            remove_off=False):
        grid = Grid(show_progress=show_progress)
        grid.load_image(self.grid_name, remove_off=remove_off)
        grid.draw_initial_grid(p, s, optimized=False)
        start = time.time()
        grid.reduce_areas()
        grid.reduce_by_lam(number_of_partitions, draw_steps=False)
        grid.create_partitions()
        grid.print_areas_stats()
        grid._draw_one_step_of_restoration(p, s)
        grid.fully_restore_with_partitions_improvement(0.2)
        grid.print_execution_times()
        print(time.time() - start)
        grid.remove_noises()
        grid.print_areas_stats()
        grid.draw_partitioned_grid(p, s, base_size=grid_base_size)

    def run_experiment_cut_size(self, number_of_iterations, number_of_partitions, s, grid_base_size=5,
                                remove_off=False):
        smallest_cut_size = float("inf")
        grid_to_draw = None
        for i in range(number_of_iterations):
            print('ITERATION', i + 1)
            grid = Grid(show_progress=False)
            grid.load_image(self.grid_name, remove_off=remove_off)
            grid.reduce_areas()
            grid.reduce_by_lam(number_of_partitions, draw_steps=False)
            grid.create_partitions()
            grid.fully_restore_with_partitions_improvement(p=0.3)
            grid.remove_noises()
            cut_size = grid._get_cut_size()
            if cut_size < smallest_cut_size:
                print('CUT_SIZE:', cut_size)
                smallest_cut_size = cut_size
                grid_to_draw = grid
        grid_to_draw.draw_initial_grid(p=1, s=s, base_size=grid_base_size)
        grid_to_draw.draw_partitioned_grid(p=1, s=s, base_size=grid_base_size)
        grid_to_draw.print_areas_stats()

    def run_experiment_areas_size_diff(self, number_of_iterations, number_of_partitions, s, grid_base_size=5,
                                       remove_off=False):
        smallest_areas_diff = float("inf")
        grid_to_draw = None
        for i in range(number_of_iterations):
            print('ITERATION', i + 1)
            grid = Grid(show_progress=False)
            grid.load_image(self.grid_name, remove_off=remove_off)
            grid.reduce_areas()
            grid.reduce_by_lam(number_of_partitions, draw_steps=False)
            grid.create_partitions()
            grid.fully_restore_with_partitions_improvement(p=0.3)
            grid.remove_noises()

            max_area, min_area = grid.get_highest_and_smallest_partition()
            diff = max_area - min_area
            if diff < smallest_areas_diff:
                cut_size = grid._get_cut_size()
                print('CUT_SIZE:', cut_size)
                print('DIFF:', diff)
                smallest_areas_diff = diff
                grid_to_draw = grid
        grid_to_draw.draw_initial_grid(p=1, s=s, base_size=grid_base_size)
        grid_to_draw.draw_partitioned_grid(p=1, s=s, base_size=grid_base_size)
        grid_to_draw.print_areas_stats()

    def run_experiment_areas_size_std(self, number_of_iterations, number_of_partitions, s, grid_base_size=5,
                                      remove_off=False):
        min_std = float("inf")
        grid_to_draw = None
        for i in range(number_of_iterations):
            print('ITERATION', i + 1)
            grid = Grid(show_progress=False)
            grid.load_image(self.grid_name, remove_off=remove_off)
            grid.reduce_areas()
            grid.reduce_by_lam(number_of_partitions, draw_steps=False)
            grid.create_partitions()
            grid.fully_restore_with_partitions_improvement(p=0.3)
            grid.remove_noises()

            std = numpy.std(numpy.array(list(grid.partitions_stats.values())))
            if std < min_std:
                cut_size = grid._get_cut_size()
                print('CUT_SIZE:', cut_size)
                print('STD:', std)
                min_std = std
                grid_to_draw = grid
        grid_to_draw.draw_initial_grid(p=1, s=s, base_size=grid_base_size)
        grid_to_draw.draw_partitioned_grid(p=1, s=s, base_size=grid_base_size)
        grid_to_draw.print_areas_stats()
