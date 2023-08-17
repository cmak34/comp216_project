import paho.mqtt.client as mqtt
import json
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.lines as mlines
from settings import Settings

class Subscriber:
    # constructor for the subscriber class
    # broker_host: the host name of the MQTT broker
    # broker_port: the port number of the MQTT broker
    # topic: the topic to subscribe to
    def __init__(self, broker_host, broker_port, topic):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.topic = topic

        self.max_val = Settings.get_max_val() # max value for temperature
        self.min_val = Settings.get_min_val() # min value for temperature
        self.buffer_size = Settings.get_buffer_size() # buffer size for the plot
        
        # Separate buffers for each publisher
        self.data_buffers = {}
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
    # data: the data to plot
    def plot_data(self, data):
        if (data is not None and data["station_name"] is not None):
            publisher = data["station_name"]
            # Check if self.data_buffers[publisher] exists
            if (data["station_name"] not in self.data_buffers):
                self.data_buffers[data["station_name"]] = []
        
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
            if len(self.data_buffers[publisher]) > self.buffer_size:
                self.data_buffers[publisher].pop(0)
        
            # Update the plot
            plt.clf()
            
            # Draw lines for each publisher
            # Add legend
            handles = []
            counter = 0
            for key, value in self.data_buffers.items():
                color = self.generate_color(counter)
                plt.plot(self.data_buffers[key], label=key, color= color)
                handles.append(mlines.Line2D([], [], color=color, label=key))
                counter += 1

            plt.xlabel('Time')
            plt.ylabel('Temperature')
            plt.ylim([self.min_val, self.max_val])
            plt.xlim([0, self.buffer_size])
            plt.title("Temperature Data from stations")
            plt.legend(handles=handles)
            self.canvas.draw()


    # callback function for when a message is received
    # client: the client object for this callback
    def on_message(self, client, userdata, message):
        try:
            payload_str = message.payload.decode("utf-8")
            data = json.loads(payload_str)
            self.plot_data(data)
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
        self.ax.set_xlim([0, self.buffer_size])
        self.ax.set_title("Temperature Data from stations")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
    
    def generate_color(self, counter):
        mode = counter % 3
        seed_red = 200
        seed_green = 0
        seed_blue = 100
        if mode == 0:
            seed_red = 200 + counter * 20
        if mode == 1:
            seed_green = 200 + counter * 20
        if mode == 2:
            seed_blue = 200 + counter * 20
        r = (seed_red) % 256  # Red
        g = (seed_green) % 256  # Green
        b = (seed_blue) % 256  # Blue
        return (r/255, g/255, b/255)  # Return the RGB color tuple

    # run the GUI
    def run(self):
        self.client.loop_start()
        self.root.mainloop()

if __name__ == "__main__":
    subscriber = Subscriber("localhost", 1883, "topic/data")
    subscriber.run()