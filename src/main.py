from src.grid import Grid

grid = Grid('empty_5.png')
grid.reduce_areas()
grid.reduce_by_lam(16, draw_steps=False)
grid.partition()
grid.fully_restore()
# grid.print_areas_stats()
# grid.draw_partitioned_grid(1, 12)
grid.improve_partitioning_improved()
grid.draw_partitioned_grid(1, 12)
