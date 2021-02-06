import time

from src.graph_utils.lam_algorithm import lam_algorithm
from src.grid import Grid

grid = Grid('empty_2.png')

grid.reduce_areas()
grid.reduce_by_lam(6)
grid.divide()
grid.fully_restore()
grid.draw_partitioned_grid(1, 10)
# print(grid.get_highest_degree())
# print(grid.get_smallest_degree())
# print(grid.get_highest_degree())

grid.print_execution_times()
