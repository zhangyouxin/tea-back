import paho.mqtt.client as mqtt
import time
import logging
import os
import re
import psycopg2
logging.basicConfig(filename= './log/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

HOST = 'localhost'
PORT = 1883

topReg = r'stds\/(.*?)(\d+)'

conn = psycopg2.connect(database="mosquitto", user="root",
                        password="dev", host=HOST, port="5432")
cur = conn.cursor()
logging.warning('Opened database successfully')

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
    cur = conn.cursor()
    client.subscribe("#")

def on_message(client, userdata, msg):
    logging.warning("[Info] Message received: " + msg.topic + " " + str(msg.payload))
    topic = msg.topic 
    res = re.search(topReg, topic)
    if res == None:
        logging.warning("[Debug] No Topic extracted for: " + topic)
    else:
        subTopic = res.group(1)
        deviceNo = res.group(2)
        logging.warning("[Debug] extracted subTopic :" + subTopic)
        logging.warning("[Debug] extracted deviceNo :" + deviceNo, )
        logging.warning("[Debug] extracted msg :" +  str(msg.payload))
        save_to_database(subTopic, deviceNo, str(msg.payload))

def save_to_database(subTopic, deviceNo, msg):
    sqlTemp = "insert into messages(sub_topic, device_no, message) values ('{0}', '{1}', '{2}')"
    sql = sqlTemp.format(subTopic, deviceNo, msg)
    logging.warning('insert sql: ' + sql)
    cur.execute(sql)
    conn.commit()

if __name__ == '__main__':
    client_loop()