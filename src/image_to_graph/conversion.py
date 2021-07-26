import cv2
import networkx as nx
import numpy as np

from src.definitions import NORMAL_AREA, INDIVISIBLE_AREA, OFF_AREA
from src.image_to_graph.helpers import is_normal, is_off


def get_pixel_type(pixel):
    if is_off(pixel):
        return OFF_AREA
    elif is_normal(pixel):
        return NORMAL_AREA
    return INDIVISIBLE_AREA


def handle_indivisible_area(x, y, image, indivisible_areas_sets, indivisible_areas_pixels, node_num,
                            initial_area_number):
    if x > 0 and get_pixel_type(image[y][x - 1]) == INDIVISIBLE_AREA:
        left_node_num = count_node_number(x - 1, y, image)
        indivisible_area_number_l = indivisible_areas_pixels[left_node_num]
        if y > 0 and get_pixel_type(image[y - 1][x]) == INDIVISIBLE_AREA:
            upper_node_num = count_node_number(x, y - 1, image)
            indivisible_area_number_u = indivisible_areas_pixels[upper_node_num]
            if indivisible_area_number_u != indivisible_area_number_l:
                nodes_to_move = indivisible_areas_sets.pop(indivisible_area_number_u)
                for node in nodes_to_move:
                    indivisible_areas_pixels[node] = indivisible_area_number_l
                indivisible_areas_sets[indivisible_area_number_l].update(nodes_to_move)
            indivisible_areas_pixels[node_num] = indivisible_area_number_l
            indivisible_areas_sets[indivisible_area_number_l].add(node_num)
        else:
            indivisible_areas_pixels[node_num] = indivisible_area_number_l
            indivisible_areas_sets[indivisible_area_number_l].add(node_num)
    elif y > 0 and get_pixel_type(image[y - 1][x]) == INDIVISIBLE_AREA:
        upper_node_num = count_node_number(x, y - 1, image)
        indivisible_area_number = indivisible_areas_pixels[upper_node_num]
        indivisible_areas_pixels[node_num] = indivisible_area_number
        indivisible_areas_sets[indivisible_area_number].add(node_num)
    else:
        indivisible_areas_sets[initial_area_number] = {node_num}
        indivisible_areas_pixels[node_num] = initial_area_number
        initial_area_number += 1
    return initial_area_number


def handle_off_area(x, y, image, off_areas_sets, off_areas_pixels, node_num,
                    off_area_number):
    if x > 0 and get_pixel_type(image[y][x - 1]) == OFF_AREA:
        left_node_num = count_node_number(x - 1, y, image)
        indivisible_area_number_l = off_areas_pixels[left_node_num]
        if y > 0 and get_pixel_type(image[y - 1][x]) == OFF_AREA:
            upper_node_num = count_node_number(x, y - 1, image)
            indivisible_area_number_u = off_areas_pixels[upper_node_num]
            if indivisible_area_number_u != indivisible_area_number_l:
                nodes_to_move = off_areas_sets.pop(indivisible_area_number_u)
                for node in nodes_to_move:
                    off_areas_pixels[node] = indivisible_area_number_l
                off_areas_sets[indivisible_area_number_l].update(nodes_to_move)
            off_areas_pixels[node_num] = indivisible_area_number_l
            off_areas_sets[indivisible_area_number_l].add(node_num)
        else:
            off_areas_pixels[node_num] = indivisible_area_number_l
            off_areas_sets[indivisible_area_number_l].add(node_num)
    elif y > 0 and get_pixel_type(image[y - 1][x]) == OFF_AREA:
        upper_node_num = count_node_number(x, y - 1, image)
        indivisible_area_number = off_areas_pixels[upper_node_num]
        off_areas_pixels[node_num] = indivisible_area_number
        off_areas_sets[indivisible_area_number].add(node_num)
    else:
        off_areas_sets[off_area_number] = {node_num}
        off_areas_pixels[node_num] = off_area_number
        off_area_number += 1
    return off_area_number


def handle_area(x, y, image, pixel_type, areas_map, areas, node_num, initial_area_number):
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


def print_progress(node_num, number_of_vertices, show):
    if show and node_num % 10000 == 0:
        print("conversion progress: " + str(round(node_num * 100 / number_of_vertices)) + "%")


