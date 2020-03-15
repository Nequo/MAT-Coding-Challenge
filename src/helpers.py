import json
import geopy

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

def car_position(carIndex, car_sectors, car_laps):
    """ 
    Get the car's position in a race
    
    Parameters: 
    carIndex (int): The number of the car
    car_sectors ([int]): latest car sector per car sorted by carIndex
    car_laps ([int]): latest car laps per car sorted by carIndex

    Returns: 
    int: position of the car in the race
    """
    car_sector_and_lap = [0] * 6
    # calculate all cars' total positions
    for i in range(len(car_sectors)):
        car_sector_and_lap[i] = car_laps[i] * 1000 + car_sectors[i] 
    # Sort the cars so that car at index 0 is the first car in the race
    sorted_cars = [i[0] for i in sorted(enumerate(car_sector_and_lap), key=lambda x:x[1])]
    sorted_cars.reverse()
    return sorted_cars.index(carIndex)

def car_speed(time_loc, prev_time_loc):
    """ 
    Get the car's speed between 2 points in time
    
    Parameters: 
    time_loc (int, int, int): a timestamp in ms epoch, a latitude and a longitude
    prev_time_loc (int, int, int): 

    Returns: 
    int: speed of the car in miles per hour
    """
    timestamp, lat, longitude = time_loc
    prev_timestamp, prev_lat, prev_longitude = prev_time_loc

    dist = geopy.distance.distance((lat, longitude), (prev_lat, prev_longitude)).miles
    # Time difference in milliseconds
    time_diff = timestamp - prev_timestamp
    speed = (dist/time_diff) * 3600000

    return speed
