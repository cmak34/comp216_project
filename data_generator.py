import random
import numpy as np

class DataGenerator:
    def __init__(self, min_val=0, max_val=1, noise=0.3, period=100):
        self.min_val = min_val
        self.max_val = max_val
        self.noise = noise
        self.period = period
        self._time_step = 0

    def _generate_normalized_value(self):
        """Generate a normalized value in the range [-1, 1]"""
        sine_wave = np.sin(2 * np.pi * self._time_step / self.period)
        noise_val = self.noise * (2*random.random() - 1)
        self._time_step += 1
        combined_value = sine_wave + noise_val
        return combined_value

    @property
    def value(self):
        normalized_value = self._generate_normalized_value()
        range_val = self.max_val - self.min_val
        output_value = self.min_val + (range_val * (normalized_value + 1) /2)
        return output_value