#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <MQTTClient.h>

#include "config.h"

volatile MQTTClient_deliveryToken deliveredToken;

void delivered(void *context, MQTTClient_deliveryToken dt){
	printf("Message with token value %d delivery confirmed\n", dt);
	deliveredToken = dt;
}

int msgarrvd(void *context, char *topicName, int topicLen, MQTTClient_message *message){
	int i;
	char* payloadptr;

	printf("Message arrived\n");
	printf("        topic: %s\n", topicName);
	printf("    message: ");

	payloadptr = message->payload;
	for(i = 0; i < message->payloadlen; i++){
		putchar(*payloadptr++);
	}

	putchar('\n');
	MQTTClient_freeMessage(&message);
	MQTTClient_free(topicName);
	return 1;
}

void connlost(void *context, char *cause){
	printf("\nConnection lost\n");
	printf("      cause: %s\n", cause);
}

int main(int argc, char *argv[]){
	MQTTClient client;

	MQTTClient_connectOptions conn_opts = MQTTClient_connectOptions_initializer;
	MQTTClient_message pubmsg = MQTTClient_message_initializer;
	MQTTClient_deliveryToken token;
	int rc;

	MQTTClient_create(&client, address, clientid, MQTTCLIENT_PERSISTENCE_NONE, NULL);
	conn_opts.keepAliveInterval = 20;
	conn_opts.cleansession = 1;

	MQTTClient_setCallbacks(client, NULL, connlost, msgarrvd, delivered);

	if((rc = MQTTClient_connect(client, &conn_opts)) != MQTTCLIENT_SUCCESS){
		printf("Failed to connect, return code %d\n", rc);
		exit(EXIT_FAILURE);
	}

	char *payload = "Test Payload";
	char *topic = topic_1;

	pubmsg.payload = payload;
	pubmsg.payloadlen = strlen(payload);
	pubmsg.qos = QOS;
	pubmsg.retained = 0;
	MQTTClient_publishMessage(client, topic, &pubmsg, &token);
	printf("Waiting for publication of %s\n"
			"on topic %s for client with ClientID: %s\n",
			payload, topic, clientid);
	while(deliveredToken != token);
	MQTTClient_disconnect(client, 10000);
	MQTTClient_destroy(&client);
	return rc;
}
