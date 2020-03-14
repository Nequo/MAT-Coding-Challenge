import paho.mqtt.client as mqtt
import time
from scipy import spatial

import helpers
import csv
import json

broker_address = "127.0.0.1"


# Get track points from csv file at the start
data = list(csv.reader(open("./lap.csv"), quoting=csv.QUOTE_NONNUMERIC))
# Generate the tree only once
track_tree = spatial.KDTree(data)

car_laps = [0] * 6
car_sector = [0] * 6

def on_connect(client, userdata, flags, rc):
    client.subscribe("carCoordinates")

def on_message(client, userdata, message):
    recv_string = str(message.payload.decode("utf-8"))
    carIndex, lat, longitude, timestamp = helpers.gen_carCoordinates(recv_string)

    car_sector[carIndex] = helpers.closest_sector(track_tree, lat, longitude)
    # Add a lap every time a car passes sector 1
    if car_sector[carIndex] == 1:
        print("Lap!")
        car_laps[carIndex] += 1
    print(car_laps)
    pos = helpers.car_position(carIndex, car_sector, car_laps)

    carStat = helpers.gen_carStatus(timestamp, carIndex , "POSITION", pos)
    client.publish("carStatus", carStat)

client = mqtt.Client("Positions")
client.on_message = on_message
client.on_connect = on_connect

try:
    client.connect(broker_address)
except:
    print("Could not connect to broker, are you sure you ran docker-compose up?")
    exit(1)

client.loop_forever()
