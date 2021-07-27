import time

from src.partitioner import Partitioner

start = time.time()
partitioner = Partitioner('strange18.png')
partitioner.run_experiment_cut_size(number_of_iterations=100,
                                    number_of_partitions=10,
                                    s=5,
                                    grid_base_size=4,
                                    remove_off=True)

partitioner = Partitioner('strange18.png')
partitioner.run_experiment_areas_size_std(number_of_iterations=100,
                                          number_of_partitions=10,
                                          s=5,
                                          grid_base_size=4,
                                          remove_off=True)

# partitioner = Partitioner('empty_4.png')
# partitioner.normal_partitioning(number_of_partitions=16, s=3, grid_base_size=5)
# print(time.time() - start)
