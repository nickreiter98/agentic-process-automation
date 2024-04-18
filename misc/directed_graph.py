import networkx as nx
import matplotlib.pyplot as plt

class DirectedGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_edge(self, start, end, weight='empty'):
        if weight == 'empty':
            self.graph.add_edge(start, end)
        else:
            self.graph.add_edge(start, end, weight=weight)

    def display(self):
        pos = nx.circular_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_color='skyblue', node_size=2000, edge_color='k', width=2, arrowstyle='-|>', arrowsize=10)
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)
        plt.show()