def convert_image_to_graph_2(path, show_progress):
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
            print_progress(node_num, number_of_vertices, show_progress)
            pixel_type = get_pixel_type(image[y][x])
            G.add_node(node_num, data={'type': pixel_type, 'x': x, 'y': y, 'num': node_num, 'lvl': 0, 'weight': 1})
            if x > 0:
                G.add_edge(y * image.shape[1] + x - 1, node_num, w=1)
            if y > 0:
                G.add_edge((y - 1) * image.shape[1] + x, node_num, w=1)
            if pixel_type != NORMAL_AREA:
                initial_area_number = handle_area(x, y, image, pixel_type, areas_map, areas, node_num,
                                                  initial_area_number)
    if show_progress:
        print("conversion finished: 100%")
    return G, areas, image.shape[0] * image.shape[1], image.shape[0], image.shape[1],


def count_node_number(x, y, image):
    return y * image.shape[1] + x


def convert_image_to_graph_off_weighted_0(path, show_progress):
    image = cv2.imread(path)
    image_shape = (image.shape[0], image.shape[1])
    number_of_vertices = image.shape[0] * image.shape[1]
    indivisible_area_number = 0
    indivisible_areas_pixels = {}
    indivisible_areas_sets = {}
    off_area_number = 0
    off_areas_pixels = {}
    off_areas_sets = {}
    G = nx.Graph(shape=image_shape)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            node_num = count_node_number(x, y, image)
            print_progress(node_num, number_of_vertices, show_progress)
            pixel_type = get_pixel_type(image[y][x])
            if pixel_type == OFF_AREA:
                weight = 0
            else:
                weight = 1
            G.add_node(node_num, data={'type': pixel_type, 'x': x, 'y': y, 'num': node_num, 'lvl': 0, 'weight': weight})
            if x > 0:
                G.add_edge(y * image.shape[1] + x - 1, node_num, w=1)
            if y > 0:
                G.add_edge((y - 1) * image.shape[1] + x, node_num, w=1)
            if pixel_type == INDIVISIBLE_AREA:
                indivisible_area_number = handle_indivisible_area(x, y, image, indivisible_areas_sets,
                                                                  indivisible_areas_pixels, node_num,
                                                                  indivisible_area_number)
            if pixel_type == OFF_AREA:
                off_area_number = handle_off_area(x, y, image, off_areas_sets,
                                                  off_areas_pixels, node_num,
                                                  off_area_number)

    if show_progress:
        print("conversion finished: 100%")
    return G, indivisible_areas_sets, off_areas_sets, image.shape[0] * image.shape[1], image.shape[0], image.shape[1],


def convert_image_to_graph_off_removed(path, show_progress):
    image = cv2.imread(path)
    image_shape = (image.shape[0], image.shape[1])
    number_of_vertices = image.shape[0] * image.shape[1]
    indivisible_area_number = 0
    indivisible_areas_pixels = {}
    indivisible_areas_sets = {}
    off_areas_sets = {}
    G = nx.Graph(shape=image_shape)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            node_num = count_node_number(x, y, image)
            print_progress(node_num, number_of_vertices, show_progress)
            pixel_type = get_pixel_type(image[y][x])
            if pixel_type != OFF_AREA:
                G.add_node(node_num,
                           data={'type': pixel_type, 'x': x, 'y': y, 'num': node_num, 'lvl': 0, 'weight': 1})
                if x > 0 and get_pixel_type(image[y][x - 1]) != OFF_AREA:
                    G.add_edge(y * image.shape[1] + x - 1, node_num, w=1)
                if y > 0 and get_pixel_type(image[y - 1][x]) != OFF_AREA:
                    G.add_edge((y - 1) * image.shape[1] + x, node_num, w=1)
                if pixel_type == INDIVISIBLE_AREA:
                    indivisible_area_number = handle_indivisible_area(x, y, image, indivisible_areas_sets,
                                                                      indivisible_areas_pixels, node_num,
                                                                      indivisible_area_number)

    if show_progress:
        print("conversion finished: 100%")
    return G, indivisible_areas_sets, off_areas_sets, image.shape[0] * image.shape[1], image.shape[0], image.shape[1],
