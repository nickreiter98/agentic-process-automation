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
    def __init__(self):
        super().__init__('O')

class Edge:
    def __init__(self, origin:Node, target:Node):
        self.origin = origin
        self.target = target

class ExclusiveEdge(Edge):
    def __init__(self, origin:Node, target:Node, condition:str):
        super().__init__(origin, target)
        self.condition = condition
