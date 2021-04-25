from src.graph_utils.helpful_sets import get_partitions_vertices, get_adjacent_partitions, count_cut_size
from src.grid import Grid

grid = Grid('empty_3.png')
grid.reduce_areas()
grid.reduce_by_lam(2)
grid.partition()
grid.fully_restore()
partition = grid.partitions_vertices[0]
grid.draw_partitioned_grid(1, 60)
# grid.print_execution_times()
# grid.print_areas_stats()
