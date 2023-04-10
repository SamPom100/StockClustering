from database import *
import networkx as nx
import matplotlib.pyplot as plt
import webbrowser

database = DataBase()

seen_stocks = database.seen_stocks()

#make a graph of the stocks, and each stock has a list of similar stocks

G = nx.Graph()

for stock in seen_stocks:
    G.add_node(stock)
    similar_stocks = database.get_stock(stock)
    for similar_stock in similar_stocks:
        G.add_node(similar_stock)
        G.add_edge(stock, similar_stock)

#draw with PyVis
from pyvis.network import Network
net = Network(notebook=False)
net.from_nx(G)
net.show_buttons()
net.save_graph("graph.html")
webbrowser.open("file:///Users/sampomerantz/Documents/GitHub/StockClustering/graph.html")
