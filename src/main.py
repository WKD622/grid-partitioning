from src.graph_utils.helpful_sets import get_partitions_vertices, get_adjacent_partitions
from src.grid import Grid

grid = Grid('empty_3.png')
grid.reduce_areas()
grid.reduce_by_lam(2)
grid.partition()
get_partitions_vertices(grid.G)
print(get_adjacent_partitions(grid.G))
grid.fully_restore()
grid.draw_partitioned_grid(1, 60)
# grid.print_execution_times()
# grid.print_areas_stats()
