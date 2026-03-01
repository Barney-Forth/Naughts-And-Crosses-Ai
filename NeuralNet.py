import random
import csv
import os
from numpy import tanh


class Neuron:
    def __init__(self, previous_layer_size: int):
        self._weights = [random.randrange(-10, 10)
                         for i in range(previous_layer_size)]
        self._bias = random.randrange(-10, 10)

    @property
    def weights(self):
        return self._weights

    @weights.setter
    def weights(self, new_weights: list[float]):
        if type(new_weights) != list[float]:
            raise TypeError("New weights should be a list of floats.")

        if len(new_weights) != len(self._weights):
            raise ValueError(
                f"New weights should be of length {len(self._weights)}.")

        self._weights = new_weights

    @property
    def bias(self):
        return self._bias

    @bias.setter
    def bias(self, new_bias: float):
        if type(new_bias) != float:
            raise TypeError("New bias should be a float.")

        self._bias = new_bias

    def activate(self, prev_layer: list[float]) -> float:
        weighted_values = [self._weights[i] * prev_layer[i]
                           for i in range(len(prev_layer))]

        sumed_values = sum(weighted_values) + self._bias

        return tanh(sumed_values)

    def __str__(self) -> str:
        return f"weights: {self._weights}, bias: {self._bias}"


class Layer:
    def __init__(self, prev_layer_size: int):
        self._neurons = [Neuron(len(prev_layer_size))
                         for i in range(len(prev_layer_size))]

    @property
    def neurons(self):
        return self._neurons

    def output(self, prev_layer_output: list[int]):
        return [neuron.activate(prev_layer_output) for neuron in self._neurons]


class Network:
    DIRECTORY = os.getcwd() + "/nets/"

    def __init__(self):
        self._layers = []

    def get_output(self, board_input: list[str], player: int) -> tuple[int, int]:
        net_output = list(map(lambda x: 1 if x == "X" else -1 if x == "O" else 0,
                              board_input)) + [player]

        for layer in self._layers:
            net_output = layer.output(net_output)

        position = net_output.index(max(net_output))

        return (position // 3, position % 3)

    def new_net(self, name: str, input_size: int, layer_sizes: list[int]):
        if not os.path.exists(self.DIRECTORY + name + "/"):
            os.makedirs(self.DIRECTORY + name + "/")

        self._layers = [Layer(size) for size in [input_size] + layer_sizes]
        self.save_net_values()

    def save_net_values(self):
        for i, layer in enumerate(self._layers):
            with open(self.DIRECTORY + self._name + f"/layer_{i}.csv", "w") as f:
                writer = csv.writer(f)
                for neuron in layer.neurons:
                    writer.writerow(neuron.weights + [neuron.bias])

    def load_net_values(self, net_name: str):
        if not os.path.exists(self.DIRECTORY + net_name + "/"):
            raise FileNotFoundError(
                f"No file found at {self.DIRECTORY + net_name}/.")

        files = os.listdir(self.DIRECTORY + net_name + "/")
        prev_layer_size = 10

        for file in files:
            self._layers.append(Layer(prev_layer_size))
            with open(self.DIRECTORY + net_name + "/" + file, "r") as f:
                prev_layer_size = 0
                reader = csv.reader(f)
                for i in range(len(reader)):
                    row = next(reader)
                    self._layers[-1].neurons[i].weights = list(
                        map(float, row[:-1]))
                    self._layers[-1].neurons[i].bias = float(row[-1])
                    prev_layer_size += 1
