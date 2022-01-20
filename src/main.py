from src.partitioner import Partitioner

partitioner = Partitioner('empty_7.png')
partitioner.partition_for_computations(number_of_iterations=100,
                                       number_of_cores=4,
                                       number_of_nodes=6,
                                       s=7,
                                       grid_base_size=7,
                                       remove_off=True)
