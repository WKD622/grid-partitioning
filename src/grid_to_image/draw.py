import random

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

from src.definitions import NORMAL_AREA, INDIVISIBLE_AREA, OFF_AREA, colors_for_partitions
from src.grid_to_image.helpers import get_color


def plot(X, y, colors, s, G, name, save=False):
    figure(figsize=(3, 3))
    for i in range(len(X)):
        plt.scatter(X[i], y[i], color=colors[i], marker="s", s=s)
    plt.gca().invert_yaxis()
    plt.axis('off')
    plt.tight_layout()
    plt.xlim(0, G.graph['shape'][1] - 1)
    plt.ylim(G.graph['shape'][0] - 1, 0)
    if save:
        plt.savefig("out/" + name + '.png')
    else:
        plt.show(pad_inches=0)
    plt.clf()


def convert_graph_to_image(G, p, s, name):
    X = []
    y = []
    colors = []
    nodes = sorted(G.nodes)

    for node_num in nodes:
        node = G.nodes[node_num]
        if node['data']['type'] != NORMAL_AREA and random.uniform(0, 1) < p:
            X.append(G.nodes[node]['data']['x'])
            y.append(G.nodes[node]['data']['y'])
            colors.append(get_color(G.nodes[node]['data']['type']))

    plot(X, y, colors, s, G, name)


def optimized_convert_graph_to_image_2(G, areas, p, s, name):
    X = []
    y = []
    colors = []

    for area_number, nodes in areas[OFF_AREA].items():
        for node in nodes:
            if random.uniform(0, 1) < p:
                X.append(G.nodes[node]['data']['x'])
                y.append(G.nodes[node]['data']['y'])
                colors.append(get_color(G.nodes[node]['data']['type']))

    for area_number, nodes in areas[INDIVISIBLE_AREA].items():
        for node in nodes:
            if random.uniform(0, 1) < p:
                X.append(G.nodes[node]['data']['x'])
                y.append(G.nodes[node]['data']['y'])
                colors.append(get_color(G.nodes[node]['data']['type']))

    plot(X, y, colors, s, G, name)


def draw_a_color():
    return "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])


def draw_partitions_colors(number_of_colors):
    return [draw_a_color() for i in range(number_of_colors)]


def convert_partitioned_graph_to_image(G, p, s, number_of_partitions, name, save=False):
    X = []
    y = []
    colors = []
    if number_of_partitions > len(colors_for_partitions):
        partitions_colors = draw_partitions_colors(len(G.nodes))
    else:
        partitions_colors = colors_for_partitions

    for node in G.nodes:
        if random.uniform(0, 1) < p:
            X.append(G.nodes[node]['data']['x'])
            y.append(G.nodes[node]['data']['y'])
            colors.append(partitions_colors[G.nodes[node]['data']['partition']])

    plot(X, y, colors, s, G, name, save)
