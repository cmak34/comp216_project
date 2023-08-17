import random
from data_generator import DataGenerator
from util import Util
import random
from settings import Settings

class Publisher:
    
    # constructor for the publisher
    # @param min_val: minimum value of the data, i.e. lowest temp in our case of weather station
    # @param max_val: maximum value of the data, i.e. highest temp in our case of weather station
    # @param name: name of the publisher (weather station)
    # @param missing_data_chance: chance of missing data in percentage
    # @param corrupted_data_chance: chance of corrupted data in percentage
    def __init__(self, min_val=0, max_val=1, name="", missing_data_chance=1, corrupted_data_chance=1):
        try:
            self.generator = DataGenerator(min_val, max_val)
            self.name = name
            self.missing_data_chance = missing_data_chance
            self.corrupted_data_chance = corrupted_data_chance
            self.packet_id = 0
            self.max_val = Settings.get_max_val()
            self.min_val = Settings.get_min_val()
        except Exception as e:
            print(f"Error in __init__: {e}")

    # function to get the packet
    # @description: gets the packet from the data generator, also it will randomly corrupt the data and missing data based on the chances inputted
    # @return: packet
    def get_packet(self):
        try:
            temperature = self.generator.value
            packet = Util.create_data(temperature, self.name, self.packet_id)
            self.packet_id += 1
            packet["packet_id"] = self.packet_id
            if temperature > self.max_val or temperature < self.min_val:
                packet["temperature"] = "out of range"
            if random.randint(1, 100) <= self.missing_data_chance:  # chance of missing data in percentage
                packet["temperature"] = None
            if random.randint(1, 100) <= self.corrupted_data_chance:  # chance of corrupted data in percentage
                packet["temperature"] = "corrupted"
            return packet
        except Exception as e:
            print(f"Error in get_packet: {e}")
            return None