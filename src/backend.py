import paho.mqtt.client as mqtt
from race import Race
import helpers

# set this to 127.0.0.1 if running independantly from the docker-compose up, set to broker if not
broker_address = "broker"
race = Race(6)

def on_connect(client, userdata, flags, rc):
    client.subscribe("carCoordinates")


def on_message(client, userdata, message):
    recv_string = str(message.payload.decode("utf-8"))
    carIndex, lat, longitude, timestamp = helpers.gen_carCoordinates(recv_string)
    race.increment_updates()
    race.update_car_sector(carIndex, lat, longitude)

    lap_events = race.update_laps(carIndex, timestamp)
    for event in lap_events:
        client.publish("events", event)

    positions = race.update_positions(timestamp)
    for position in positions:
        client.publish("carStatus", position)
        
    speed = race.update_speed(carIndex, timestamp, lat, longitude)
    client.publish("carStatus", speed)

    overtakes = race.check_overtakes(timestamp)
    for overtake in overtakes:
        client.publish("events", overtake)


client = mqtt.Client("Positions")
client.on_message = on_message
client.on_connect = on_connect

try:
    client.connect(broker_address, 1883)
except:
    print("Could not connect to broker, are you sure you ran docker-compose up?")
    exit(1)

client.loop_forever()
