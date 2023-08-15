import paho.mqtt.client as mqtt
import json
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.lines as mlines

class Subscriber:
    # constructor for the subscriber class
    # broker_host: the host name of the MQTT broker
    # broker_port: the port number of the MQTT broker
    # topic: the topic to subscribe to
    def __init__(self, broker_host, broker_port, topic):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.topic = topic

        self.max_val = 50.0 # max value for temperature
        self.min_val = -50.0 # min value for temperature
        self.BUFFER_SIZE = 100
        # Separate buffers for each publisher
        self.data_buffers = {
            'publisher1': [],
            'publisher2': []
        }
        self.setup_gui()
                
        try:
            self.client = mqtt.Client()
            self.client.on_message = self.on_message
            self.client.connect(self.broker_host, self.broker_port, 60)
            self.client.subscribe(self.topic)
        except ConnectionRefusedError:
            print("Connection to MQTT broker refused. Make sure the broker is running.")
            return

    # plot the data
    # publisher: the publisher of the data
    # data: the data to plot
    def plot_data(self, publisher, data):
        if data is None:
            print("Data: Missing")
            self.data_buffers[publisher].append(None)
        else:
            # Check if temperature data is missing
            if "temperature" not in data or data["temperature"] is None:
                print("Data: corrupted1")
                self.data_buffers[publisher].append(None)  # Append None to create a gap
            # Check if temperature data is str
            elif type(data["temperature"]) is str: 
                print("Data: corrupted2")
                self.data_buffers[publisher].append(None)  # Append None to create a gap
            # Check if temperature data is not a number
            elif type(data["temperature"]) is not (float):
                print("Data: corrupted3")
                self.data_buffers[publisher].append(None)  # Append None to create a gap
            # Check if temperature data is out of range
            elif data["temperature"] > self.max_val or data["temperature"] < self.min_val:
                print("Data: Temperature is out of range")
                self.data_buffers[publisher].append(None)  # Append None to create a gap        
            # If data passes all checks, update the buffer
            else:
                self.data_buffers[publisher].append(data['temperature'])
    
        # If data passes all checks, update the appropriate buffer
        if len(self.data_buffers[publisher]) > self.BUFFER_SIZE:
            self.data_buffers[publisher].pop(0)
    
        # Update the plot
        plt.clf()
        
        # Draw lines for each publisher
        for pub, color in [('publisher1', 'blue'), ('publisher2', 'orange')]:
            plt.plot(self.data_buffers[pub], label=pub, color=color)

        plt.xlabel('Time')
        plt.ylabel('Temperature')
        plt.ylim([self.min_val, self.max_val])
        plt.xlim([0, self.BUFFER_SIZE])
        plt.title("Temperature Data from stations A and B")
        # Add legend
        handles = [
            mlines.Line2D([], [], color='blue', label='Station A'),
            mlines.Line2D([], [], color='orange', label='Station B')
        ]
        plt.legend(handles=handles)
        self.canvas.draw()


    # callback function for when a message is received
    # client: the client object for this callback
    def on_message(self, client, userdata, message):
        try:
            payload_str = message.payload.decode("utf-8")
            data = json.loads(payload_str)
            publisher = "publisher1" if data["station_name"] == "Station A" else "publisher2"
            self.plot_data(publisher, data)
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON data: {e}")

    # setup the GUI of the graph
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("MQTT Subscriber GUI")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.fig, self.ax = plt.subplots()
        self.ax.set_ylim([self.min_val, self.max_val])
        self.ax.set_xlim([0, self.BUFFER_SIZE])
        self.ax.set_title("Temperature Data from stations A and B")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        print("Waiting for messages...")

    # run the GUI
    def run(self):
        self.client.loop_start()
        self.root.mainloop()

if __name__ == "__main__":
    subscriber = Subscriber("localhost", 1883, "topic/data")
    subscriber.run()