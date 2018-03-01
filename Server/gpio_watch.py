import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

HOST = "192.168.1.132"
TOPIC_3 = "Hall_Effect"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code {}".format(str(rc)))
    error = rc
    return error

def on_disconnect(client, userdata, rc=0):
    print("Connection lost")
    client.loop_stop()

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect(HOST, 1883, 60)

# CH4 MPV:  BCM 15 / PHYS 10
# LOX MPV:  BCM 18 / PHYS 12
# CH4 VENT: BCM 14 / PHYS 08
# LOX VENT: BCM 04 / PHYS 07
# HI CH4:   BCM 17 / PHYS 11
# HI LOX:   BCM 27 / PHYS 13

# HIGH MEANS OPEN

pins = [15,18,14,4,17,27] # Keep numbers in order listed above

states = [0,0,0,0,0,0]

def pin_name(num):
    pin_index = pins.index(num)
    if(pin_index == 0):
        return "CH4 MPV "
    elif(pin_index == 1):
        return "LOX MPV "
    elif(pin_index == 2):
        return "CH4 VENT"
    elif(pin_index == 3):
        return "LOX VENT"
    elif(pin_index == 4):
        return "HI CH4  "
    elif(pin_index == 5):
        return "HI LOX"
    else:
        return "INVALID PIN"

def handler(pin_num):
    pin_index = pins.index(pin_num)
    if(states[pin_index]):
        print("{}: OPEN".format(pin_name(pin_num)))
        if(pin_index == 0):
            client.publish(TOPIC_3,b'CH4_MPV_OPEN')
            return;
        if(pin_index == 1):
            client.publish(TOPIC_3,b'LOX_MPV_OPEN')
            return;
        if(pin_index == 2):
            client.publish(TOPIC_3,b'CH4_VENT_OPEN')
            return;
        if(pin_index == 3):
            client.publish(TOPIC_3,b'LOX_VENT_OPEN')
            return;
        if(pin_index == 4):
            client.publish(TOPIC_3,b'CH4_HI_OPEN')
            return;
        if(pin_index == 5):
            client.publish(TOPIC_3,b'LOX_HI_OPEN')
            return;
    else:
        print("{}: CLOSED".format(pin_name(pin_num)))
        if(pin_index == 0):
            client.publish(TOPIC_3,b'CH4_MPV_CLOSED')
            return;
        if(pin_index == 1):
            client.publish(TOPIC_3,b'LOX_MPV_CLOSED')
            return;
        if(pin_index == 2):
            client.publish(TOPIC_3,b'CH4_VENT_CLOSED')
            return;
        if(pin_index == 3):
            client.publish(TOPIC_3,b'LOX_VENT_CLOSED')
            return;
        if(pin_index == 4):
            client.publish(TOPIC_3,b'CH4_HI_CLOSED')
            return;
        if(pin_index == 5):
            client.publish(TOPIC_3,b'LOX_HI_CLOSED')
            return;

# Load Starting Values
for i in range(6):
    pin = pins[i]
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin,GPIO.IN)
    states[i] = GPIO.input(pin)

while True:
    for i in range(6):
        pin = pins[i]
        if(states[i] != GPIO.input(pin)):
            states[i] = GPIO.input(pin)
            handler(pin)

client.loop_forever()
