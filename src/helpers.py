import json

def gen_carCoordinates(message):
    json_msg = json.loads(message)
    carIndex = json_msg["carIndex"]
    location = json_msg["location"]
    lat = location["lat"]
    longitude = location["long"]
    timestamp = json_msg["timestamp"]
    return (carIndex, lat, longitude, timestamp)


def gen_carStatus(timestamp, carIndex, statType, statValue):
    """ 
    Generate the car status data to send to the broker's carStatus topic. 
  
    Parameters: 
    timestamp (int): the timestamp in epoch time
    carIndex (int)
    statType (string): SPEED | POSITION
    statValue (int): speed in mph, position between 1 and number of cars
  
    Returns: 
    json: Data to send to broker
    """
    if statType not in ["SPEED", "POSITION"]:
        raise ValueError("statType must be: SPEED or POSITION")
    stat = {
        "timestamp": timestamp,
        "carIndex": carIndex,
        "type": statType,
        "value": statValue
    }
    return json.dumps(stat)
        

def gen_event(timestamp, text):
    """ 
    Generate the car status data to send to the broker's events topic. 
  
    Parameters: 
    timestamp (int): the timestamp in epoch time
    text (string): the event's description

    Returns: 
    json: Data to send to broker
    """
    event = {
        "timestamp": timestamp,
        "text": text
    }
    return json.dumps(event)


def closest_sector(track_kdtree, lat, longitude):
    """ 
    Given an ordered list of track coordinates, get the index of the
    closest point on track

    Parameters: 
    track (scipy.spatial.KDTree): list of track coordinates

    Returns: 
    int: closest track sector
    """
    dist, sector = track_kdtree.query([lat,longitude])

    return sector

def car_position(carIndex, car_sector, car_laps):
    car_sector_and_lap = [0] * 6
    # calculate all cars' positions
    for i in range(len(car_sector)):
        car_sector_and_lap[i] = car_laps[i] * 1000 + car_sector[i] 
    print(car_sector_and_lap)
    # Sort the cars so that car at index 0 is the first car in the race
    sorted_cars = [i[0] for i in sorted(enumerate(car_sector_and_lap), key=lambda x:x[1])]
    sorted_cars.reverse()
    return sorted_cars.index(carIndex)

