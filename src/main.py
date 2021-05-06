from src.grid import Grid

grid = Grid('grid15.png')
# grid.parse_ready_partitioning('partitioning.png')
grid.reduce_areas()
grid.reduce_by_lam(9)
grid.partition()
grid.fully_restore()
grid.draw_partitioned_grid(1, 30)
grid.improve_partitioning()
grid.draw_partitioned_grid(1, 30)
# grid.print_execution_times()
# grid.print_areas_stats()
