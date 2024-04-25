from misc.directed_graph import DirectedGraph
from modelling.notation import Node, Edge, ExclusiveEdge, StartEvent, EndEvent, Task, ExclusiveGateway, ParallelGateway

import pm4py.objects.bpmn.obj as bpmn_obj
from pm4py.visualization.bpmn import visualizer

class ModelGenerator:
    def __init__(self):
        self.bpmn = bpmn_obj.BPMN()
        self.graph = {}

    def create_start_event(self, name='Start'):
        start_event = self.bpmn.StartEvent(name=name)
        self.bpmn.add_node(start_event)
        return start_event

    def create_end_event(self, name='End'):
        end_event = self.bpmn.EndEvent(name=name)
        self.bpmn.add_node(end_event)
        return end_event

    def create_task(self, name:str):
        task = self.bpmn.Task(name=name)
        self.bpmn.add_node(task)
        return task

    def create_exclusive_gateway(self, name:str):
        exclusive_gateway = self.bpmn.ExclusiveGateway(name=name, gateway_direction='diverging')
        self.bpmn.add_node(exclusive_gateway)
        return exclusive_gateway

    def create_parallel_gateway(self, name:str):
        parallel_gateway = self.bpmn.ParallelGateway(name='X')
        self.bpmn.add_node(parallel_gateway)
        return parallel_gateway

    def create_edge(self, source:Node, target:Node):
        edge = self.bpmn.Flow(source=source, target=target)
        self.bpmn.add_flow(edge)
        return edge

    def create_exclusive_edge(self, source:Node, target:Node, condition:str):
        edge = self.bpmn.Flow(source=source, target=target, name=condition)
        self.bpmn.add_flow(edge)
        return edge
    
    def is_start_event(self, node):
        return isinstance(node, self.bpmn.StartEvent)
    
    def is_end_event(self, node):
        return isinstance(node, self.bpmn.EndEvent)
    
    def is_task(self, node):
        return isinstance(node, self.bpmn.Task)
    
    def is_exclusive_gateway(self, node):
        return isinstance(node, self.bpmn.ExclusiveGateway)
    
    def is_parallel_gateway(self, node):
        return isinstance(node, self.bpmn.ParallelGateway)

    # def get_target_nodes(self, origin:Node):
    #     return [target for target, _ in self.graph[origin]]
    
    # def get_target_nodes_with_condition(self, origin:Node):
    #     return {target: condition for target, condition in self.graph[origin]}
    
    def get_start_node(self):
        for node in self.bpmn.get_nodes():
            if isinstance(node, self.bpmn.StartEvent):
                return node.get_name()

    def get_graph(self):
        return self.bpmn.get_graph()

    def view_bpmn(self):
        gviz = visualizer.apply(self.bpmn)
        visualizer.matplotlib_view(gviz)

    def save_bpmn(self):
        gviz = visualizer.apply(self.bpmn)
        visualizer.save(gviz, 'model.gviz')

    





