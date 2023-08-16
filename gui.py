import tkinter as tk
import paho.mqtt.client as mqtt
import numpy as np
from publisher import Publisher
import paho.mqtt.client as mqtt
import json
import time
import random
from threading import Thread
import threading
from subscriber import Subscriber
from settings import Settings

class GUI:
    # constructor for the GUI
    # @description - creates the GUI and sets up the widgets
    # @param root: the root window of tkinter
    def __init__(self, root):
        self.root = root
        self.root.title("MQTT Data Publisher")

        # set up the grid
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
    
        self.proj_description = tk.Label(root, text="""
        COMP 216 Final Project
        Topic: MQTT Data Publisher (Weather Station)

        GROUP MEMBERS:
        Chinnawut Boonluea (301276464)
        Chung Ping Mak (301281670)
        Ho Yin Yip (301288909)
        Wing Chung Kam (301279106)
        Yuen Kwan LI (301228849)

        INSTRUCTIONS:
        1. Start the MQTT broker (mosquitto) on localhost:1883
        2. Click on the "Add Publisher" button to add a publisher
        3. Toggle the start/stop button to start/stop publishing data
        4. Temperature data will be published to the broker every 1 second 
           using random values with noise and following a sine wave pattern
        """, anchor='w', justify='left')
        self.proj_description.grid(row=0, column=0, columnspan=5, sticky='nsew')

        # publisher
        self.publisher = []
        self.publisher_running = []
        self.publisher_thread = []
        self.publisher_log_text = []

        # Add publisher button
        add_publisher_button = tk.Button(root, text="Add Publisher", command=self.add_publisher)
        add_publisher_button.grid(row=1, column=0, pady=10, sticky='nsew')

        self.missing_data_var = tk.BooleanVar()
        missing_data_checkbox = tk.Checkbutton(root, text="Missing Data", variable=self.missing_data_var)
        missing_data_checkbox.grid(row=1, column=1, pady=5, sticky='w')
        
        self.corrupted_data_var = tk.BooleanVar()
        corrupted_data_checkbox = tk.Checkbutton(root, text="Corrupted Data", variable=self.corrupted_data_var)
        corrupted_data_checkbox.grid(row=1, column=2, pady=5, sticky='w')

        # Add subscriber button
        # add_subscriber_button = tk.Button(root, text="Add Subscriber", command=self.add_subscriber)
        # add_subscriber_button.grid(row=1, column=3, pady=10, sticky='nsew')
        
        # connect to the broker
        self.client = mqtt.Client()
        try:
            self.client.connect("localhost", 1883, 60)
        except ConnectionRefusedError:
            print("Connection to MQTT broker refused. Make sure the broker is running.")
            return
    
    # add a publisher
    # @description - adds a publisher to the GUI
    def add_publisher(self):
        index = len(self.publisher)
        max_val = Settings.get_max_val()
        min_val = Settings.get_min_val()
        missing_data_chance = Settings.get_missing_chance() if (self.missing_data_var.get()) else 0
        corrupted_data_chance = Settings.get_corrupted_chance() if (self.corrupted_data_var.get()) else 0
        pub = Publisher(max_val,  min_val, name="Station " + str(index + 1), missing_data_chance= missing_data_chance, corrupted_data_chance=corrupted_data_chance)
        self.publisher.append(pub)
        self.publisher_running.append(False)
        self.publisher_thread.append(Thread(target=self.publish_data, args=(index,)))
        
        toggle_button = tk.Button(self.root, text="Start/Stop Publisher " + str(index + 1), command=lambda i=index: self.toggle_publishing(i))
        toggle_button.grid(row=2 + index, column=0, pady=10, sticky='w')
        
        missing_data_description = tk.Label(root, text="Yes" if (self.missing_data_var.get()) else "No", anchor='w', justify='left')
        missing_data_description.grid(row=2 + index, column=1, columnspan=2, sticky='nsew')
        
        corrupted_data_description = tk.Label(root, text="Yes" if (self.corrupted_data_var.get()) else "No", anchor='w', justify='left')
        corrupted_data_description.grid(row=2 + index, column=2, columnspan=2, sticky='nsew')
        
        text_widget = tk.Text(self.root, height=4, width=40)
        text_widget.grid(row=2 + index, column=3, pady=10, sticky='nsew')
        self.publisher_log_text.append(text_widget)

        self.publisher_thread[index].start()
    
    # toggle publishing
    # @description - toggles the publishing of data
    def toggle_publishing(self, index): 
        self.publisher_running[index] = False if (self.publisher_running[index]) else True
    
    # publish data
    # @description - publishes data to the broker
    # @param index: the index of the publisher
    def publish_data(self, index):
        try:
            while (True):
                if self.publisher_running[index]:
                    packet = self.publisher[index].get_packet()
                    if packet is not None:
                        payload_str = json.dumps(packet)
                        self.publisher_log_text[index].insert(tk.END, "\t---\tStation " + str(index + 1) + "\t\t---\n")
                        self.publisher_log_text[index].insert(tk.END, "Timestamp:\t\t" + str(packet["timestamp"]) + "\n")
                        if type(packet["temperature"]) is str:
                            self.publisher_log_text[index].insert(tk.END, "Temperature:\t\t" + str(packet["temperature"]) + "\n")
                        elif packet["temperature"] is not None:
                            self.publisher_log_text[index].insert(tk.END, "Temperature:\t\t{:.1f}".format(round(packet["temperature"], 1)) + "°C\n")
                    else:
                        self.publisher_log_text[index].insert(tk.END, "\t---\tStation " + str(index + 1) + "\t\t---\n")
                        self.publisher_log_text[index].insert(tk.END, "Missing data detected\n")
                    self.client.publish("topic/data", payload_str)
                    self.publisher_log_text[index].see(tk.END)
                time.sleep(1)
        except Exception as e:
            self.publisher_log_text[index].insert(tk.END, f"Failed to publish message: {e}" + "\n")
            self.publisher_log_text[index].see(tk.END)
    
    def add_subscriber(self):
        print("Add subscriber")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()