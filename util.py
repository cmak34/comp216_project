import time
import random
import string

class Util:
    # global start_id = 111 
    
    def create_data(temperature):
        station_name = ''.join(random.choices(string.ascii_uppercase, k=1))  # Random 1-character station name
        data = {
            # 'id': start_id,
            'station_name': station_name,
            'timestamp': time.asctime(),
            'temperature': temperature,        # Temperature in Celsius with 2 decimal places
        }
        # start_id += 1
        return data

    def print_data(data):
        # print(f"ID: {data['id']}")
        print(f"Station Name: {data['station_name']}")
        print(f"Time: {data['timestamp']}")
        print(f"Temperature: {data['temperature']:.2f} °C")  # Two decimal places for temperature

