import cv2
import networkx as nx

from src.definitions import NORMAL_AREA

PARTITION_1 = (255, 0, 255)
PARTITION_2 = (0, 255, 0)


def get_partition_number(pixel):
    if tuple(pixel) == PARTITION_1:
        return 1
    return 2


def parse_partitioning(path):
    image = cv2.imread(path)
    image_shape = (image.shape[0], image.shape[1])
    partition_1_vertices = set()
    partition_2_vertices = set()
    G = nx.Graph(shape=image_shape)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            node_num = y * image.shape[1] + x
            partition = get_partition_number(image[y][x])
            if partition == 1:
                partition_1_vertices.add(node_num)
            else:
                partition_2_vertices.add(node_num)
            G.add_node(node_num, data={'type': NORMAL_AREA, 'x': x, 'y': y, 'num': node_num, 'lvl': 0, 'weight': 1,
                                       'partition': partition})
            if x > 0:
                G.add_edge(y * image.shape[1] + x - 1, node_num, w=1)
            if y > 0:
                G.add_edge((y - 1) * image.shape[1] + x, node_num, w=1)
    print("conversion finished: 100%")
    partitions_vertices = {1: partition_1_vertices, 2: partition_2_vertices}
    return G, image.shape[0] * image.shape[1], partitions_vertices
