
from src.grid import Grid

grid = Grid('empty_3.png')
# grid.draw_initial_grid(1, 20)
grid.reduce_areas()
grid.reduce_by_lam(2)
grid.partition()
grid.fully_restore()
# grid.draw_partitioned_grid(1, 80)
grid.improve_partitioning()
# grid.draw_partitioned_grid(1, 80)
# grid.print_execution_times()
# grid.print_areas_stats()
