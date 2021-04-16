import time

from src.graph_utils.lam_algorithm import lam_algorithm
from src.grid import Grid

grid = Grid('grid16.png')
grid.reduce_areas()
grid.reduce_by_lam(9)

# grid = Grid('grid16.png')
# grid.draw_initial_grid(1, 6, 'initial3')

# for i in range(14):
#     grid = Grid('grid16.png')
#     grid.reduce_areas()
#     grid.reduce_by_lam(9)
#     grid.divide()
#     grid.fully_restore()
#     grid.draw_partitioned_grid(1, 6, "b" + str(i))

# grid.print_execution_times()
# grid.test_dividing(4)
