from misc.directed_graph import DirectedGraph
from modelling.notation import Node, Edge, ExclusiveEdge, StartEvent, EndEvent, Task, ExclusiveGateway, ParallelGateway

# class LabeledAdjacencyMatrix:
#     def __init__(self, labels):
#         self.labels = labels
#         self.size = len(labels)
#         self.matrix = [[0 for _ in range(self.size)] for _ in range(self.size)]

#     def _get_index(self, label):
#         return self.labels.index(label)

#     def add_edge(self, label1, label2, weight=1):
#         i, j = self._get_index(label1), self._get_index(label2)
#         self.matrix[i][j] = weight

#     def remove_edge(self, label1, label2):
#         i, j = self._get_index(label1), self._get_index(label2)
#         self.matrix[i][j] = 0

#     def has_edge(self, label1, label2):
#         i, j = self._get_index(label1), self._get_index(label2)
#         return self.matrix[i][j] != 0

#     def get_target_nodes(self, label):
#         i = self._get_index(label)
#         return [self.labels[j] for j in range(self.size) if self.matrix[i][j] != 0]
    
#     def get_target_nodes_with_condition(self, label):
#         i = self._get_index(label)
#         return {self.labels[j]: self.matrix[i][j] for j in range(self.size) if self.matrix[i][j] != 0}

#     def display(self):
#         print(' ', ' '.join(self.labels))
#         for label, row in zip(self.labels, self.matrix):
#             print(label, row)


class ModelGenerator:
    def __init__(self):
        self.edges = []
        self.graph = {}

    def start_event(self, name='Start'):
        start_event = StartEvent(name)
        # self.nodes.append(start_event)
        return start_event

    def end_event(self, name='End'):
        end_event = EndEvent(name)
        # self.nodes.append(end_event)
        return end_event

    def task(self, name:str):
        task = Task(name)
        # self.nodes.append(task)
        return task

    def exclusive_gateway(self, name:str):
        exclusive_gateway = ExclusiveGateway(name)
        # self.nodes.append(exclusive_gateway)
        return exclusive_gateway

    def parallel_gateway(self, name:str):
        parallel_gateway = ParallelGateway(name)
        # self.nodes.append(parallel_gateway)
        return parallel_gateway
    
    def _add_nodes_to_graph(self, origin:Node, target:Node, condition:str=None):
        if condition == None:
            target = (target, None)
        else:
            target = (target, condition)

        if origin not in self.graph:
            self.graph[origin] = [target]
        else:
            self.graph[origin].append(target)

    def get_target_nodes(self, origin:Node):
        return [target for target, _ in self.graph[origin]]
    
    def get_target_nodes_with_condition(self, origin:Node):
        return {target: condition for target, condition in self.graph[origin]}
    
    def get_start_node(self):
        for edge in self.edges:
            if isinstance(edge.origin, StartEvent):
                return edge.origin
                break

    def create_edge(self, origin:Node, target:Node):
        edge = Edge(origin, target)
        self.edges.append(edge)
        self._add_nodes_to_graph(origin, target)

    def create_exclusive_edge(self, origin:Node, target:Node, condition:str):
        edge = ExclusiveEdge(origin, target, condition)
        self.edges.append(edge)
        self._add_nodes_to_graph(origin, target, condition)

    def display_graph(self):
        graph = DirectedGraph()

        for edge in self.edges:
            if isinstance(edge, ExclusiveEdge):
                graph.add_edge(edge.origin.name, edge.target.name, edge.condition)
            elif isinstance(edge, Edge):
                graph.add_edge(edge.origin.name, edge.target.name)
        
        graph.display()

    def get_iterable_graph(self) -> dict:
        graph_dict = {}

        for edge in self.edges:
            if isinstance(edge, ExclusiveEdge):
                if edge.start.name not in graph_dict:
                    graph_dict[edge.start.name] = [(edge.end.name, edge.condition)]
                else:
                    graph_dict[edge.start.name].append((edge.end.name, edge.condition))
            elif isinstance(edge, Edge):
                if edge.start.name not in graph_dict:
                    graph_dict[edge.start.name] = [(edge.end.name, 'empty')]
                else:
                    graph_dict[edge.start.name].append((edge.end.name, 'empty'))

        return graph_dict





