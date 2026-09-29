import numpy as np

INIT_SCALE = 0.5  # shared with genetic.py so random genomes match init scale


class Layer_Dense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = INIT_SCALE * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))

    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases


class Activation_ReLU:
    def forward(self, inputs):
        self.output = np.maximum(0, inputs)


class Activation_Tanh:
    def forward(self, inputs):
        self.output = np.tanh(inputs)


class Activation_Sigmoid:
    def forward(self, inputs):
        self.output = 1 / (1 + np.exp(-np.clip(inputs, -500, 500)))


class NeuralNetwork:
    """
    Doodle Jump brain. 3 outputs: [left, stay, right]. Action = argmax.
    Suggested inputs (normalize all to roughly -1..1):
      player x / WIDTH, player y_velocity / 20,
      dx, dy to nearest platform above (normalized),
      dx, dy to 2nd nearest platform above,
      dx, dy to nearest monster (0 if none)
    """

    def __init__(self, input_size=8, hidden_size=12, output_size=3):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.layer1 = Layer_Dense(input_size, hidden_size)
        self.activation1 = Activation_ReLU()
        self.layer2 = Layer_Dense(hidden_size, output_size)

    @property
    def genome_size(self):
        return (self.input_size * self.hidden_size + self.hidden_size
                + self.hidden_size * self.output_size + self.output_size)

    def forward(self, inputs):
        inputs = np.asarray(inputs, dtype=float).reshape(1, -1)
        self.layer1.forward(inputs)
        self.activation1.forward(self.layer1.output)
        self.layer2.forward(self.activation1.output)
        return self.layer2.output[0]  # raw logits, shape (output_size,)

    def decide(self, inputs):
        """Return -1 (left), 0 (stay), 1 (right)."""
        return int(np.argmax(self.forward(inputs))) - 1

    def get_weights(self):
        return np.concatenate([
            self.layer1.weights.flatten(),
            self.layer1.biases.flatten(),
            self.layer2.weights.flatten(),
            self.layer2.biases.flatten()
        ])

    def set_weights(self, flat_weights):
        flat_weights = np.asarray(flat_weights, dtype=float)
        if flat_weights.size != self.genome_size:
            raise ValueError(f"Expected {self.genome_size} weights, got {flat_weights.size}")

        idx = 0
        for layer in (self.layer1, self.layer2):
            size = layer.weights.size
            # .copy() so brain does not share memory with genome
            layer.weights = flat_weights[idx:idx + size].reshape(layer.weights.shape).copy()
            idx += size
            size = layer.biases.size
            layer.biases = flat_weights[idx:idx + size].reshape(layer.biases.shape).copy()
            idx += size