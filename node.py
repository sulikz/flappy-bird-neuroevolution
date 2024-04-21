import numpy as np


class Node:
    def __init__(self, layer: int, bias=False):
        self.input_value = 0.0
        self.output_value = 0.0
        self.layer = layer
        self.is_bias = bias
        self.connections = []

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    def reset(self):
        self.input_value = 0.0
        if self.is_bias:
            self.output_value = 1.0
        else:
            self.output_value = 0.0

    def activate(self):
        if self.layer > 0:
            self.output_value = self.sigmoid(self.input_value)
        for conn in self.connections:
            conn.to_node.input_value += conn.weight * self.output_value


class NodeConnection:
    def __init__(self, from_node: Node, to_node: Node, weight: float):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
