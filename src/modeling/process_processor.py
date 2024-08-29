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


class ProcessProcessor:
    def __init__(self):
        self.bpmn = bpmn_obj.BPMN()
        self.graph = None

    def create_start_event(self, name: str = "Start") -> StartEvent:
        start_event = self.bpmn.StartEvent(name)
        self.bpmn.add_node(start_event)
        return start_event

    def create_end_event(self, name: str = "End") -> EndEvent:
        end_event = self.bpmn.EndEvent(name=name)
        self.bpmn.add_node(end_event)
        return end_event

    def create_task(self, name: str) -> Task:
        task = self.bpmn.Task(name=name)
        self.bpmn.add_node(task)
        return task

    def create_exclusive_gateway(self, name: str) -> ExclusiveGateway:
        name = f"EXCLUSIVE: {name}"
        exclusive_gateway = self.bpmn.ExclusiveGateway(
            name=name, gateway_direction="diverging"
        )
        self.bpmn.add_node(exclusive_gateway)
        return exclusive_gateway

    def create_parallel_gateway(self, id: str) -> ParallelGateway:
        name = "PARALLEL: " + id
        parallel_gateway = self.bpmn.ParallelGateway(
            name=name, gateway_direction="diverging"
        )
        self.bpmn.add_node(parallel_gateway)
        return parallel_gateway

    def create_edge(self, source: Node, target: Node) -> Edge:
        edge = self.bpmn.Flow(source=source, target=target)
        self.bpmn.add_flow(edge)
        return edge

    def create_exclusive_edge(self, source: Node, target: Node, condition: str) -> Edge:
        edge = self.bpmn.Flow(source=source, target=target, name=condition)
        self.bpmn.add_flow(edge)
        return edge

    def get_start_node(self) -> StartEvent | List[StartEvent]:
        start_nodes = [n for n in self.bpmn.get_nodes() if self.is_start_event(n)]
        assert len(start_nodes) == 1
        return start_nodes[0]

    def is_start_event(self, node: StartEvent) -> bool:
        return isinstance(node, StartEvent)

    def is_end_event(self, node: EndEvent) -> bool:
        return isinstance(node, EndEvent)

    def is_task(self, node: Task) -> bool:
        return isinstance(node, Task)

    def is_exclusive_gateway(self, node: ExclusiveGateway) -> bool:
        return isinstance(node, ExclusiveGateway)

    def is_parallel_gateway(self, node: ParallelGateway) -> bool:
        return isinstance(node, ParallelGateway)

    def get_target_node(self, source: Node) -> Node:
        out_arcs = source.get_out_arcs()
        return out_arcs[0].target

    def get_target_nodes(
        self, source: ExclusiveGateway | ParallelGateway
    ) -> List[Tuple[Node, str]]:
        out_arcs = source.get_out_arcs()
        return [(out_arc.target, out_arc.get_name()) for out_arc in out_arcs]

    def __str__(self) -> str:
        graph = ""
        # Iterate over all nodes
        for node in self.bpmn.get_nodes():
            if self.is_exclusive_gateway(node):
                # Pretty print all target nodes with conditions
                for i, (target, condition) in enumerate(self.get_target_nodes(node)):
                    # First target node of the gateway
                    if i == 0:
                        graph += (
                            f"{node.name} -> {target.name} [condition='{condition}']"
                        )
                    # All other target nodes of the gateway
                    else:
                        graph += f" & {target.name} [condition='{condition}']"
                    graph += "\n"
            elif self.is_parallel_gateway(node):
                for i, (target, _) in enumerate(self.get_target_nodes(node)):
                    # First target node of the gateway
                    if i == 0:
                        graph += f"{node.name} -> {target.name}"
                    # All other target nodes of the gateway
                    else:
                        graph += f" & {target.name}"
                    graph += "\n"
            # End events are not pretty printed
            elif self.is_end_event(node):
                continue
            # Start event and tasks
            else:
                graph += f"{node.name} -> {self.get_target_node(node).name}\n"
        return graph

    def initialize(self) -> None:
        """Initialize the model and check for abnormalities.
        """
        # Get the graph representation
        orig_graph = self.bpmn.get_graph()
        # Initalize by transforming the graph to a dictionary of dictionaries
        self.graph = nx.to_dict_of_dicts(orig_graph)
        # Check the graph for abnormalities
        self._check_graph_for_abnormalities()

    def _check_graph_for_abnormalities(self) -> None:
        """Check the graph for abnormalities by iterating every node of the graph.
        Abnormalities are checked by inspecting source and target nodes.
        """
        print("Checking graph for abnormalities")
        self._check_start_node()
        # Iterate over all nodes
        for node in self.bpmn.get_graph():
            if self.is_start_event(node) or self.is_task(node):
                self._check_target_node(node)
                self._check_source_nodes(node)
            elif self.is_end_event(node):
                self._check_source_nodes(node)
            elif self.is_exclusive_gateway(node) or self.is_parallel_gateway:
                self._check_target_nodes(node)
                self._check_source_nodes(node)

    def _check_start_node(self) -> None:
        """Check the start node for abnormalities.
        The abnormality is there must be only one start node.
        If abnormalities found, raise Exception to provide information for
        overlying module.

        :raises Exception: If start_nodes is empty
        :raises Exception: If start_nodes comprises more than one start nodes
        """
        # Store all start nodes in  list
        start_nodes = [node for node in self.graph if self.is_start_event(node)]
        if not start_nodes:
            raise Exception("No start node found. Please add a start node")
        elif len(start_nodes) > 1:
            raise Exception(
                "Multiple start nodes found. Please remove all but one start node"
            )

    # TODO: Add function to check whether predecessor of end event is exclusive or parallel gateway
    def _check_source_nodes(self, node: Node) -> None:
        """Check the source nodes of a given node for abnormalities.
        The abnormality is that a node must always be preceded by only one node.
        If abnormalities found, raise Exception to provide information for
        overlying module.

        :param node: The node to check for abnormalities
        :raises Exception: Node doesnt posses an source node
        :raises Exception: Node posses more than one source nodes
        """
        # Start event was already checked - skip
        if self.is_start_event(node):
            None
        elif (
            self.is_task(node)
            or self.is_exclusive_gateway(node)
            or self.is_parallel_gateway(node)
            or self.is_end_event(node)
        ):
            # get the incoming arcs of the node
            incoming_arcs = node.get_in_arcs()
            if not incoming_arcs:
                raise Exception(
                    f"The node '{node.name}' doesnt posses an source node."
                    " Please create an edge from a source node to it!"
                )
            elif len(incoming_arcs) > 1:
                raise Exception(
                    f"The node '{node.name}' posses too many source nodes."
                    " Please remove all but one edge. Check as well whether"
                    " node might be a parallel stream!"
                )
            else:
                None

    def _check_target_node(self, node: Node) -> None:
        """Check the target node of a given node for abnormalities.
        The abnormality is that a node must always be followed by only one node.
        If abnormalities found, raise Exception to provide information for
        overlying module.

        :param node: Start event and tasks to check for abnormalities 
        :raises Exception: Node posses more than one target node
        :raises Exception: Node doesnt posses a target node
        """
        # Get the out arcs of the node
        out_arcs = node.get_out_arcs()
        if len(out_arcs) > 1:
            raise Exception(
                f"The node '{node.name}' contains multiple target nodes. "
                f"Please remove all  edges but one or check whether the node "
                f"could be modelled as a parallel/exclusive gateway."
            )
        if len(out_arcs) == 0:
            raise Exception(
                f"The node '{node.name}' is not connected to a target node."
                "Please create an edge to one target node!"
            )

    def _check_target_nodes(self, gateway: ExclusiveGateway | ParallelGateway) -> None:
        """Check the target nodes of a given gateway for abnormalities.
        The abnormality is that the gateway must always be followed by at least two nodes.
        Also an end event cannot be directly connected to a parallel gateway.

        :param gateway: _descriptio
        :raises Exception: Gateway is connected to one target node
        :raises Exception: Gateway is not connected to target nodes
        :raises Exception: Parallel Gateway is connected to an end event
        """
        # Get the out arcs of the gateway
        out_arcs = gateway.get_out_arcs()
        if len(out_arcs) == 1:
            raise Exception(
                f"Only one target found for node '{gateway.name}'. "
                "Add another target node!"
            )
        elif len(out_arcs) == 0:
            raise Exception(
                f"The node '{gateway.name}' is not connected to a target node. "
                " Please connect it at least to two!"
            )
        if self.is_parallel_gateway(gateway):
            for arc in out_arcs:
                if self.is_end_event(arc.target):
                    raise Exception(
                        f"The node '{gateway.name}' is connected to an end event. "
                        "Please delete the directly connected end node!"
                    )

    def get_as_adjacent_dict(self):
        return self.graph

    def get_bpmn(self):
        return visualizer.apply(self.bpmn, parameters={"format": str("svg").lower()})

    def view_bpmn(self) -> None:
        gviz = visualizer.apply(self.bpmn)
        visualizer.matplotlib_view(gviz)

    def save_bpmn(self) -> None:
        gviz = visualizer.apply(self.bpmn)
        visualizer.save(gviz, "model.gviz")
