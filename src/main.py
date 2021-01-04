from src.grid import Grid

grid = Grid('grid9.png')
# print(grid.get_highest_degree())
# print(grid.get_smallest_degree())
# grid.reduce_areas()
# print(grid.get_highest_degree())
# print(grid.get_smallest_degree())
grid.draw_graph()
grid.reduce_by_lam()
# print(grid.get_highest_degree())
# print(grid.get_smallest_degree())
# grid.fully_restore()
grid.print_execution_times()
