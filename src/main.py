from src.grid import Grid

grid = Grid('empty_3.png')
# grid.parse_ready_partitioning('partitioning.png')
grid.reduce_areas()
grid.reduce_by_lam(2, True)
grid.partition()
grid.fully_restore()
grid.draw_partitioned_grid(1, 50)
grid.improve_partitioning()
grid.draw_partitioned_grid(1, 50)
# grid.print_execution_times()
# grid.print_areas_stats()
