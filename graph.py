#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Mustafa Durmuş [mustafa.durmus@albert.health]

import networkx as nx
import matplotlib.pyplot as plt


def display_dict(x):

    G = nx.DiGraph()

    for key, value in x.items():
        for v in value:
            G.add_edge(key, v)


    nx.draw(G, with_labels=True, node_size=[4000, 4000, 4000, 4000, 4000, 4000, 4000])
    plt.show()


def dict_2_graph(x, ranks):
    # pagerank değerlerini yüzdelik olarak gösterelim.
    sorted_percentage_list = []
    for key,value in sorted(ranks.items()):
        sorted_percentage_list.append(round(value * 100, 2))

    # node ve edge'leri liste olarak tut.
    node_list = [key for key in sorted(x.keys())]
    edge_list = []
    for key, value in sorted(x.items()):
        for v in value:
            edge_list.append((key, v))

    # node isimleri ve yüzdeliklerini label olarak ata.
    label_list = {}
    for idx, node in enumerate(node_list):
        label_list[str(node)] = f'{node}\n%{sorted_percentage_list[idx]}'

    # düğümlerin boyutları daha da belli olsun diye 500 ile çarp.
    node_size_list = list(map(lambda y: y * 1000, sorted_percentage_list))

    # göster
    G = nx.DiGraph()
    G.add_nodes_from(node_list)
    G.add_edges_from(edge_list)
    nx.draw(G, labels=label_list, with_labels=True, node_size=node_size_list)
    plt.show()
