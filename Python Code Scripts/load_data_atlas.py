from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json
import threading
import pymongo as pym #database client package for python

#atlas db address
myclient = pym.MongoClient("") #copy paste the connection string here

mydb = myclient["add232iotdb"] #database name
temp_data = mydb["humidity"] #collection name

ENDPOINT = ""#aws broker url
CLIENT_ID = "" put here client id
PATH_TO_CERTIFICATE = ""#.pem.crt
PATH_TO_PRIVATE_KEY = ""#private.pem.key
PATH_TO_AMAZON_ROOT_CA_1 = ""#root ca


event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection_app = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )

print("Connecting to {} with client ID '{}'...".format(ENDPOINT, CLIENT_ID))

connect_future_app = mqtt_connection_app.connect()
connect_future_app.result()
print("Connected!")

def on_message_received_temp(topic, payload, dup, qos, retain):
     
     print(f"Message received from topic {topic}: {payload}")
     data_dict = json.loads(payload.decode('utf-8'))
     humidity = data_dict.get('hum')
     timestamp = data_dict.get('time')
     temp = data_dict.get('temp')
     print(f"Parsed Data - Time: {timestamp}, Temp: {temp}, Humidity: {humidity}")
     
     temp_data.insert_one({"humidity":humidity,"time":timestamp,"temperature":temp})
     print("Data inserted into MongoDB")

    
#subscribing to a topic therm/temp1
topic_temp = "hum/hum1"     
subscribe_future, packet_id = mqtt_connection_app.subscribe(
    topic=topic_temp,
    qos=mqtt.QoS.AT_LEAST_ONCE,
    callback=on_message_received_temp
    )
    

subscribe_result = subscribe_future.result()
print(f'Subscribed to {topic_temp}')

threading.Event().wait()
