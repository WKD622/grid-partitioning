from src.grid import Grid

grid = Grid('empty_3.png')
grid.reduce_areas()
grid.reduce_by_lam(10, draw_steps=False)
grid.partition()
grid.fully_restore()
grid.draw_partitioned_grid(1, 50)
grid.print_areas_stats()
grid.improve_partitioning()
grid.draw_partitioned_grid(1, 50)
