from src.grid import Grid


def run_experiment(number_of_iterations, number_of_partitions):
    smallest_cut_size = float("inf")
    grid_to_draw = None
    for i in range(number_of_iterations):
        print('ITERATION', i + 1)
        grid = Grid('empty_4.png', show_progress=False)
        grid.reduce_areas()
        grid.reduce_by_lam(number_of_partitions, draw_steps=False)
        grid.partition()
        grid.fully_restore_with_partitions_improvement()

        cut_size = grid.get_cut_size()
        if grid.last_number_of_partitions == number_of_partitions and cut_size < smallest_cut_size:
            print('CUT_SIZE:', cut_size)
            smallest_cut_size = cut_size
            grid_to_draw = grid
    grid_to_draw.draw_partitioned_grid(1, 3)
