1. Install Mosquitto, tkinter, paho-mqtt:
Open a terminal and run the following command to install Mosquitto using Homebrew:
`brew install mosquitto`
`pip install paho-mqtt`
`brew install python-tk@3.9` <your python version>

1. Start Mosquitto service:
After installation, start the Mosquitto service using the following command:
`brew services start mosquitto`

2. Run the GUI:
Navigate to the script directory. Then, run the script using the following command:   
`python gui.py`