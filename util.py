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
            # 'humidity': round(random.uniform(30, 80), 2),           # Humidity percentage with 2 decimal places
            # 'pressure': round(random.uniform(980, 1050), 2),        # Atmospheric pressure in hPa with 2 decimal places
            # 'wind': {
            #     'speed': round(random.uniform(0, 15), 2),           # Wind speed in meters per second with 2 decimal places
            #     'direction': random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']),
            # },
            # 'rainfall': round(random.uniform(0, 10), 2),            # Rainfall in millimeters with 2 decimal places
            # 'cloud_cover': round(random.uniform(0, 100), 2),        # Cloud cover percentage with 2 decimal places
            # 'sunshine_duration': round(random.uniform(0, 10), 2),   # Sunshine duration in hours with 2 decimal places
        }
        # start_id += 1
        return data

    def print_data(data):
        # print(f"ID: {data['id']}")
        print(f"Station Name: {data['station_name']}")
        print(f"Time: {data['timestamp']}")
        print(f"Temperature: {data['temperature']:.2f} °C")  # Two decimal places for temperature
        # print(f"Humidity: {data['humidity']:.2f} %")         # Two decimal places for humidity
        # print(f"Pressure: {data['pressure']:.2f} hPa")       # Two decimal places for pressure
        # print("Wind:")
        # print(f"  Speed: {data['wind']['speed']:.2f} m/s")   # Two decimal places for wind speed
        # print(f"  Direction: {data['wind']['direction']}")
        # print(f"Rainfall: {data['rainfall']:.2f} mm")        # Two decimal places for rainfall
        # print(f"Cloud Cover: {data['cloud_cover']:.2f} %")   # Two decimal places for cloud cover
        # print(f"Sunshine Duration: {data['sunshine_duration']:.2f} hours")  # Two decimal places for sunshine duration
