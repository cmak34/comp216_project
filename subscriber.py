import paho.mqtt.client as mqtt
import json
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Subscriber:
    def __init__(self, broker_host, broker_port, topic):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.topic = topic

        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(self.broker_host, self.broker_port, 60)
        self.client.subscribe(self.topic)

        self.data_buffer = []
        self.BUFFER_SIZE = 100

        self.setup_gui()

    def plot_data(self, data):
        # Check for missing data
        if data is None:
            print("Data: Missing")
            self.data_buffer.append(None)  # Append None to create a gap
        else:
            # Check if temperature data is missing
            if "temperature" not in data or data["temperature"] is None:
                print("Data: Temperature is missing")
                self.data_buffer.append(None)  # Append None to create a gap
            else:
                # Check if temperature data is not a number
                if not isinstance(data["temperature"], (int, float)):
                    print("Data: Temperature is not a number")
                    self.data_buffer.append(None)  # Append None to create a gap
                else:
                    # Check if temperature data is out of range
                    if data["temperature"] > 50 or data["temperature"] < -100:
                        print("Data: Temperature is out of range")
                        self.data_buffer.append(None)  # Append None to create a gap
                    else:
                        # If data passes all checks, update the buffer
                        self.data_buffer.append(data['temperature'])

        # Maintain buffer size
        if len(self.data_buffer) > self.BUFFER_SIZE:
            self.data_buffer.pop(0)

        # Update the plot
        plt.clf()
        plt.plot(self.data_buffer)
        plt.xlabel('Time')
        plt.ylabel('Received temperature')
        self.canvas.draw()


    def on_message(self, client, userdata, message):
        payload_str = message.payload.decode("utf-8")
        try:
            data = json.loads(payload_str)
            print("Received data:")
            print(data)

            #@TODO: check corrupt data

            self.plot_data(data)

        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON data: {e}")

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("MQTT Subscriber GUI")

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

        print("Waiting for messages...")

    def run(self):
        self.client.loop_start()
        self.root.mainloop()


if __name__ == "__main__":
    subscriber = Subscriber("localhost", 1883, "topic/data")
    subscriber.run()