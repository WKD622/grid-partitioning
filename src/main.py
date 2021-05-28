from src.experiment import run_experiment
from src.grid import Grid


# grid.draw_initial_grid(1, 5)
for i in range(0, 10):
    grid = Grid('empty_5.png')
    grid.reduce_areas()
    grid.reduce_by_lam(16, draw_steps=False)
    grid.partition()
    grid.print_areas_stats()
    grid.fully_restore_with_partitions_improvement()
    grid.print_areas_stats()
    grid.draw_partitioned_grid(1, 10)


# run_experiment(100, 16)
