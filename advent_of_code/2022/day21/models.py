from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from .input import Operation, MonkeyInput


class OperationNotSupported(Exception):
    ...


@dataclass
class MonkeyNode:
    name: str
    number: Optional[int]
    operation: Optional[Operation]

    @property
    def has_number(self) -> bool:
        return self.number is not None


@dataclass
class MonkeyGraph:
    adjancency_list: dict[str, list[str]]
    node_map: dict[str, MonkeyNode]

    def fill_node_numbers(self, visiting: str, visited=set()) -> MonkeyNode:
        """
        Uses Depth First Search to navigate the graph.
        Recursively updates each node with its number based on its operation and the numbers of its child nodes.
        """
        visited.add(visiting)
        destinations = self.adjancency_list[visiting]
        visiting_node = self.node_map[visiting]

        if not destinations:
            return visiting_node

        destination_nodes_with_numbers = []
        for destination in destinations:
            destination_node = self.node_map[destination]
            destination_node = self.fill_node_numbers(destination, visited)

            if destination_node.has_number:
                destination_nodes_with_numbers.append(destination_node)

        if len(destination_nodes_with_numbers) == len(destinations):
            visiting_node.number = self.calculate_node_number(
                visiting_node, destination_nodes_with_numbers
            )
        return visiting_node

    def calculate_node_number(
        self, visiting_node: MonkeyNode, destination_nodes: list[MonkeyNode]
    ) -> int:
        assert len(destination_nodes) == 2

        if visiting_node.operation == Operation.ADD:
            return destination_nodes[0].number + destination_nodes[1].number
        elif visiting_node.operation == Operation.SUBTRACT:
            return destination_nodes[0].number - destination_nodes[1].number
        elif visiting_node.operation == Operation.MULTIPLY:
            return int(destination_nodes[0].number * destination_nodes[1].number)
        elif visiting_node.operation == Operation.DIVIDE:
            return int(destination_nodes[0].number / destination_nodes[1].number)
        raise OperationNotSupported()

    @classmethod
    def create(cls, monkey_inputs: list[MonkeyInput]) -> MonkeyGraph:
        adjancency_list = {}
        node_map = {}

        for monkey_input in monkey_inputs:
            node = MonkeyNode(
                name=monkey_input.name,
                number=monkey_input.number,
                operation=monkey_input.operation,
            )
            adjancency_list[node.name] = []
            node_map[node.name] = node

            for child in monkey_input.children:
                adjancency_list[node.name].append(child)

        return cls(adjancency_list=adjancency_list, node_map=node_map)
