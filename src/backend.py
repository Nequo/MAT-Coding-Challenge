import paho.mqtt.client as mqtt
import time

broker_address = "127.0.0.1"


def on_connect(client, userdata, flags, rc):
    client.subscribe("carCoordinates")

def on_message(client, userdata, message):
    print("Received: ", str(message.payload.decode("utf-8")))

client = mqtt.Client("Positions")
client.on_message = on_message
client.on_connect = on_connect

try:
    client.connect(broker_address)
except:
    print("Could not connect to broker, are you sure you ran docker-compose up?")
    exit(1)

client.loop_start()
time.sleep(4)
client.loop_stop()
