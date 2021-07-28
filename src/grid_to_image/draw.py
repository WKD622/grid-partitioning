import random

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.pyplot import figure

from src.definitions import colors_for_partitions
from src.grid_to_image.helpers import get_color


def plot_legend(plt, partitions_colors, partitions_stats, grid_size):
    legend_elements = []
    print(partitions_stats)
    print(partitions_colors)
    for partition_number, partition_color in partitions_colors.items():
        print(partition_number)
        legend_elements.append(Line2D([0], [0], marker='s', color='w',
                                      label='Partition {}, w={}, %a={:.2f}%'.format(partition_number,
                                                                                     partitions_stats[partition_number],
                                                                                     round(partitions_stats[
                                                                                               partition_number] / grid_size * 100, 2)
                                                                                     , 4),
                                      markerfacecolor=partition_color, markersize=15))
    fig, ax = plt.subplots()
    ax.axis('off')
    fig.set_figheight(5)
    fig.set_figwidth(5)
    ax.legend(handles=legend_elements, loc='best')


def plot(X, y, colors, s, G, name, fig_size=(3, 3), save=False, title='', partitions_colors={}, partitions_stats={},
         grid_size=0):
    figure(figsize=fig_size)
    for i in range(len(X)):
        plt.scatter(X[i], y[i], color=colors[i], marker="s", s=s)
    plt.gca().invert_yaxis()
    plt.axis('off')
    if title:
        plt.title(title)
    else:
        plt.tight_layout()
    plt.xlim(0, G.graph['shape'][1] - 1)
    plt.ylim(G.graph['shape'][0] - 1, 0)
    if save:
        plt.savefig("out/" + name + '.png')
    else:
        if len(partitions_colors):
            plot_legend(plt, partitions_colors, partitions_stats, grid_size)
        plt.show(pad_inches=0)
    plt.clf()


def convert_graph_to_image(G, p, s, vertical_size, horizontal_size, name):
    X = []
    y = []
    colors = []
    nodes = sorted(G.nodes)

    for node_num in nodes:
        node = G.nodes[node_num]
        X.append(G.nodes[node_num]['data']['x'])
        y.append(G.nodes[node_num]['data']['y'])
        colors.append(get_color(node['data']['type']))

    fig_size = compute_fig_size(horizontal_size, vertical_size)
    plot(X=X, y=y, colors=colors, s=s, G=G, name=name, fig_size=fig_size)


def optimized_convert_graph_to_image_2(G, indivisible_areas, off_areas, p, s, vertical_size, horizontal_size, name,
                                       base_size=5):
    X = []
    y = []
    colors = []

    for area_number, nodes in off_areas.items():
        for node in nodes:
            if random.uniform(0, 1) < p:
                X.append(G.nodes[node]['data']['x'])
                y.append(G.nodes[node]['data']['y'])
                colors.append(get_color(G.nodes[node]['data']['type']))

    for area_number, nodes in indivisible_areas.items():
        for node in nodes:
            if random.uniform(0, 1) < p:
                X.append(G.nodes[node]['data']['x'])
                y.append(G.nodes[node]['data']['y'])
                colors.append(get_color(G.nodes[node]['data']['type']))

    fig_size = compute_fig_size(horizontal_size, vertical_size, base_size=base_size)
    plot(X=X, y=y, colors=colors, s=s, G=G, name=name, fig_size=fig_size)


def draw_a_color():
    return "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])


def draw_partitions_colors(number_of_colors):
    return [draw_a_color() for i in range(number_of_colors)]


def compute_fig_size(horizontal_size, vertical_size, base_size=3):
    if horizontal_size > vertical_size:
        size_y = base_size
        size_x = horizontal_size * base_size / vertical_size
    else:
        size_y = vertical_size * base_size / horizontal_size
        size_x = base_size
    return size_x, size_y


def choose_colors_for_partitions(partitions_numbers, number_of_partitions):
    if number_of_partitions > len(colors_for_partitions):
        colors = draw_partitions_colors(2500)
    else:
        colors = colors_for_partitions
    partitions_colors = {}
    for partition_number in partitions_numbers:
        partitions_colors[partition_number] = colors[partition_number]
    return partitions_colors


def convert_partitioned_graph_to_image(G, p, s, number_of_partitions, partitions, partitions_vertices, partitions_stats,
                                       grid_size, name, vertical_size, horizontal_size, save=False, title='',
                                       base_size=5):
    partitions_colors = choose_colors_for_partitions(partitions_vertices.keys(), number_of_partitions)
    X = []
    y = []
    colors = []
    for node in G.nodes:
        if random.uniform(0, 1) < p:
            X.append(G.nodes[node]['data']['x'])
            y.append(G.nodes[node]['data']['y'])
            colors.append(partitions_colors[partitions[node]])
    fig_size = compute_fig_size(horizontal_size, vertical_size, base_size)
    plot(X, y, colors, s, G, name, fig_size, save, title, partitions_colors=partitions_colors,
         partitions_stats=partitions_stats, grid_size=grid_size)
