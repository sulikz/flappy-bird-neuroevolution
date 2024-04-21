from typing import List

import numpy as np

from config import INITIAL_MUTATION_STRENGTH, MUTATION_RATE, INPUT_SIZE, MIN_MUTATION_STRENGTH
from node import Node, NodeConnection


class Network:
    def __init__(self):
        self.nodes = [Node(layer=0) for _ in range(INPUT_SIZE)]
        self.nodes.append(Node(layer=0, bias=True))
        self.nodes[-1].output_value = 1  # Bias node value
        self.connections = []
        self.input_size = INPUT_SIZE
        output_node = Node(layer=1)
        self.nodes.append(output_node)
        for node in self.nodes[:-1]:  # Except output node
            self.connections.append(NodeConnection(node, output_node, np.random.uniform(-1, 1)))
        self.connect_nodes()

    @classmethod
    def clone_network(cls, network: "Network"):
        new_network = cls()
        new_network.nodes = []
        node_map = {}
        for old_node in network.nodes:
            new_node = Node(layer=old_node.layer, bias=old_node.is_bias)
            node_map[old_node] = new_node
            new_network.nodes.append(new_node)
        new_network.connections = [NodeConnection(node_map[conn.from_node], node_map[conn.to_node], conn.weight) for
                                   conn in network.connections]
        new_network.connect_nodes()
        return new_network

    def connect_nodes(self) -> None:
        for node in self.nodes:
            node.connections = []
        for conn in self.connections:
            conn.from_node.connections.append(conn)

    def feed_forward(self, inputs: List[float]) -> float:
        for node in self.nodes:
            node.reset()
        for idx, input in enumerate(inputs):
            self.nodes[idx].output_value = input
        for node in self.nodes:
            node.activate()
        return self.nodes[-1].output_value

    def mutate(self, current_generation) -> None:
        generation_factor = max(MIN_MUTATION_STRENGTH, 1 - (current_generation / 100))  # Decrease over 100 generations
        adaptive_mutation_strength = INITIAL_MUTATION_STRENGTH * generation_factor
        for conn in self.connections:
            if np.random.rand() < MUTATION_RATE:
                conn.weight += np.random.uniform(-adaptive_mutation_strength, adaptive_mutation_strength)
                conn.weight = np.clip(conn.weight, -1, 1)
