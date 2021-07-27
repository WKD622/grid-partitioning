from src.partitioner import Partitioner

partitioner = Partitioner('empty_6.png')
partitioner.partition_for_computations(number_of_cores=4,
                                       number_of_nodes=4,
                                       s=4,
                                       grid_base_size=2,
                                       remove_off=True)
