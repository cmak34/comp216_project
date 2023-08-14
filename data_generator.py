import random
import numpy as np

class DataGenerator:
    def __init__(self, min_val=0, max_val=1, noise=0.1, frequency=100):
        self.min_val = min_val
        self.max_val = max_val
        self.noise = noise
        self.frequency = frequency
        self._time_step = 0

    def _generate_normalized_value(self):
        sine_wave = (np.sin(2 * np.pi * self._time_step / self.frequency) + 1) / 2
        noise_val = self.noise * random.uniform(-1, 1)
        self._time_step += 1
        return sine_wave + noise_val

    @property
    def value(self):
        normalized_value = self._generate_normalized_value()
        range_val = self.max_val - self.min_val
        output_value = self.min_val + range_val * normalized_value
        return output_value