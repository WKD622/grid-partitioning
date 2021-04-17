from src.grid import Grid

grid = Grid('grid16.png')
grid.reduce_areas()
grid.reduce_by_lam(9)
grid.divide()
grid.fully_restore()
grid.draw_partitioned_grid(1, 6)
grid.print_execution_times()
