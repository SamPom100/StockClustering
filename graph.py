from database import *
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import community

database = DataBase()

def generate_graph(seen_stocks, filename):
    G = nx.Graph(useDot=True)

    for stock in seen_stocks:
        G.add_node(stock)
        similar_stocks = database.get_similar(stock)
        for similar_stock in similar_stocks:
            similarity_score = database.similar_score(stock, similar_stock) / 3
            if similarity_score <= 1:
                weight = 0.01
            elif similarity_score <= 2:
                weight = 0.05
            elif similarity_score <= 3:
                weight = 0.2
            elif similarity_score <= 4:
                weight = 0.8
            elif similarity_score <= 5:
                weight = 1.5
            else:
                weight = 3
            G.add_edge(stock, similar_stock, weight=weight)

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
            subgraphs[part1].add_edge(edge[0], edge[1], weight=G.edges[edge]['weight'])

    combined_graph = nx.Graph()

    for subgraph in subgraphs.values():
        combined_graph = nx.compose(combined_graph, subgraph)

    for node in combined_graph.nodes():
        combined_graph.nodes[node]['color'] = partition[node]
        #combined_graph.nodes[node]['size'] = combined_graph.degree(node) * 0.8
        combined_graph.nodes[node]['size'] = 0.7*sum([combined_graph.edges[edge]['weight'] for edge in combined_graph.edges(node)])

    net = Network(bgcolor="#222222", font_color="white", height="100rem", width="100%")
    net.from_nx(combined_graph)
    nodes, edges, heading, height, width, options = net.get_network_data()

    tmp_dict = {"nodes": nodes, "edges": edges}
    with open(filename, "w") as f:
        json.dump(tmp_dict, f)

    print("EXPORTED ", filename)

if __name__ == "__main__":
    seen_stocks = database.get_indexed_similar_tickers()
    generate_graph(seen_stocks, "graph.json")

    seen_stocks = seen_stocks[:30]
    generate_graph(seen_stocks, "graph_mobile.json")