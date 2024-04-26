import networkx as nx
import pm4py.objects.bpmn.obj as bpmn_obj

from pm4py.visualization.bpmn import visualizer
from pm4py.objects.bpmn.obj import BPMN

# Define type hints
from typing import List, Tuple, TypeAlias
StartEvent: TypeAlias = BPMN.StartEvent
EndEvent: TypeAlias = BPMN.EndEvent
Task: TypeAlias = BPMN.Task
ExclusiveGateway: TypeAlias = BPMN.ExclusiveGateway
ParallelGateway: TypeAlias = BPMN.ParallelGateway
Node: TypeAlias = BPMN.BPMNNode
Edge: TypeAlias = BPMN.Flow


class ModelGenerator:
    def __init__(self):
        self.bpmn = bpmn_obj.BPMN()
        self.graph = {}

    def create_start_event(self, name:str='Start') -> StartEvent:
        start_event = self.bpmn.StartEvent(name=name)
        self.bpmn.add_node(start_event)
        return start_event

    def create_end_event(self, name:str='End') -> EndEvent:
        end_event = self.bpmn.EndEvent(name=name)
        self.bpmn.add_node(end_event)
        return end_event

    def create_task(self, name:str) -> Task:
        task = self.bpmn.Task(name=name)
        self.bpmn.add_node(task)
        return task

    def create_exclusive_gateway(self, name:str) -> ExclusiveGateway:
        exclusive_gateway = self.bpmn.ExclusiveGateway(name=name, gateway_direction='diverging')
        self.bpmn.add_node(exclusive_gateway)
        return exclusive_gateway

    def create_parallel_gateway(self, name:str) -> ParallelGateway:
        parallel_gateway = self.bpmn.ParallelGateway(name='X', gateway_direction='diverging')
        self.bpmn.add_node(parallel_gateway)
        return parallel_gateway

    def create_edge(self, source:Node, target:Node) -> Edge:
        edge = self.bpmn.Flow(source=source, target=target)
        self.bpmn.add_flow(edge)
        return edge

    def create_exclusive_edge(self, source:Node, target:Node, condition:str) -> Edge:
        edge = self.bpmn.Flow(source=source, target=target, name=condition)
        self.bpmn.add_flow(edge)
        return edge

    def get_as_adjacent_dict(self):
        graph = self.bpmn.get_graph()
        graph = nx.to_dict_of_dicts(graph)
        return AdjacentDict(graph)

    def view_bpmn(self) -> None:
        gviz = visualizer.apply(self.bpmn)
        visualizer.matplotlib_view(gviz)

    def save_bpmn(self) -> None:
        gviz = visualizer.apply(self.bpmn)
        visualizer.save(gviz, 'model.gviz')

class AdjacentDict:
    def __init__(self, graph):
        self.graph = graph
    
    def get_start_node(self) -> StartEvent:
        for node in self.graph:
            if isinstance(node, StartEvent):
                return node
            
    def is_start_event(self, node:StartEvent) -> bool:
        return isinstance(node, StartEvent)
    
    def is_end_event(self, node:EndEvent) -> bool:
        return isinstance(node, EndEvent)
    
    def is_task(self, node:Task) -> bool:
        return isinstance(node, Task)
    
    def is_exclusive_gateway(self, node:ExclusiveGateway) -> bool:
        return isinstance(node, ExclusiveGateway)
    
    def is_parallel_gateway(self, node:ParallelGateway) -> bool:
        return isinstance(node, ParallelGateway)
    
    def get_target_node(self, source:Node) -> Node:
        if len(self.graph[source]) > 1:
            raise Exception('Multiple targets for source node')
        return list(self.graph[source].keys())[0]
    
    def get_target_nodes(self, source:ExclusiveGateway|ParallelGateway) -> List[Tuple[Node, str]]:
        if len(self.graph[source]) < 2:
            raise Exception('Too few targets for source node')
        return [(target, self.graph[source][target][0]['name']) for target in self.graph[source]]
                
                

        





