from src.grid import Grid

grid = Grid('grid19.png')
grid.reduce_areas()
grid.reduce_by_lam(4, draw_steps=False)
grid.partition()
grid.fully_restore_with_partitions_improvement()
grid.draw_partitioned_grid(1, 50)
grid.remove_noises()
# grid.print_areas_stats()
# grid.draw_partitioned_grid(1, 5)

# run_experiment(100, 16)
