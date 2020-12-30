import random

import matplotlib.pyplot as plt

from src.definitions import NORMAL_AREA, INDIVISIBLE_AREA, OFF_AREA
from src.grid_to_image.helpers import get_color


def plot(X, y, colors, s, G):
    for i in range(len(X)):
        plt.scatter(X[i], y[i], color=colors[i], marker="s", s=s)
    plt.gca().invert_yaxis()
    plt.axis('off')
    plt.tight_layout()
    plt.xlim(0, G.graph['shape'][1] - 1)
    plt.ylim(G.graph['shape'][0] - 1, 0)
    plt.show(pad_inches=0)


def convert_graph_to_image(G, p, s):
    print("drawing initial grid...")
    X = []
    y = []
    colors = []
    nodes = sorted(G.nodes)

    for node_num in nodes:
        node = G.nodes[node_num]
        if node['data']['type'] != NORMAL_AREA and random.uniform(0, 1) < p:
            X.append(G.nodes[node]['data']['x'])
            y.append(G.nodes[node]['data']['y'])
            colors.append('#%02x%02x%02x' % get_color(G.nodes[node]['data']['type'])[::-1])

    plot(X, y, colors, s, G)


def optimized_convert_graph_to_image_2(G, areas, p, s):
    print("drawing initial grid...")
    X = []
    y = []
    colors = []

    for area_number, nodes in areas[OFF_AREA].items():
        for node in nodes:
            if random.uniform(0, 1) < p:
                X.append(G.nodes[node]['data']['x'])
                y.append(G.nodes[node]['data']['y'])
                colors.append('#%02x%02x%02x' % get_color(G.nodes[node]['data']['type'])[::-1])

    for area_number, nodes in areas[INDIVISIBLE_AREA].items():
        for node in nodes:
            if random.uniform(0, 1) < p:
                X.append(G.nodes[node]['data']['x'])
                y.append(G.nodes[node]['data']['y'])
                colors.append('#%02x%02x%02x' % get_color(G.nodes[node]['data']['type'])[::-1])

    plot(X, y, colors, s, G)
