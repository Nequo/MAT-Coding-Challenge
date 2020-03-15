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
data = list(csv.reader(open("./track.csv"), quoting=csv.QUOTE_NONNUMERIC))
# Generate the tree only once
track_tree = spatial.KDTree(data)

drivers = ["Lando Norris", "Carlos Sainz", "Max Verstappen", "Daniel Ricciardo", "Charles Leclerc", "Esteban Ocon"]
start_time = int(round(time.time() * 1000))
car_laps = [0] * 6
lap_counted = [0] * 6 # This is needed because sometimes cars can have sector 0 as the closest for 2 consecutive measurements
car_sectors = [0] * 6
car_locations = [(start_time,52.07400735591073,-1.020686454699684)] * 6
lap_starts = [start_time] * 6
fastest_lap = 100000000000000


def on_connect(client, userdata, flags, rc):
    client.subscribe("carCoordinates")


def on_message(client, userdata, message):
    recv_string = str(message.payload.decode("utf-8"))
    carIndex, lat, longitude, timestamp = helpers.gen_carCoordinates(recv_string)
    car_sectors[carIndex] = helpers.closest_sector(track_tree, lat, longitude)
    # Add a lap every time a car passes sectors 0 or 1
    # TODO: Need to check what sector value to use, maybe retake track measurements
    if car_sectors[carIndex] in [0, 1] and lap_counted[carIndex] == 0:
        msg = drivers[carIndex] + " in car " + str(carIndex) + " just completed lap " + str(car_laps[carIndex])
        event = helpers.gen_event(timestamp, msg)
        client.publish("events", event)
        lap_counted[carIndex] = 1
        car_laps[carIndex] += 1
        lap_time = timestamp - lap_starts[carIndex]
        lap_starts[carIndex] = timestamp

    # Now the car has passed sector 0 so lap won't be counted twice
    if car_sectors[carIndex] >= 2 and car_sectors[carIndex] <=10:
        lap_counted[carIndex] = 0

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
