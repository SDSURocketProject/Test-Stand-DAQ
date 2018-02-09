import piplates.RELAYplate as RELAY
import paho.mqtt.client as mqtt

HOST = "192.168.1.132"
TOPIC_1 = "Valve_Commands"
TOPIC_2 = "Valve_Readings"

print ("\nTest Stand Server Ready.")
print (("Please connect client software to: %s at port: %d \n") % (HOST, 1883))
print ("Waiting to establish connection........ \n")

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe(TOPIC_1)
	error = rc
	return error

def on_disconnect(client, userdata,rc=0):
	print("Connection Lost.")
	client.loop_stop()

def on_message(client, userdata, msg):
	calldata(str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
#client.on_publish = on_publish
client.on_disconnect = on_disconnect
client.connect(HOST, 1883, 60)

print ("Connection established.")
#print ('Connection address: ',addr)
#logger.debug("Connection established at {}".format(time.asctime())) #find what the ip is
print ("Awaiting commands... \n")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Feedback Logging Setup
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#setting up the logging program
#all of the logging events will be put into a text file wherever the location is specified
#the location can be specified by setting the "filename" equal to "anyname.log"
#if the logging filname is kept the same, the logging events will be put in the same file, adding to past events.


#logname = time.strftime("LC_ServerLog(%H_%M_%S).log",time.localtime())
#logger = logging.getLogger("")                                                                 
#logging.basicConfig(filename=logname, level=logging.DEBUG)


def lox_hi_open():
	RELAY.relayON(0,1)
	print("LOX HI OPENED")
	client.publish(TOPIC_2,b'LOXHIOPEN')
	return

def meth_hi_open():
	RELAY.relayON(0,3)
	print("METH HI OPENED")
	client.publish(TOPIC_2,b'METHHIOPEN')
	return

def meth_vent_open():
	RELAY.relayOFF(0,2)
	print("METH VENT OPENED")
	client.publish(TOPIC_2,b'METHVENTOPEN')
	return

def lox_vent_open():
	RELAY.relayOFF(0,4)
	print("LOX VENT OPENED")
	client.publish(TOPIC_2,b'LOXVENTOPEN')
	return

def meth_mpv_open():
	RELAY.relayON(0,5)
	print("METH MPV OPENED")
	client.publish(TOPIC_2,b'METHMPVOPEN')
	return

def lox_mpv_open():
	RELAY.relayON(0,6)
	print("LOX MPV OPENED")
	client.publish(TOPIC_2,b'LOXMPVOPEN')
	return

def purge_open():
	RELAY.relayON(1,1)
	print("PURGE OPENED")
	client.publish(TOPIC_2,b'PURGEOPEN')
	return

def vents_open():
	RELAY.relayOFF(0,2)
	RELAY.relayOFF(0,4)
	print("VENTS OPENED")
	client.publish(TOPIC_2,b'VENTSOPEN')
	return

def main_open():
	RELAY.relayON(0,5)
	RELAY.relayON(0,6)
	print("MPV OPENED")
	client.publish(TOPIC_2,b'MAINOPEN')
	return

def ignite_on():
	RELAY.relayON(1,2)
	print("IGNITOR ON")
	client.publish(TOPIC_2,b'IGNITEON')
	return

def relay7_on():
	RELAY.relayON(0,7)
	print("Relay 7 ON")
	client.publish(TOPIC_2,b'R7ON')
	return

def lox_hi_close():
	RELAY.relayOFF(0,1)
	print("LOX HI CLOSED")
	client.publish(TOPIC_2,b'LOXHICLOSE')
	return

def meth_hi_close():
	RELAY.relayOFF(0,3)
	print("METH HI CLOSED")
	client.publish(TOPIC_2,b'METHHICLOSE')
	return

def meth_vent_close():
	RELAY.relayON(0,2)
	print("METH VENT CLOSED")
	client.publish(TOPIC_2,b'METHVENTCLOSE')
	return

def lox_vent_close():
	RELAY.relayON(0,4)
	print("LOX VENT CLOSED")
	client.publish(TOPIC_2,b'LOXVENTCLOSE')
	return

def meth_mpv_close():
	RELAY.relayOFF(0,5)
	print("METH MPV CLOSED")
	client.publish(TOPIC_2,b'METHMPVCLOSE')
	return

def lox_mpv_close():
	RELAY.relayOFF(0,6)
	print("LOX MPV CLOSED")
	client.publish(TOPIC_2,b'LOXMPVCLOSE')
	return

def purge_close():
	RELAY.relayOFF(1,1)
	print("PURGE CLOSED")
	client.publish(TOPIC_2,b'PURGECLOSE')
	return

def vents_close():
	RELAY.relayON(0,2)
	RELAY.relayON(0,4)
	print("VENTS CLOSED")
	client.publish(TOPIC_2,b'VENTSCLOSE')
	return

def main_close():
	RELAY.relayOFF(0,5)
	RELAY.relayOFF(0,6)
	print("MPV CLOSED")
	client.publish(TOPIC_2,b'MAINCLOSE')
	return

def ignite_off():
	RELAY.relayOFF(1,2)
	print("IGNITOR OFF")
	client.publish(TOPIC_2,b'IGNITEOFF')
	return

def relay7_off():
	RELAY.relayOFF(0,7)
	print("Relay 7 OFF")
	client.publish(TOPIC_2,b'R7OFF')
	return

def launch():
	RELAY.relayON(0,5)
	RELAY.relayON(0,6)
	print("MPV OPENED")
	client.publish(TOPIC_2,b'MAINOPEN')
	return

def abort():
	#HI need to close, mpvs need to close, vents need to open, and ignitor off
	RELAY.relayOFF(0,1)
	RELAY.relayOFF(0,3)
	RELAY.relayOFF(0,5)
	RELAY.relayOFF(0,6)
	RELAY.relayOFF(0,2)
	RELAY.relayOFF(0,4)
	print("ABORT")
	client.publish(TOPIC_2,b'ABORT')
	return

def relay_state():
	states = RELAY.relaySTATE(0)
	print(states)
	client.publish(TOPIC_2,str(states))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Main Loop
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# Our main loop is the listener or the TCP connection. It listens for 'data' and 
# uses this data to analyze what is being requested on the Launch Control Client. Data
# that is receieved requesting valve or ignitor actuation simply jumps into the correct
# function listed above. If sensor information is requested, new threads are started that
# use the target function specified to send sensor information back to the client software.

'''
#########RELAYS###########
relay 1: LOX HI VALVE
relay 2: METH HI VALVE
relay 3: METH VENT VALVE
relay 4: LOX VENT VALVE
relay 5: METH MPV
relay 6: LOX MPV
relay 7: Nothing
relay 8: PURGE
'''

def calldata(data):

	print("data is {}".format(data))

	if 'LOX_HI_open' in data:
		print ("Received data: ",data)
		lox_hi_open()

	elif 'METH_HI_open' in data:
		print ("Received data: ",data)
		meth_hi_open()

	elif 'METH_VENT_open' in data:
		print ("Received data: ",data)
		meth_vent_open()

	elif 'LOX_VENT_open' in data:
		print ("Received data: ",data)
		lox_vent_open()

	elif 'METH_MPV_open' in data:
		print ("Received data: ",data)
		meth_mpv_open()

	elif 'LOX_MPV_open' in data:
		print ("Received data: ",data)
		lox_mpv_open()

	elif 'PURGE_open' in data:
		print ("Received data: ",data)
		purge_open()

	elif 'VENTS_open' in data:
		print ("Received data: ",data)
		vents_open()

	elif 'MAIN_open' in data:
		print ("Received data: ",data)
		main_open()

	elif 'IGNITE_on' in data:
		print ("Received data: ",data)
		ignite_on()

	elif 'relay7_open' in data:
		print ("Received data: ",data)
		relay7_on()

	elif 'LOX_HI_close' in data:
		print ("Received data: ",data)
		lox_hi_close()

	elif 'METH_HI_close' in data:
		print ("Received data: ",data)
		meth_hi_close()

	elif 'METH_VENT_close' in data:
		print ("Received data: ",data)
		meth_vent_close()

	elif 'LOX_VENT_close' in data:
		print ("Received data: ",data)
		lox_vent_close()

	elif 'METH_MPV_close' in data:
		print ("Received data: ",data)
		meth_mpv_close()

	elif 'LOX_MPV_close' in data:
		print ("Received data: ",data)
		lox_mpv_close()

	elif 'PURGE_close' in data:
		print ("Received data: ",data)
		purge_close()

	elif 'VENTS_close' in data:
		print ("Received data: ",data)
		vents_close()

	elif 'MAIN_close' in data:
		print ("Received data: ",data)
		main_close()

	elif 'IGNITE_off' in data:
		print ("Received data: ",data)
		ignite_off()

	elif 'abort' in data:
		print ("Received data: ",data)
		abort()

	elif 'relay7_close' in data:
		print ("Received data: ",data)
		relay7_off()


client.loop_forever()
print("testing again")
