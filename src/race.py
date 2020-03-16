from scipy import spatial
import geopy.distance
import csv
import json
import time
import helpers


class Race(object):
    def __init__(self, cars):
        self.cars = cars
        self.drivers = ["Lando Norris", "Carlos Sainz", "Max Verstappen", "Daniel Ricciardo", "Charles Leclerc", "Esteban Ocon"]
        self.track_points = list(csv.reader(open("./track.csv"), quoting=csv.QUOTE_NONNUMERIC))
        self.track_tree = spatial.KDTree(self.track_points)
        self.car_laps = [0] * cars # Total laps done per car
        self.lap_counted = [0] * cars # This is needed because sometimes cars can have sector 0 as the closest for 2 consecutive measurements
        self.car_sectors = [0] * cars # Which sector a car is on
        self.start_time = int(round(time.time() * 1000))
        self.car_locations = [(self.start_time,52.07400735591073,-1.020686454699684)] * cars # Initialise locations at sector 1
        self.lap_starts = [0] * cars # Timestamp for the start of a car's lap
        self.fastest_lap = 100000000000000
        self.car_updates = 0
        self.positions = [0] * cars
        self.stable_positions = []

    def increment_updates(self):
        self.car_updates += 1


    def update_car_sector(self, carIndex, lat, longitude):
        self.car_sectors[carIndex] = helpers.closest_sector(self.track_tree, lat, longitude)
        if self.car_sectors[carIndex] in [2, 3, 4]:
            self.lap_counted[carIndex] = 0


    def update_laps(self, carIndex, timestamp):
        events = []
        if self.car_sectors[carIndex] in [0,1] and self.lap_counted[carIndex] == 0:
            msg = "{} in car {} just completed lap {}".format(self.drivers[carIndex],
                                                              carIndex,self.car_laps[carIndex])
            event = helpers.gen_event(timestamp, msg)
            events.append(event)
            self.lap_counted[carIndex] = 1
            self.car_laps[carIndex] += 1
            lap_time = timestamp - self.lap_starts[carIndex]
            self.lap_starts[carIndex] = timestamp
            if lap_time < self.fastest_lap:
                self.fastest_lap = lap_time
                minutes, seconds, milliseconds = helpers.ms_to_time(self.fastest_lap)
                msg = "{} in car {} sets the fastest lap in {}:{}.{}".format(self.drivers[carIndex],
                                                                            carIndex,
                                                                            minutes,seconds,milliseconds)
                event = helpers.gen_event(timestamp, msg)
                events.append(event)
            print(events)
        return events
    

    def update_positions(self, timestamp):
        pos_updates = []
        if self.car_updates % self.cars == 0:
            pos = helpers.car_positions(self.car_sectors, self.car_laps)
            self.positions = pos
            if self.stable_positions == []:
                self.stable_positions = self.positions
            for i in range(self.cars):
                carPos = helpers.gen_carStatus(timestamp, i , "POSITION", self.stable_positions.index(i) + 1)
                pos_updates.append(carPos)

        return pos_updates


    def update_speed(self, carIndex, timestamp, lat, longitude):
        new_location = (timestamp, lat, longitude)
        speed = helpers.car_speed(new_location, self.car_locations[carIndex])
        self.car_locations[carIndex] = new_location
        carSpeed = helpers.gen_carStatus(timestamp, carIndex , "SPEED", speed)
        return carSpeed


    def check_overtakes(self, timestamp):
        overtakes = []
        if self.car_updates % self.cars == 0:
            if self.stable_positions == []:
                self.stable_positions = self.positions
            # check for overtakes between first and second place
            else:
                for i in range(self.cars):
                    if self.positions[i] != self.stable_positions[i]:
                        car = self.positions[i]
                        old_car = self.stable_positions[i]
                        if self.car_sectors[car] - self.car_sectors[old_car] > 3:
                            print(self.stable_positions)
                            msg = "{} in car {} does an amazing overtake on {} in car {} to take position {}".format(
                                self.drivers[car], car, self.drivers[old_car], old_car, i+1
                            )
                            overtake = helpers.gen_event(timestamp, msg)
                            overtakes.append(overtake)
                            self.stable_positions = self.positions
        return overtakes

