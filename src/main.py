from src.partitioner import Partitioner

partitioner = Partitioner('strange22.png')
partitioner.run_experiment_areas_size_std(number_of_iterations=10,
                                          number_of_partitions=16,
                                          s=1,
                                          grid_base_size=7,
                                          remove_off=False)
