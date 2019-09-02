import paho.mqtt.client as mqtt
import time
import logging
import os
logging.basicConfig(filename= './log/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

HOST = 'localhost'
PORT = 1883

def client_loop():
    client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    client = mqtt.Client(
    client_id=client_id, clean_session=True)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOST, PORT, 60)
    client.loop_forever()

def on_connect(client, userdata, flags, rc):
    logging.warning('Connected with result code ' + str(rc))
    client.subscribe('/topic1')

def on_message(client, userdata, msg):
    logging.warning(msg.topic + ' ' + msg.payload.decode('utf-8'))
    print(msg.topic + ' ' + msg.payload.decode('utf-8'))

if __name__ == '__main__':
    client_loop()