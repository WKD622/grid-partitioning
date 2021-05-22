from src.experiment import run_experiment
from src.grid import Grid

# grid = Grid('empty_6.png')
# # grid.draw_initial_grid(1, 15)
# # grid.reduce_areas()
# grid.reduce_by_lam(10, draw_steps=False)
# grid.partition()
# grid.fully_restore()
# grid.print_areas_stats()
# grid.draw_partitioned_grid(1, 30)
# grid.improve_partitioning_improved()
# grid.draw_partitioned_grid(1, 30)
# grid.print_areas_stats()

run_experiment(100, 16)
