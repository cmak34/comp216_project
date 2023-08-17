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
    
    # constructor for the publisher
    # @param min_val: minimum value of the data, i.e. lowest temp in our case of weather station
    # @param max_val: maximum value of the data, i.e. highest temp in our case of weather station
    # @param name: name of the publisher (weather station)
    # @param missing_data_chance: chance of missing data in percentage
    # @param corrupted_data_chance: chance of corrupted data in percentage
    def __init__(self, min_val=0, max_val=1, name="", missing_data_chance=0, corrupted_data_chance=0):
        self.generator = DataGenerator(min_val, max_val)
        self.name = name
        self.missing_data_chance = missing_data_chance
        self.corrupted_data_chance = corrupted_data_chance
        self.packet_id = 0

    # function to get the packet
    # @description: gets the packet from the data generator, also it will randomly corrupt the data and missing data based on the chances inputted
    # @return: packet
    def get_packet(self):
        if random.randint(1, 100) <= self.missing_data_chance:  # chance of missing data in percentage
            return None
        temperature = self.generator.value
        packet = Util.create_data(temperature, self.name, self.packet_id)
        self.packet_id += 1
        if random.randint(1, 100) <= self.corrupted_data_chance:  # chance of corrupted data in percentage
            packet["temperature"] = "corrupted"
        packet["packet_id"] = self.packet_id
        return packet