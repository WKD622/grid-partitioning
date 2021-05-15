from src.grid import Grid


def run_experiment(number_of_iterations, number_of_partitions):
    smallest_diff = float("inf")

    for i in range(number_of_iterations):
        print('ITERATION', i + 1)
        grid = Grid('empty_5.png', show_progress=False)
        grid.reduce_areas()
        grid.reduce_by_lam(number_of_partitions, draw_steps=False)
        grid.partition()

        diff = grid.count_diff_between_smallest_and_biggest_partition()
        if grid.last_number_of_partitions == number_of_partitions and diff < smallest_diff:
            smallest_diff = diff
            grid.fully_restore()
            grid.improve_partitioning_normal()
            grid.draw_partitioned_grid(1, 12)
            grid.print_areas_stats()
