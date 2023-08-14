1. Install Mosquitto:
Open a terminal and run the following command to install Mosquitto using Homebrew:
`brew install mosquitto`

2. Start Mosquitto service:
After installation, start the Mosquitto service using the following command:
`brew services start mosquitto`

3. Run the Publisher:
Navigate to the script directory. Then, run the script using the following command:   
`python publisher.py`

4. Run the Subscriber
Run the script:
`python subscriber.py`