import paho.mqtt.client as mqtt
import json
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.lines as mlines
from settings import Settings
import numpy as np

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
        self.missing_data_points = {}
        self.corrupted_data_points = {}

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
        try:
            if (data is not None and data["station_name"] is not None):
                publisher = data["station_name"]
                # Check if self.data_buffers[publisher] exists
                if (data["station_name"] not in self.data_buffers):
                    self.data_buffers[data["station_name"]] = []
                print(data)
                label = None
                if "temperature" not in data or data["temperature"] is None or data["temperature"] == "":
                    self.data_buffers[publisher].append(np.nan)
                    label = 'missing'
                    if publisher not in self.missing_data_points:
                        self.missing_data_points[publisher] = []
                    self.missing_data_points[publisher].append(len(self.data_buffers[publisher])-1)
                elif data["temperature"] == "corrupted":
                    self.data_buffers[publisher].append(np.nan)
                    label = 'corrupted'
                    if publisher not in self.corrupted_data_points:
                        self.corrupted_data_points[publisher] = []
                    self.corrupted_data_points[publisher].append(len(self.data_buffers[publisher])-1)
                else:
                    self.data_buffers[publisher].append(data['temperature'])

                if len(self.data_buffers[publisher]) > self.buffer_size:
                    self.data_buffers[publisher].pop(0)
            
                plt.clf()
                handles = []
                counter = 0
                for key, value in self.data_buffers.items():
                    color = self.generate_color(counter)
                    plt.plot(self.data_buffers[key], label=key, color=color)
                    handles.append(mlines.Line2D([], [], color=color, label=key))
                    
                    # Annotate missing data points
                    if key in self.missing_data_points:
                        for index in self.missing_data_points[key]:
                            plt.annotate("missing",
                                        (index, self.min_val),
                                        color=color,
                                        xytext=(0, 5),
                                        textcoords="offset points",
                                        ha='center',
                                        va='bottom',
                                        fontsize=3)
        
                    # Annotate corrupted data points
                    if key in self.corrupted_data_points:
                        for index in self.corrupted_data_points[key]:
                            plt.annotate("corrupted",
                                        (index, self.min_val),
                                        color=color,
                                        xytext=(0, 5),
                                        textcoords="offset points",
                                        ha='center',
                                        va='bottom',
                                        fontsize=3)
                    
                    counter += 1
                
                plt.xlabel('Packets', fontdict={'fontsize': 4, 'fontweight': 'light'}, labelpad=-2)
                plt.ylabel('Temperature', fontdict={'fontsize': 4, 'fontweight': 'light'}, labelpad=-2) 
                plt.ylim([self.min_val, self.max_val])
                plt.xlim([0, self.buffer_size])
                plt.tick_params(axis='x', labelsize=6)
                plt.tick_params(axis='y', labelsize=6)
                plt.title("Temperature Data from stations", fontdict={'fontsize': 6, 'fontweight': 'light'})
                plt.legend(handles=handles, prop={'size': 6})
                self.canvas.draw()
        except Exception as e:
            print(f"An error occurred during data plotting: {e}")


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
        try:
            self.root = tk.Tk()
            self.root.title("MQTT Subscriber GUI")
            width = 600
            height = 400
            self.root.geometry(f"{width}x{height}")
            self.root.grid_rowconfigure(0, weight=1)
            self.root.grid_columnconfigure(0, weight=1)
            self.fig, self.ax = plt.subplots(figsize=(width / 100, height / 100))
            self.ax.set_ylim([self.min_val, self.max_val])
            self.ax.set_xlim([0, self.buffer_size])
            self.ax.set_title("Temperature Data from stations", fontdict={'fontsize': 6, 'fontweight': 'light'})
            self.ax.tick_params(axis='x', labelsize=6)
            self.ax.tick_params(axis='y', labelsize=6)
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
            self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        except Exception as e:
            print(f"An error occurred during GUI setup: {e}")
    
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
        r = (seed_red) % 256 
        g = (seed_green) % 256
        b = (seed_blue) % 256
        return (r/255, g/255, b/255)

    # run the GUI
    def run(self):
        self.client.loop_start()
        self.root.mainloop()

if __name__ == "__main__":
    subscriber = Subscriber("localhost", 1883, "topic/data")
    subscriber.run()