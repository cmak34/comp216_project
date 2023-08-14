import tkinter as tk
import paho.mqtt.client as mqtt
import numpy as np
from publisher import Publisher
import paho.mqtt.client as mqtt
import json
import time
import random
from threading import Thread

class GUI:
    def __init__(self, root):
        self.root = root
        self.max_val = 50 # max value for temperature
        self.min_val = -40 # min value for temperature
        self.root.title("MQTT Data Publisher")
        self.proj_description = tk.Label(root, text="2 Publishers is running. Please choose one of them to start publishing.")
        self.proj_description.grid(row=0, column=0)
        
        # publisher 1
        self.publisher1 = None
        self.publisher1_running = False
        self.publisher1_thread = None
        self.publisher1_label = tk.Label(root, text="Publisher 1:")
        self.publisher1_label.grid(row=1, column=0)
        self.publisher1_start_button = tk.Button(root, text="Start Publishing", command=self.start_publishing1)
        self.publisher1_start_button.grid(row=2, column=0, pady=10)
        self.publisher1_stop_button = tk.Button(root, text="Stop Publishing", command=self.stop_publishing1)
        self.publisher1_stop_button.grid(row=3, column=0, pady=10)
        self.publisher1_log_text = tk.Text(root, height=10, width=40)
        self.publisher1_log_text.grid(row=4, column=0, pady=10)
        

        
        # publisher 2
        self.publisher2 = None
        self.publisher2_running = False
        self.publisher2_thread = None
        self.publisher2_label = tk.Label(root, text="Publisher 2:")
        self.publisher2_label.grid(row=1, column=1)
        self.publisher2_start_button = tk.Button(root, text="Start Publishing", command=self.start_publishing2)
        self.publisher2_start_button.grid(row=2, column=1, pady=10)
        self.publisher2_stop_button = tk.Button(root, text="Stop Publishing", command=self.stop_publishing2)
        self.publisher2_stop_button.grid(row=3, column=1, pady=10)
        self.publisher2_log_text = tk.Text(root, height=10, width=40)
        self.publisher2_log_text.grid(row=4, column=1, pady=10)
    
    def start_publishing1(self):
        if not self.publisher1_running:
            self.publisher1 = Publisher(self.max_val, self.min_val)
            self.publisher1_thread = Thread(target=self._publish_data1)
            self.publisher1_thread.start()
            self.publisher1_running = True
            self.log("Publisher 1 publishing.")
        
    def start_publishing2(self):
        if not self.publisher2_running:
            self.publisher2 = Publisher(self.max_val, self.min_val)
            self.publisher2_thread = Thread(target=self._publish_data2)
            self.publisher2_thread.start()
            self.publisher2_running = True
            self.log("Publisher 2 publishing.")
    
    def stop_publishing1(self):
        if self.publisher1_running:
            self.publisher1 = None
            self.publisher1_running = False
            self.log("Publisher 1 Stopped publishing.")
        
    def stop_publishing2(self):
        if self.publisher2_running:
            self.publisher2 = None
            self.publisher2_running = False
            self.log("Publisher 2 Stopped publishing.")
    
    def _publish_data1(self):
        client = mqtt.Client()
        try:
            client.connect("localhost", 1883, 60)
        except ConnectionRefusedError:
            self.log("Connection to MQTT broker refused. Make sure the broker is running.")
            return

        while self.publisher1 and self.publisher1_running:
            packet = self.publisher1.get_packet()
            if packet:  # Ensure packet is not None
                payload_str = json.dumps(packet)
                try:
                    client.publish("topic/data", payload_str)
                    self.publisher1_log_text.insert(tk.END, "Published data:\n" + payload_str + "\n")
                    self.publisher1_log_text.see(tk.END)
                except mqtt.MQTTException as e:
                    self.publisher1_log_text.insert(tk.END, f"Failed to publish message: {e}" + "\n")
                    self.publisher1_log_text.see(tk.END)
            time.sleep(1)
        client.disconnect()
    
    def _publish_data2(self):
        client = mqtt.Client()
        try:
            client.connect("localhost", 1883, 60)
        except ConnectionRefusedError:
            self.log("Connection to MQTT broker refused. Make sure the broker is running.")
            return

        while self.publisher2 and self.publisher2_running:
            packet = self.publisher2.get_packet()
            if packet:  # Ensure packet is not None
                payload_str = json.dumps(packet)
                try:
                    client.publish("topic/data", payload_str)
                    self.publisher2_log_text.insert(tk.END, "Published data:\n" + payload_str + "\n")
                    self.publisher2_log_text.see(tk.END)
                except mqtt.MQTTException as e:
                    self.publisher2_log_text.insert(tk.END, f"Failed to publish message: {e}" + "\n")
                    self.publisher2_log_text.see(tk.END)
            time.sleep(1)
        client.disconnect()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()