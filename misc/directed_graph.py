import networkx as nx
import matplotlib.pyplot as plt

class DirectedGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_edge(self, start, end):
        self.graph.add_edge(start, end)

    def display(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, arrows=True)
        plt.show()
