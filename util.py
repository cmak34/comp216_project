import time
import random
import string

class Util:

    def create_data(temperature, name):
        data = {
            'station_name': name,  # Use the passed name here
            'timestamp': time.asctime(),
            'temperature': temperature,
        }
        return data

    def print_data(data):
        print(f"Station Name: {data['station_name']}")
        print(f"Time: {data['timestamp']}")
        print(f"Temperature: {data['temperature']:.2f} °C")  # Two decimal places for temperature
