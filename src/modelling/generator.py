import logging

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
        self.graph = None

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
        name = f'EXCLUSIVE: {name}'
        exclusive_gateway = self.bpmn.ExclusiveGateway(name=name, gateway_direction='diverging')
        self.bpmn.add_node(exclusive_gateway)
        return exclusive_gateway

    def create_parallel_gateway(self, id:str) -> ParallelGateway:
        name = 'PARALLEL: ' + id
        parallel_gateway = self.bpmn.ParallelGateway(name=name, gateway_direction='diverging')
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

    def get_start_node(self) -> StartEvent|List[StartEvent]:
        start_nodes = [node for node in self.bpmn.get_nodes() if self.is_start_event(node)]
        assert len(start_nodes) != 1 
        return start_nodes[0]
       
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
        out_arcs = source.get_out_arcs()
        return out_arcs[0].target
    
    def get_target_nodes(self, source:ExclusiveGateway|ParallelGateway) -> List[Tuple[Node, str]]:
        out_arcs = source.get_out_arcs()
        return [(out_arc.target, out_arc.get_name()) for out_arc in out_arcs]

    def __str__(self) -> str:
        graph = ''
        for node in self.bpmn.get_nodes():
            if self.is_exclusive_gateway(node):
                for i, (target, condition) in enumerate(self.get_target_nodes(node)):
                    if i == 0:
                        graph += f'{node.name} -> {target.name} [condition="{condition}"]'
                    else:
                        graph += f' & {target.name} [condition="{condition}]'
                    graph += '\n'
            elif self.is_parallel_gateway(node):
                 for i, (target, condition) in enumerate(self.get_target_nodes(node)):
                    if i == 0:
                        graph += f'{node.name} -> {target.name}"'
                    else:
                        graph += f' & {target.name}'
                    graph += '\n'
            elif self.is_end_event(node):
                continue
            else:
                graph += f'{node.name} -> {self.get_target_node(node).name}\n'
        return graph
  
    def initialize(self):
        orig_graph = self.bpmn.get_graph()
        self.graph = nx.to_dict_of_dicts(orig_graph)
        self._check_graph_for_abnormalities()
            
    def _check_graph_for_abnormalities(self):
        logging.info('Checking graph for abnormalities')
        self._check_start()
        for node in self.bpmn.get_graph():
            if self.is_start_event(node) or self.is_task(node):
                self._check_target_node(node)
                self._check_source_nodes(node) 
            elif self.is_end_event(node):
                self._check_source_nodes(node)
            elif self.is_exclusive_gateway(node) or self.is_parallel_gateway:
                self._check_target_nodes(node)
                self._check_source_nodes(node)
        logging.info('Graph is free of abnormalities')

    def _check_start(self) -> None:
        start_nodes = [node for node in self.graph if self.is_start_event(node)]
        if not start_nodes:
            raise Exception('No start node found. Please add a start node')
        elif len(start_nodes) > 1:
            raise Exception('Multiple start nodes found. Please remove all but one start node')
      
    def _check_source_nodes(self, node:Node) -> None:
        if self.is_start_event(node):
            None
        elif (self.is_task(node) or self.is_exclusive_gateway(node) or 
              self.is_parallel_gateway(node) or self.is_end_event(node)):
            if not node.get_in_arcs():
                raise Exception(f'The node "{node.name}" doesnt posses an source node.'
                                ' Please create an edge from a source node to it!')
            elif len(node.get_in_arcs()) > 1:
                raise Exception(f'The node "{node.name}" posses too many source nodes.'
                                ' Please remove all but one edge. Check as well whether'
                                ' node should be a parallel stream!')
            else:
                None

    def _check_target_node(self, source:Node) -> None:
        out_arcs = source.get_out_arcs()
        if len(out_arcs) > 1:
            raise Exception(f'The node "{source.name}" contains multiple target nodes.'
                            ' Please remove all edges but one or check whether'
                            ' the node could be modelled as a parallel/exclusive gateway')
        if len(out_arcs) == 0:
            raise Exception(f'The node "{source.name}" is not connected to a target node.'
                            ' Please create an edge to one target node!')
        
    def _check_target_nodes(self, source:ExclusiveGateway|ParallelGateway) -> None:
        out_arcs = source.get_out_arcs()
        if len(out_arcs) == 1:
            raise Exception(f'Only one target found for node "{source.name}".'
                            ' Add another target node!')
        if len(out_arcs) == 0:
            raise Exception(f'The node "{source.name}" is not connected to a target node.'
                            ' Please connect it at least to two!')
        for arc in out_arcs:
            if self.is_end_event(arc.target):
                raise Exception(f'The node "{source.name}" is connected to an end event.'
                                'Please delete the directly connected end node!')

    def get_as_adjacent_dict(self):
       return self.graph
    
    def get_bpmn(self):
        return visualizer.apply(
            self.bpmn,
            parameters={'format': str('svg').lower()}
        )

    def view_bpmn(self) -> None:
        gviz = visualizer.apply(self.bpmn)
        visualizer.matplotlib_view(gviz)

    def save_bpmn(self) -> None:
        gviz = visualizer.apply(self.bpmn)
        visualizer.save(gviz, 'model.gviz')
                
                

        





