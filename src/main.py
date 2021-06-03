from src.partitioner import Partitioner

partitioner = Partitioner('grid15.png')
partitioner.partition_for_computations(number_of_cores=4, number_of_nodes=4, p=1, s=5)
