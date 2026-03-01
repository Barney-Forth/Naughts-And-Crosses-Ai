import numpy
import random


class Neuron:
    def __init__(self, previous_layer_size: int):
        self._weights = [random.randrange(-10, 10)
                         for i in range(previous_layer_size)]
        self._bias = random.randrange(-10, 10)

    def activate(self, prev_layer: list[float]) -> float:
        weighted_values = [self._weights[i] * prev_layer[i]
                           for i in range(len(prev_layer))]

        sumed_values = sum(weighted_values) + self._bias

        return numpy.tanh(sumed_values)

    def __str__(self) -> str:
        return f"weights: {self._weights}, bias: {self._bias}"


class Layer:
    def __init__(self, prev_layer_size: int):
        self._neurons = [Neuron(len(prev_layer_size))
                         for i in range(len(prev_layer_size))]

    def output(self, prev_layer_output: list[int]):
        return [neuron.activate(prev_layer_output) for neuron in self._neurons]


class Network:
    def __init__(self):
        self._layers = [Layer(10), Layer(20), Layer(9)]

    def get_output(self, board_input: list[str], player: int) -> tuple[int, int]:
        net_output = list(map(lambda x: 1 if x == "X" else -1 if x == "O" else 0,
                              board_input)) + [player]

        for layer in self._layers:
            net_output = layer.output(net_output)
