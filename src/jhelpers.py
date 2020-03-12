import json

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
