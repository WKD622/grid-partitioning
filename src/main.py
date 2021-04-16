import time

from src.graph_utils.lam_algorithm import lam_algorithm
from src.grid import Grid

grid = Grid('empty_3.png')

# grid.draw_initial_grid(1, 10)
# grid.reduce_areas()
# grid.reduce_by_lam(4)
# grid.divide()
# grid.fully_restore()
# grid.draw_partitioned_grid(1, 25)
# print(grid.get_highest_degree())
# print(grid.get_smallest_degree())
# print(grid.get_highest_degree())

# grid.print_execution_times()

grid.test_dividing(4)