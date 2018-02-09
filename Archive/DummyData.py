import time
import random
import math
import datetime
import paho.mqtt.client as mqtt

def mqtt_init():
    print("attempting new mqtt init...")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.connect(host, 1883, 60)
    client.subscribe(valve_command_topic)
    client.subscribe(safe_abort_topic)
    print('client connected')
    return client

def echo_data():
    seed_data = time.time()
    random.seed(seed_data)
    
    #create fake valve states (randomly open small percentage of time)
    #normally server would read data from the valve feedback sensor  
    # layout -> [v0, v1, v2...v7]
    relays = [(random.random() >= 0.90) for sensor in range(8)]

    #create fake pressure transducer and thermocouple data
    #normally server would read data from the ADC board
    # layout -> [p0, p1, p2, p3, t0, t1, t2, t3...t9]
    sensors = [random.uniform(0,100) for sensor in range(14)]

    # PUBLISH ANY OUTGOING DATA HERE
    #publish generated values to mqtt broker - data will become available for clients
    client.publish(valve_states_topic, ",".join(str(x) for x in relays))
    client.publish(data_sensors_topic, ",".join(str(x) for x in sensors))

    return relays + sensors
    
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    return rc

def on_disconnect(client, userdata,rc=0):
    print("Connection Lost. Attempting to reconnect...")
    client.loop_stop()
    client = mqtt_init()

def on_message(client, userdata, msg):
	parse_message(str(msg.payload))

def parse_message(message):
    print(message)

def main_loop():
    print("main loop started...")

    while True:
        print("Echo Data: " + str(echo_data()))
        time.sleep(0.5)

# OBJECTS #
# Topic Name | Topic Description
# 1 | Valve States  (publish)
# 2 | Valve Command (subscribe)
# 3 | Transducer Data/Thermocouple Data (publish)2
# 4 | Load Cell/GPS/IMU/TVC Position Feedback (publish)
# 5 | Safe/Alert/Panic/Launch (publish/subscribe)
#       ...(0 - Safe, 1 - Alert, 2 - Panic, 3 - Abort, 4 - Launch)

# Panic State
SAFE_ALERT_PANIC_ABORT_LAUNCH = 0 

# IP address of mqtt broker - localhost/127.0.0.1 if on local machine
host = "localhost"	

#mqtt broker topic string definitions
valve_states_topic = "1"
valve_command_topic = "2"
data_sensors_topic = "3"
data_telemetry_topic = "4"
safe_abort_topic = "5"

#init mqtt client connection and begin echo/listen loop
client = mqtt_init()
print("about to begin main loop...")
main_loop()

# end of program