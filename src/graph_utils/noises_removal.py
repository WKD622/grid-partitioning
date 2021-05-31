import math


def remove_noises(G, horizontal_size, partitions, partitions_vertices, number_of_partitions):
    areas = find_areas(G, horizontal_size, partitions, number_of_partitions)
    biggest_size_indexes = find_biggest_partitions_areas(areas, number_of_partitions)
    remove_small_partitions(areas, biggest_size_indexes, partitions, partitions_vertices)


def find_areas(G, horizontal_size, partitions, number_of_partitions):
    areas = init_areas(number_of_partitions)
    for node_num in sorted(G.nodes):

        node_partition = partitions[node_num]
        added = False
        if upper_node_exists(node_num, horizontal_size):
            upper_node_partition = get_upper_node_partition(node_num, horizontal_size, partitions)
            if upper_node_partition == node_partition:
                added = True
                append_to_area(upper_node_number(node_num, horizontal_size), node_num, upper_node_partition, areas)

        if left_node_exists(node_num, horizontal_size):
            left_node_partition = get_left_node_partition(node_num, partitions)
            if left_node_partition == node_partition:
                parent_number = left_node_number(node_num)
                left_area = get_area(parent_number, areas[left_node_partition])
                upper_area = get_area(upper_node_number(node_num, horizontal_size), areas[left_node_partition])

                if added and are_different_areas(left_area, upper_area):
                    update_area(parent_number, upper_area, left_node_partition, areas)
                    areas[node_partition].remove(upper_area)
                else:
                    append_to_area(parent_number, node_num, left_node_partition, areas)
                added = True

        if not added:
            create_new_area(node_num, partitions, areas)
    return areas


def init_biggest_partitions_index(number_of_partitions):
    biggest_size = {}
    for i in range(number_of_partitions):
        biggest_size[i] = -1
    return biggest_size


def find_biggest_partitions_areas(areas, number_of_partitions):
    biggest_size_indexes = init_biggest_partitions_index(number_of_partitions)
    for partition_number, partition_areas in areas.items():
        biggest_partition_size = -math.inf
        for index, partition_area in enumerate(partition_areas):
            if len(partition_area) > biggest_partition_size:
                biggest_partition_size = len(partition_area)
                biggest_size_indexes[partition_number] = index
    return biggest_size_indexes


def remove_small_partitions(areas, biggest_size_indexes, partitions, partitions_vertices):
    for partition_number, partition_areas in areas.items():
        if len(partition_areas) > 1:
            for index, partition_area in enumerate(partition_areas):
                if index != biggest_size_indexes[partition_area]:
                    merge_partition_area(partition_area, partitions, partitions_vertices)


def merge_partition_area(partition_area, partitions, partitions_vertices):
    partition_to_merge_with = get_partition_number_to_merge_with(partition_area)
    for vertex in partition_area:
        pass


def get_partition_number_to_merge_with(partition_area):
    return 1


def get_merged_areas(number_of_partitions, areas):
    merged_areas = init_areas(number_of_partitions)
    for key, partition_areas in areas.items():
        merged_partition_areas = set()
        for partition_area in partition_areas:
            merged_partition_areas.update(partition_area)
        merged_areas[key] = merged_partition_areas
    return merged_areas


def are_different_areas(area_1, area_2):
    return area_1 != area_2


def create_new_area(node_num, partitions, areas):
    areas[partitions[node_num]].append({node_num})


def get_area(parent, partition_areas):
    for partition_area in partition_areas:
        if parent in partition_area:
            return partition_area


def append_to_area(parent, node_num, partition, areas):
    partition_areas = areas[partition]
    get_area(parent, partition_areas).add(node_num)


def update_area(parent, another_partition_area, partition, areas):
    partition_areas = areas[partition]
    get_area(parent, partition_areas).update(another_partition_area)


def upper_node_exists(node_num, horizontal_size):
    return node_num - horizontal_size >= 0


def left_node_exists(node_num, horizontal_size):
    return node_num - 1 >= 0 and node_num % horizontal_size != 0


def get_upper_node_partition(node_num, horizontal_size, partitions):
    return partitions[upper_node_number(node_num, horizontal_size)]


def get_left_node_partition(node_num, partitions):
    return partitions[left_node_number(node_num)]


def init_areas(number_of_partitions):
    grouped_partitions = {}
    for i in range(number_of_partitions):
        grouped_partitions[i] = []
    return grouped_partitions


def upper_node_number(node_num, horizontal_size):
    return node_num - horizontal_size


def left_node_number(node_num):
    return node_num - 1
