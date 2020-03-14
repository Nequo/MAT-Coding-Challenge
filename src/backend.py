import paho.mqtt.client as mqtt
import time
from scipy import spatial
import geopy.distance

import helpers
import csv
import json
import datetime

broker_address = "127.0.0.1"

# Get track points from csv file at the start
data = list(csv.reader(open("./lap.csv"), quoting=csv.QUOTE_NONNUMERIC))
# Generate the tree only once
track_tree = spatial.KDTree(data)



car_laps = [0] * 6
car_sectors = [0] * 6
car_locations = [(int(round(time.time() * 1000)),52.07400735591073,-1.020686454699684)] * 6


def on_connect(client, userdata, flags, rc):
    client.subscribe("carCoordinates")


def on_message(client, userdata, message):
    recv_string = str(message.payload.decode("utf-8"))
    carIndex, lat, longitude, timestamp = helpers.gen_carCoordinates(recv_string)
    car_sectors[carIndex] = helpers.closest_sector(track_tree, lat, longitude)
    # Add a lap every time a car passes sector 1
    if car_sectors[carIndex] == 1:
        car_laps[carIndex] += 1
    pos = helpers.car_position(carIndex, car_sectors, car_laps)
    carPos = helpers.gen_carStatus(timestamp, carIndex , "POSITION", pos)
    client.publish("carStatus", carPos)

    new_location = (timestamp, lat, longitude)
    speed = helpers.car_speed(new_location, car_locations[carIndex])
    car_locations[carIndex] = new_location
    carSpeed = helpers.gen_carStatus(timestamp, carIndex , "SPEED", speed)
    client.publish("carStatus", carSpeed)
    

client = mqtt.Client("Positions")
client.on_message = on_message
client.on_connect = on_connect

try:
    client.connect(broker_address)
except:
    print("Could not connect to broker, are you sure you ran docker-compose up?")
    exit(1)

client.loop_forever()
