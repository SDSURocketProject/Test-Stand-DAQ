CC=tcc
CFLAGS=-L/usr/local/lib -lpaho-mqtt3c

client:
	@echo [CC] client.c
	@${CC} client.c -o client ${CFLAGS}

clean:
	@echo cleaning
	@echo rm client
	@rm client
