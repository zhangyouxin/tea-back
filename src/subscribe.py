import paho.mqtt.client as mqtt
import time
import logging
import os
import re
import psycopg2
from enum import Enum, unique
logging.basicConfig(filename= './log/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

HOST = 'localhost'
PORT = 1883

@unique
class Topic(Enum):
    CL_Up = r'(stds\/up\/CL\/)(\d+)'           
    CL_Offline = r'(stds\/offline\/CL\/)(\d+)'  

    SYS_Up = r'(stds\/up\/sys\/)(\d+)' 
    SYS_Down = r'(stds\/down\/sys\/)(\d+)'
    SYS_Offline = r'(stds\/offline\/sys\/)(\d+)'

    CT_Up = r'(stds\/up\/CT\/)(\d+)'   
    CT_Down_Switch = r'(stds\/down\/CT\/)(\d+)\/(switch)' 
    CT_Down_Loop = r'(stds\/down\/CT\/)(\d+)\/(loop)' 
    CT_Offline = r'(stds\/offline\/CT\/)(\d+)' 

topReg = r'stds\/(.*?)(\d+)'

conn = psycopg2.connect(database="mosquitto", user="root",
                        password="dev", host="localhost", port="5432")
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
        logging.warning("[Debug] extracted subTopic :", subTopic , 'deviceNo: ', deviceNo, 'msg: ', str(msg.payload))
        save_to_database(subTopic, deviceNo, str(msg.payload))

def save_to_database(subTopic, deviceNo, msg):
    sqlTemp = "insert into messages(sub_topic, device_no, message) values ('{0}', '{1}', '{2}')"
    sql = sqlTemp.format(subTopic, deviceNo, msg)
    logging.warning('insert sql: ', sql)
    cur.execute(sql)
    conn.commit()

if __name__ == '__main__':
    client_loop()