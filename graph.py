from database import *
import networkx as nx
import matplotlib.pyplot as plt
import webbrowser

database = DataBase()

seen_stocks = database.get_indexed_similar_tickers()

G = nx.Graph()

for stock in seen_stocks:
    G.add_node(stock)
    similar_stocks = database.get_similar(stock)
    for similar_stock in similar_stocks:
        G.add_node(similar_stock)
        G.add_edge(stock, similar_stock)

from pyvis.network import Network

net = Network(notebook=False, neighborhood_highlight=True)
net.from_nx(G)
net.toggle_physics(False)
"""
:param gravity: The more negative the gravity value is, the stronger the
                repulsion is.
:param central_gravity: The gravity attractor to pull the entire network
                        to the center. 
:param spring_length: The rest length of the edges
:param spring_strength: The strong the edges springs are
:param damping: A value ranging from 0 to 1 of how much of the velocity
                from the previous physics simulation iteration carries
                over to the next iteration.
:param overlap: When larger than 0, the size of the node is taken into
                account. The distance will be calculated from the radius
                of the encompassing circle of the node for both the
                gravity model. Value 1 is maximum overlap avoidance.
"""
net.barnes_hut(
            gravity=1000,
            central_gravity=0,
            spring_length=100,
            spring_strength=0.1,
            damping=0.05,
            overlap=1
    )
net.show_buttons()
net.save_graph('graph.html')

webbrowser.open("file:///Users/sampomerantz/Documents/GitHub/StockClustering/graph.html")
