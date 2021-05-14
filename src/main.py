from src.grid import Grid

show_progress = False
smallest_diff = float("inf")

for i in range(100):
    print('ITERATION', i + 1)
    grid = Grid('empty_5.png', show_progress=show_progress)
    grid.reduce_areas()
    grid.reduce_by_lam(16, draw_steps=False)
    grid.partition()
    grid.fully_restore()
    grid.improve_partitioning()
    diff = grid.count_diff_between_smallest_and_biggest_partition()
    if grid.last_number_of_partitions == 16 and diff < smallest_diff:
        smallest_diff = diff
        grid.draw_partitioned_grid(1, 12)
        grid.print_areas_stats()
