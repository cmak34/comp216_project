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

class GUI:
    # constructor for the GUI
    # @description - creates the GUI and sets up the widgets
    # @param root: the root window of tkinter
    def __init__(self, root):
        self.root = root
        self.max_val = 50.0 # max value for temperature
        self.min_val = -50.0 # min value for temperature
        self.root.title("MQTT Data Publisher")

        # Configure the grid weights
        for i in range(5):
            self.root.grid_rowconfigure(i, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

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
        2. Click on the "Start Publishing" button to start publishing data
        3. Temperature data will be published to the broker every 1 second 
           using random values between -40°C and 50°C with noise and following a sine wave pattern
        """, anchor='w', justify='left')
        self.proj_description.grid(row=0, column=0, columnspan=2, sticky='nsew')
        # publisher 1
        self.publisher1 = None
        self.publisher1_running = False
        self.publisher1_thread = None
        self.publisher1_label = tk.Label(root, text="Station A:\nNormal Station", justify='left', anchor='w')
        self.publisher1_label.grid(row=1, column=0, sticky='nsew')
        self.publisher1_start_button = tk.Button(root, text="Start Publishing", command=self.start_publishing1)
        self.publisher1_start_button.grid(row=2, column=0, pady=10, sticky='nsew')
        self.publisher1_stop_button = tk.Button(root, text="Stop Publishing", command=self.stop_publishing1)
        self.publisher1_stop_button.grid(row=3, column=0, pady=10, sticky='nsew')
        self.publisher1_log_text = tk.Text(root, height=10, width=40)
        self.publisher1_log_text.grid(row=4, column=0, pady=10, sticky='nsew')
        
        # publisher 2
        self.publisher2 = None
        self.publisher2_running = False
        self.publisher2_thread = None
        self.publisher2_label = tk.Label(root, text="Station B:\n10% chance of missing data and \n10% chance of corrupted data", justify='left', anchor='w')
        self.publisher2_label.grid(row=1, column=1, sticky='nsew')
        self.publisher2_start_button = tk.Button(root, text="Start Publishing", command=self.start_publishing2)
        self.publisher2_start_button.grid(row=2, column=1, pady=10, sticky='nsew')
        self.publisher2_stop_button = tk.Button(root, text="Stop Publishing", command=self.stop_publishing2)
        self.publisher2_stop_button.grid(row=3, column=1, pady=10, sticky='nsew')
        self.publisher2_log_text = tk.Text(root, height=10, width=40)
        self.publisher2_log_text.grid(row=4, column=1, pady=10, sticky='nsew')

        # counter
        self.counter_running = False
        self.counter = 0
        self.counter_lock = threading.Lock()
        self.counter_thread = Thread(target=self.counter_incremental)
        self.counter_thread.daemon = True
        self.counter_thread.start()

        # connect to the broker
        self.client = mqtt.Client()
        try:
            self.client.connect("localhost", 1883, 60)
        except ConnectionRefusedError:
            print("Connection to MQTT broker refused. Make sure the broker is running.")
            return
    
    # function to start_publishing for publisher 1
    # @description - starts the publisher thread
    def start_publishing1(self):
        with self.counter_lock:
            if not self.counter_running:
                self.counter_running = True
            if not self.publisher1_running:
                self.publisher1_running = True
                self.publisher1 = Publisher(self.max_val, self.min_val, name="Station A", missing_data_chance=0, corrupted_data_chance=0)
                self.publisher1_thread = Thread(target=self.publish_data1)
                self.publisher1_thread.start()

    # function to start_publishing for publisher 2
    # @description - starts the publisher thread    
    def start_publishing2(self):
        with self.counter_lock:
            if not self.counter_running:
                self.counter_running = True
            if not self.publisher2_running:
                self.publisher2_running = True
                self.publisher2 = Publisher(self.max_val, self.min_val, name="Station B", missing_data_chance=10, corrupted_data_chance=10)
                self.publisher2_thread = Thread(target=self.publish_data2)
                self.publisher2_thread.start()
    
    # function to stop_publishing for publisher 1
    # @description - stops the publisher thread
    def stop_publishing1(self):
        if self.publisher1_running:
            self.publisher1 = None
            self.publisher1_running = False
            if (not self.publisher2_running): 
                self.counter_running = False
    
    # function to stop_publishing for publisher 2
    # @description - stops the publisher thread
    def stop_publishing2(self):
        if self.publisher2_running:
            self.publisher2 = None
            self.publisher2_running = False
            if (not self.publisher1_running): 
                self.counter_running = False
    
    # function to increment the counter
    # @description - increments the counter every 1 second
    def counter_incremental(self):
        while (True):
            while (self.counter_running):
                with self.counter_lock:
                    self.counter += 1
                time.sleep(1)
    
    # function to publish data to broker for publisher 1
    # @description - publishes data to the broker with same topic
    def publish_data1(self):
        try:
            while self.publisher1 and self.publisher1_running:
                packet = self.publisher1.get_packet()
                if packet is not None:
                    packet["counter"] = self.counter
                    payload_str = json.dumps(packet)    
                    self.publisher1_log_text.insert(tk.END, "Station:\t\t" + str(packet["station_name"]) + "\n")
                    self.publisher1_log_text.insert(tk.END, "Counter:\t\t" + str(packet["counter"]) + "\n")
                    self.publisher1_log_text.insert(tk.END, "Timestamp:\t\t" + str(packet["timestamp"]) + "\n")
                    if type(packet["temperature"]) is str: 
                        self.publisher1_log_text.insert(tk.END, "Temperature:\t\t" + str(packet["temperature"]) + "\n\n")
                    elif packet["temperature"] < self.max_val and packet["temperature"] > self.min_val: 
                        self.publisher1_log_text.insert(tk.END, "Temperature:\t\t{:.1f}".format(round(packet["temperature"], 1)) + "°C\n\n")
                    elif packet["temperature"] > self.max_val or packet["temperature"] < self.min_val:
                        self.publisher1_log_text.insert(tk.END, "Temperature:\t\t" + str(packet["temperature"]) + " is out of range" + "\n\n")    
                else: 
                    self.publisher1_log_text.insert(tk.END, "Missing data detected\n\n")
                self.client.publish("topic/data", payload_str)
                self.publisher1_log_text.insert(tk.END, "-"*10 + "\n\n")
                self.publisher1_log_text.see(tk.END)
                time.sleep(1)
        except Exception as e:
            self.publisher1_log_text.insert(tk.END, f"Failed to publish message: {e}" + "\n")
            self.publisher1_log_text.see(tk.END)
    
    # function to publish data to broker for publisher 2
    # @description - publishes data to the broker with same topic
    def publish_data2(self):
        try:
            while self.publisher2 and self.publisher2_running:
                packet = self.publisher2.get_packet()
                if packet is not None:
                    packet["counter"] = self.counter
                    payload_str = json.dumps(packet)    
                    self.publisher2_log_text.insert(tk.END, "Station:\t\t" + str(packet["station_name"]) + "\n")
                    self.publisher2_log_text.insert(tk.END, "Counter:\t\t" + str(packet["counter"]) + "\n")
                    self.publisher2_log_text.insert(tk.END, "Timestamp:\t\t" + str(packet["timestamp"]) + "\n")
                    if type(packet["temperature"]) is str: 
                        self.publisher2_log_text.insert(tk.END, "Temperature:\t\t" + str(packet["temperature"]) + "\n\n")
                    elif packet["temperature"] < self.max_val and packet["temperature"] > self.min_val: 
                        self.publisher2_log_text.insert(tk.END, "Temperature:\t\t{:.1f}".format(round(packet["temperature"], 1)) + "°C\n\n")
                    elif packet["temperature"] > self.max_val or packet["temperature"] < self.min_val:
                        self.publisher2_log_text.insert(tk.END, "Temperature:\t\t" + str(packet["temperature"]) + " is out of range" + "\n\n")    
                else: 
                    self.publisher2_log_text.insert(tk.END, "Missing data detected\n\n")
                self.client.publish("topic/data", payload_str)
                self.publisher2_log_text.insert(tk.END, "-"*10 + "\n\n")
                self.publisher2_log_text.see(tk.END)
                time.sleep(1)
        except Exception as e:
            self.publisher2_log_text.insert(tk.END, f"Failed to publish message: {e}" + "\n")
            self.publisher2_log_text.see(tk.END)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()