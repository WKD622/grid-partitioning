from src.grid import Grid


class Partitioner:

    def __init__(self, grid_name):
        self.grid_name = grid_name

    def partition_for_computations(self, number_of_cores, number_of_nodes, p, s):
        grid = Grid(show_progress=False)
        grid.load_image(self.grid_name)
        grid.reduce_areas()
        grid.reduce_by_lam(number_of_cores * number_of_nodes, draw_steps=False)
        grid.create_partitions()
        grid.fully_restore_with_partitions_improvement()
        grid.remove_noises()
        grid.draw_partitioned_grid(p, s, title='all partitions')
        compact_G = grid.get_compact_graph()
        print(compact_G)
        # grid.reduce_by_lam(number_of_nodes)
        # grid.create_partitions()
        # print(grid.partitions_vertices)
        # grid.draw_partitioned_grid(p, s, title='partitions for nodes')
        # grid.equalize_areas()
        # grid.fully_restore()

        # grid.print_areas_stats()

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
