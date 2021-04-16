import cv2
import networkx as nx
import numpy as np

from src.definitions import NORMAL_AREA, INDIVISIBLE_AREA, OFF_AREA
from src.image_to_graph.helpers import is_normal, is_indivisible


def get_pixel_type(pixel):
    if is_normal(pixel):
        return NORMAL_AREA
    elif is_indivisible(pixel):
        return INDIVISIBLE_AREA
    return OFF_AREA


def handle_area(x, y, image, pixel_type, areas_map, areas, node_num, G, initial_area_number):
    if x > 0 and get_pixel_type(image[y][x - 1]) == pixel_type:
        prev_pixel_type = get_pixel_type(image[y][x - 1])
        area_number = areas_map[y][x - 1]
        areas_map[y][x] = area_number
        areas[prev_pixel_type][area_number].append(node_num)
    elif y > 0 and get_pixel_type(image[y - 1][x]) == pixel_type:
        prev_pixel_type = get_pixel_type(image[y - 1][x])
        area_number = areas_map[y - 1][x]
        areas_map[y][x] = area_number
        areas[prev_pixel_type][area_number].append(node_num)
    else:
        areas_map[y][x] = initial_area_number
        areas[pixel_type][initial_area_number] = [node_num]
        initial_area_number += 1
    return initial_area_number


def print_progress(node_num, number_of_vertices):
    if node_num % 10000 == 0:
        print("conversion progress: " + str(round(node_num * 100 / number_of_vertices)) + "%")


def convert_image_to_graph(path):
    image = cv2.imread(path)
    image_shape = (image.shape[0], image.shape[1])
    number_of_vertices = image.shape[0] * image.shape[1]
    areas_map = np.zeros(image_shape).astype(int)
    initial_area_number = 0
    areas = {OFF_AREA: {}, INDIVISIBLE_AREA: {}}
    G = nx.Graph(shape=image_shape)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            node_num = y * image.shape[1] + x
            print_progress(node_num, number_of_vertices)
            pixel_type = get_pixel_type(image[y][x])
            G.add_node(node_num, data={'type': pixel_type, 'x': x, 'y': y, 'num': node_num, 'lvl': 0, 'count': 1})
            if x > 0:
                G.add_edge(y * image.shape[1] + x - 1, node_num, w=1)
            if y > 0:
                G.add_edge((y - 1) * image.shape[1] + x, node_num, w=1)
            if pixel_type != NORMAL_AREA:
                initial_area_number = handle_area(x, y, image, pixel_type, areas_map, areas, node_num, G,
                                                  initial_area_number)
    print("conversion finished: 100%")
    return G, areas
