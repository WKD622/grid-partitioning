from src.grid import Grid

grid = Grid('empty_6.png')
grid.reduce_areas()
grid.reduce_by_lam(8, draw_steps=False)
grid.partition()
grid.fully_restore()
# grid.print_areas_stats()
grid.draw_partitioned_grid(1, 40)
grid.improve_partitioning_improved()
grid.draw_partitioned_grid(1, 30)
