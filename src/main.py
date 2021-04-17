from src.grid import Grid


for i in range(5):
    grid = Grid('empty_3.png')
    grid.reduce_areas()
    grid.reduce_by_lam(4)
    grid.partition()
    grid.fully_restore()
    grid.draw_partitioned_grid(1, 40, "f" + str(i), save=True)
    grid.print_execution_times()
    grid.print_areas_stats()
