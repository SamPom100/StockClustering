from database import *
import networkx as nx
import matplotlib.pyplot as plt
import webbrowser
from pyvis.network import Network

import community

database = DataBase()

limit_size = False
seen_stocks = database.get_indexed_similar_tickers()
if limit_size:
    seen_stocks = seen_stocks[:50]

G = nx.Graph()

for stock in seen_stocks:
    G.add_node(stock)
    similar_stocks = database.get_similar(stock)
    for similar_stock in similar_stocks:
        index = similar_stocks.index(similar_stock)
        if index > 3:
            G.add_edge(stock, similar_stock)

partition = community.best_partition(G, resolution=4)

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

for subgraph in subgraphs.values():
    combined_graph = nx.compose(combined_graph, subgraph)

for node in combined_graph.nodes():
    combined_graph.nodes[node]['color'] = partition[node]
    combined_graph.nodes[node]['size'] = combined_graph.degree(node) * 1.5

#nx.draw(combined_graph, with_labels=True)
#plt.show()

net = Network(bgcolor="#222222", font_color="white", height="1000px", width="1500px")
net.from_nx(combined_graph)
net.toggle_physics(False)
net.toggle_drag_nodes(False)

net.show_buttons(filter_=['physics'])

net.save_graph("graph.html")
webbrowser.open("file:///Users/sampomerantz/Documents/GitHub/StockClustering/graph.html")


#save networkx in DOT format
nx.nx_pydot.write_dot(combined_graph, "graph.dot")
