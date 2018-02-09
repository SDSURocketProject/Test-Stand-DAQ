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
client.subscribe(TOPIC_1)

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


def relay1_on():
	RELAY.relayON(0,1)
	print("Relay 1 ON")
	client.publish(TOPIC_2,"Relay_1_ON.")
	return

def relay2_on():
	RELAY.relayON(0,2)
	print("Relay 2 ON")
	client.publish(TOPIC_2,b"Relay_2_ON.")
	return

def relay3_on():
	RELAY.relayON(0,3)
	print("Relay 3 ON")
	client.publish(TOPIC_2,b"Relay_3_ON.")
	return

def relay4_on():
	RELAY.relayON(0,4)
	print("Relay 4 ON")
	client.publish(TOPIC_2,b"Relay_4_ON.")
	return

def relay5_on():
	RELAY.relayON(0,5)
	print("Relay 5 ON")
	client.publish(TOPIC_2,b"Relay_5_ON.")
	return

def relay6_on():
	RELAY.relayON(0,6)
	print("Relay 6 ON")
	client.publish(TOPIC_2,b"Relay_6_ON.")
	return

def relay1_off():
	RELAY.relayOFF(0,1)
	print("Relay 1 OFF")
	client.publish(TOPIC_2,b"Relay_1_OFF.")
	return

def relay2_off():
	RELAY.relayOFF(0,2)
	print("Relay 2 OFF")
	client.publish(TOPIC_2,b"Relay_2_OFF.")
	return

def relay3_off():
	RELAY.relayOFF(0,3)
	print("Relay 3 OFF")
	client.publish(TOPIC_2,b"Relay_3_OFF.")
	return

def relay4_off():
	RELAY.relayOFF(0,4)
	print("Relay 4 OFF")
	client.publish(TOPIC_2,b"Relay_4_OFF.")
	return

def relay5_off():
	RELAY.relayOFF(0,5)
	print("Relay 5 OFF")
	client.publish(TOPIC_2,b"Relay_5_OFF.")
	return

def relay6_off():
	RELAY.relayOFF(0,6)
	print("Relay 6 OFF")
	client.publish(TOPIC_2,b"Relay_6_OFF.")
	return

def	send_pressures(data):
	client.publish(TOPIC_3,str(data))
	return



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Main Loop
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# Our main loop is the listener or the TCP connection. It listens for 'data' and 
# uses this data to analyze what is being requested on the Launch Control Client. Data
# that is receieved requesting valve or ignitor actuation simply jumps into the correct
# function listed above. If sensor information is requested, new threads are started that
# use the target function specified to send sensor information back to the client software.


def calldata(data):
	print(data)
	if 'ducers' in data:
		send_pressures(str(data))

	elif 'relay1_open' in data:
		print ("Received data: ",data)
		relay1_on()

	elif 'relay2_open' in data:
		print ("Received data: ",data)
		relay2_on()

	elif 'relay3_open' in data:
		print ("Received data: ",data)
		relay3_on()

	elif 'relay4_open' in data:
		print ("Received data: ",data)
		relay4_on()

	elif 'relay5_open' in data:
		print ("Received data: ",data)
		relay5_on()

	elif 'relay6_open' in data:
		print ("Received data: ",data)
		relay6_on()

	elif 'relay1_close' in data:
		print ("Received data: ",data)
		relay1_off()

	elif 'relay2_close' in data:
		print ("Received data: ",data)
		relay2_off()

	elif 'relay3_close' in data:
		print ("Received data: ",data)
		relay3_off()

	elif 'relay4_close' in data:
		print ("Received data: ",data)
		relay4_off()

	elif 'relay5_close' in data:
		print ("Received data: ",data)
		relay5_off()

	elif 'relay6_close' in data:
		print ("Received data: ",data)
		relay6_off()

client.loop_forever()