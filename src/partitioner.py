from src.grid import Grid
from src.nodes_partitioner import NodesPartitioner


class Partitioner:

    def __init__(self, grid_name):
        self.grid_name = grid_name

    def partition_for_computations(self, number_of_cores, number_of_nodes, p, s, show_progress=False):
        grid1 = Grid(show_progress=show_progress)
        grid1.load_image(self.grid_name)
        grid1.reduce_areas()
        grid1.reduce_by_lam(number_of_cores * number_of_nodes)
        grid1.create_partitions()
        grid1.fully_restore_with_partitions_improvement(0.1)
        grid1.remove_noises()
        grid1.draw_partitioned_grid(p, s)
        compact_G = grid1.create_compact_graph()

        nodes_partitioner = NodesPartitioner(show_progress=show_progress)
        nodes_partitioner.load_partitioned_graph_object(compact_G=compact_G,
                                                        number_of_partitions=number_of_nodes * number_of_cores)
        partitions = nodes_partitioner.get_equal_partitioning_by_lam(number_of_nodes)

        grid1.load_new_partitions(partitions)
        grid1.fully_restore()
        grid1.draw_partitioned_grid(p, s)
        # grid1.print_areas_stats()

    def normal_partitioning(self, number_of_partitions, show_progress=False):
        grid = Grid(show_progress=show_progress)
        grid.load_image(self.grid_name)
        grid.draw_initial_grid(1, 100)
        grid.reduce_areas()
        grid.reduce_by_lam(number_of_partitions, draw_steps=False)
        grid.create_partitions()
        grid.fully_restore_with_partitions_improvement()
        grid.remove_noises()
        grid.print_areas_stats()
        grid.draw_partitioned_grid(1, 100)

    def run_experiment(self, number_of_iterations, number_of_partitions):
        smallest_cut_size = float("inf")
        grid_to_draw = None
        for i in range(number_of_iterations):
            print('ITERATION', i + 1)
            grid = Grid(self.grid_name, show_progress=False)
            grid.reduce_areas()
            grid.reduce_by_lam(number_of_partitions, draw_steps=False)
            grid.create_partitions()
            grid.fully_restore_with_partitions_improvement()

            cut_size = grid._get_cut_size()
            if grid.last_number_of_partitions == number_of_partitions and cut_size < smallest_cut_size:
                print('CUT_SIZE:', cut_size)
                smallest_cut_size = cut_size
                grid_to_draw = grid
        grid_to_draw.draw_partitioned_grid(1, 3)
