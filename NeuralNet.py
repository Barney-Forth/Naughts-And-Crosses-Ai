import random
import csv
import os
from numpy import tanh


class Neuron:
    """Represents a single neuron in the neural network.

    A neuron has weights for each input from the previous layer and a bias term.
    It uses the tanh activation function.

    Attributes:
        weights (list[float]): Weights for each input from the previous layer.
            Has getter and setter.
        bias (float): The neuron's bias term. Has getter and setter.
    """

    def __init__(self, previous_layer_size: int):
        """Initialize a neuron with random weights and bias.

        Args:
            previous_layer_size: The number of inputs (neurons in previous layer).
        """
        self._weights = [random.uniform(-10, 10)
                         for i in range(previous_layer_size)]
        self._bias = random.uniform(-10, 10)

    @property
    def weights(self):
        return self._weights

    @weights.setter
    def weights(self, new_weights: list[float]):
        if not isinstance(new_weights, list) or not all(isinstance(w, float) for w in new_weights):
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
        if not isinstance(new_bias, float):
            raise TypeError("New bias should be a float.")

        self._bias = new_bias

    def activate(self, prev_layer: list[float]) -> float:
        """Compute the neuron's output given inputs from the previous layer.

        Args:
            prev_layer: A list of output values from the previous layer.

        Returns:
            The tanh-activated output of this neuron.
        """
        weighted_values = [self._weights[i] * prev_layer[i]
                           for i in range(len(prev_layer))]

        sumed_values = sum(weighted_values) + self._bias

        return tanh(sumed_values)

    def __str__(self) -> str:
        return f"weights: {self._weights}, bias: {self._bias}"


class Layer:
    """Represents a layer of neurons in the neural network.

    Attributes:
        neurons (list[Neuron]): List of Neuron objects in this layer.
            Has getter only (read-only).
    """

    def __init__(self, size, prev_layer_size: int):
        """Initialize a layer with a specified number of neurons.

        Args:
            size: The number of neurons in this layer.
            prev_layer_size: The number of inputs per neuron (size of previous layer).
        """
        self._neurons = [Neuron(prev_layer_size)
                         for i in range(size)]

    @property
    def neurons(self):
        return self._neurons

    def output(self, prev_layer_output: list[int]):
        """Compute the output of all neurons in this layer.

        Args:
            prev_layer_output: The output values from the previous layer.

        Returns:
            A list of output values, one from each neuron in this layer.
        """
        return [neuron.activate(prev_layer_output) for neuron in self._neurons]


class Network:
    """Represents a multi-layer neural network for Tic-Tac-Toe decision-making.

    The network can be loaded from disk or created new with random weights.
    Input size is typically 10 (9 board positions + 1 player indicator).
    Output size is typically 9 (one value per board position).

    Attributes:
        name (str): The name/identifier of the network used for saving and loading.
            Public attribute, no explicit getter/setter.
        DIRECTORY (str): Class variable for the base directory where networks are stored.
            No getter/setter.
    """

    DIRECTORY = os.getcwd() + "\\nets\\"

    def __init__(self, name: str, input_size: int = 10, layer_sizes: list[int] = [20, 9]):
        """Initialize or load a neural network.

        Args:
            name: The name/identifier of the network.
            input_size: The number of input values (default: 10).
            layer_sizes: List of sizes for each hidden and output layer (default: [20, 9]).
        """
        self.name = name
        self._layers = []
        if os.path.exists(self.DIRECTORY + self.name + "\\"):
            self.load_net_values()
        else:
            self.new_net(input_size, layer_sizes)

    def get_output(self, board_input: list[str], player: int) -> tuple[int, int]:
        """Get the network's move recommendation for the current board state.

        Args:
            board_input: A flattened list representing the board (9 elements).
            player: The current player (0 or 1).

        Returns:
            A tuple of (row, col) representing the recommended move.
        """
        net_output = list(map(lambda x: 1 if x == "X" else -1 if x == "O" else 0,
                              board_input)) + [player]

        for layer in self._layers:
            net_output = layer.output(net_output)

        position = net_output.index(max(net_output))

        return (position // 3, position % 3)

    def new_net(self, input_size: int, layer_sizes: list[int]):
        """Create a new network with random weights and save it to disk.

        Args:
            input_size: The number of input values.
            layer_sizes: List of sizes for each hidden and output layer.
        """
        if not os.path.exists(self.DIRECTORY + self.name + "\\"):
            os.makedirs(self.DIRECTORY + self.name + "\\")

        prev_layer_sizes = [input_size] + layer_sizes[:-1]

        self._layers = [Layer(layer_sizes[i], prev_layer_sizes[i])
                        for i in range(len(layer_sizes))]
        self.save_net_values()

    def save_net_values(self):
        """Save the network's weights and biases to CSV files on disk.

        Creates one CSV file per layer in the network's directory.
        """
        for i, layer in enumerate(self._layers):
            with open(self.DIRECTORY + self.name + f"\\layer_{i}.csv", "w", newline="") as f:
                neurons = [neuron.weights + [neuron.bias]
                           for neuron in layer.neurons]
                writer = csv.writer(f)
                writer.writerows(neurons)

    def load_net_values(self):
        """Load the network's weights and biases from CSV files on disk.

        Raises:
            FileNotFoundError: If the network directory doesn't exist.
        """
        if not os.path.exists(self.DIRECTORY + self.name + "\\"):
            raise FileNotFoundError(
                f"No file found at {self.DIRECTORY + self.name}\\")

        files = os.listdir(self.DIRECTORY + self.name + "\\")
        prev_layer_size = 10

        for file in files:
            with open(self.DIRECTORY + self.name + "\\" + file, "r") as f:
                reader = csv.reader(f)
                num_of_rows = sum(1 for row in reader)
                self._layers.append(
                    Layer(num_of_rows, prev_layer_size))
                prev_layer_size = 0
                f.seek(0)
                reader = csv.reader(f)
                for i in range(num_of_rows):
                    row = next(reader)
                    self._layers[-1].neurons[i].weights = [
                        float(x) for x in row[:-1]]
                    self._layers[-1].neurons[i].bias = float(row[-1])
                    prev_layer_size += 1
