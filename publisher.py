import random
from data_generator import DataGenerator
from util import Util
import tkinter as tk
from threading import Thread
import paho.mqtt.client as mqtt
import json
import time
import random
import numpy as np

class Publisher:
    def __init__(self, min_val=0, max_val=1, name=""):
        self.generator = DataGenerator(min_val, max_val)
        self.packet_id = 0
        self.name = name  # the publisher's unique name

    def get_packet(self):
        if random.randint(1, 100) <= 1:  # 1% chance of missing data
            return None

        temperature = self.generator.value
        packet = Util.create_data(temperature, self.name)

        if random.randint(1, 100) <= 10:  # 10% chance of corrupted data
            packet["temperature"] = round(temperature + random.uniform(-2, 2), 2)  # Introduce random variation

        self.packet_id += 1
        return packet