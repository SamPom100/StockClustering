from database import *
import networkx as nx
import matplotlib.pyplot as plt
import webbrowser
from pyvis.network import Network

#https://github.com/simonlindgren/nXd3/tree/master

import community

database = DataBase()

seen_stocks = database.get_indexed_similar_tickers()

G = nx.Graph(useDot=True)

for stock in seen_stocks:
    G.add_node(stock)
    similar_stocks = database.get_similar(stock)
    for similar_stock in similar_stocks:
        index = similar_stocks.index(similar_stock)
        if index < 5:
            G.add_edge(stock, similar_stock)

partition = community.best_partition(G, resolution=20)

subgraphs = {}
for node, part in partition.items():
    if part not in subgraphs:
        subgraphs[part] = nx.Graph()
    subgraphs[part].add_node(node)

for edge in G.edges():
    part1 = partition[edge[0]]
    part2 = partition[edge[1]]
    if part1 == part2:
        subgraphs[part1].add_edge(edge[0], edge[1])

combined_graph = nx.Graph()

#construct the MST in each subgraph
# for subgraph in subgraphs.values():
#     mst = nx.minimum_spanning_tree(subgraph)
#     combined_graph = nx.compose(combined_graph, mst)

for subgraph in subgraphs.values():
    combined_graph = nx.compose(combined_graph, subgraph)

for node in combined_graph.nodes():
    combined_graph.nodes[node]['color'] = partition[node]
    combined_graph.nodes[node]['size'] = combined_graph.degree(node) * 2.5

net = Network(bgcolor="#222222", font_color="white", height="100rem", width="100%")
net.from_nx(combined_graph)
net.toggle_physics(True)
net.toggle_drag_nodes(True)
net.toggle_hide_edges_on_drag(True)

#net.save_graph("index2.html")
nodes, edges, heading, height, width, options = net.get_network_data()

tmp_dict = {"nodes": nodes, "edges": edges}
with open("graph.json", "w") as f:
    json.dump(tmp_dict, f)