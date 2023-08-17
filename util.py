import time
import random
import string
from settings import Settings

class Util:

    def create_data(temperature, name, id):
        data = {
            'station_name': name,  # Use the passed name here
            'timestamp': time.asctime(),
            'temperature': temperature,
            'packet_id': id
        }
        return data

    def print_data(data):
        print(f"Station Name: {data['station_name']}")
        print(f"Packet ID: {data['packet_id']}")
        print(f"Time: {data['timestamp']}")
        print(f"Temperature: {data['temperature']:.2f} °C")  # Two decimal places for temperature

    def checkCorruptedDate(data):
        if data is None:
            return True
        if "temperature" not in data or data["temperature"] is None:
            return True
        if type(data["temperature"]) is str:
            return True
        if type(data["temperature"]) is not (float):
            return True
        if data["temperature"] > Settings.get_max_val() or data["temperature"] < Settings.get_min_val():
            return True
        if data["packet_id"] is None:
            return True
        if data["station_name"] is None:
            return True
        if data["timestamp"] is None:
            return True
        return False
