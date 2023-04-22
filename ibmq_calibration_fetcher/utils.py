import pygraphviz as pgv
import pandas as pd
import numpy as np
import re

# For the whole table:

def make_df_row(row):
    cells = row.find_all("td")
    return list(map(lambda c: c.text.strip(), cells))

# For the last two columns:

def edge_list_text_to_dict(text):
    result = {}
    try:
        text = re.sub("\s+", " ", text)
        text = re.sub(": ", ":", text)
        edge_value_pairs = list(map(lambda p: p.split(":"), text.split(" ")))
        for edge, value in edge_value_pairs:
            from_vertex, to_vertex = edge.split("_")
            to_vertex = int(to_vertex)
            result[to_vertex] = float(value)
        return result
    except ValueError:
        # print(text)
        return {}

def edge_text_column_to_graph(values, name):
    result = {}
    for i, text in enumerate(values):
        result[i] = edge_list_text_to_dict(text)
    return result

def edge_text_column_to_graphviz_graph(column):
    graph = edge_text_column_to_graph(column.values, column.name)

    G = pgv.AGraph(name=column.name, directed=True)
    for from_vertex, to_vertex_map in graph.items():
        G.add_node(from_vertex)

        for to_vertex, value in to_vertex_map.items():
            value_map={}
            value_map[column.name] = value
            G.add_edge(from_vertex, to_vertex, **value_map)

    return G
