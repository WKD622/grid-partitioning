from src.partitioner import Partitioner

partitioner = Partitioner('empty_5.png')
partitioner.partition_for_computations(number_of_iterations=100,
                                       number_of_nodes=4,
                                       number_of_cores=4,
                                       s=5,
                                       grid_base_size=4,
                                       remove_off=False)
