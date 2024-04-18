class Node:
    def __init__(self, name:str):
        self.name = name

class StartEvent(Node):
    def __init__(self, name:str):
        super().__init__(name)

class EndEvent(Node):
    def __init__(self, name:str):
        super().__init__(name)

class Task(Node):
    def __init__(self, name:str):
        super().__init__(name)

class ExclusiveGateway(Node):
    def __init__(self, name:str):
        super().__init__(name)

class ParallelGateway(Node):
    def __init__(self, name:str):
        super().__init__(name)

class Edge:
    def __init__(self, start:Node, end:Node):
        self.start = start
        self.end = end

class ExclusiveEdge(Edge):
    def __init__(self, start:Node, end:Node, condition:str):
        super().__init__(start, end)
        self.condition = condition


class ModelGenerator:
    def __init__(self):
        self.edges = []
        self.nodes = []

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

    def create_edge(self, origin:Node, target:Node):
        edge = Edge(origin, target)
        self.edges.append(edge)

    def create_exclusive_edge(self, origin:Node, target:Node, condition:str):
        edge = ExclusiveEdge(origin, target, condition)
        self.edges.append(edge)

