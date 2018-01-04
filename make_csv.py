import json
import csv

# sensor_path = '/Users/tonis.kasekamp/other/data/DataMiningProject/starship/example_sensor_data.json'
# final = '/Users/tonis.kasekamp/other/data/DataMiningProject/starship_sensors_data/dt=2017-07-03/final'
other_path = '/Users/tonis.kasekamp/other/data/DataMiningProject/starship_sensors_data/dt=2017-07-03/ahrs.25.json'
sensor_data = open(other_path)

# sensor_path
location_path = '/Users/tonis.kasekamp/other/data/starship_localisation_data/tallinn_location_july.csv'
loc_sample = '/Users/tonis.kasekamp/other/data/DataMiningProject/starship/tallinn_sample_1000.csv'

# with open(location_path) as f:
#     for line in f:
#         loc_data.append(line)
# loc_data = open(loc_sample)

loc_data_filter = []

new_csv_header = ['timestamp', 'botid','coordinates_long','coordinates_lat','accel_vec_x','accel_vec_y','accel_vec_z','orientation_delta_x','orientation_delta_y','orientation_delta_z']

counter = 0
# algorithm
# for each line in sensor
# if timestamp not in used_timestamps
# that is not standstill
# check if there is the same timestamp in location by splitting loc to points
# if yes
#  add to used_timestamps
#  make an array that contains necessary data
#  add this to accumulator
# save result to file


def filter_localisation(f):
    suitable_bots = set([u'6E7', u'6E5', u'6D40'])

    array = []
    min = 1499073283
    max = 1499104501
    for line in iter(f):
        # if i == 10:
        #     break
        points = line.split(",")
        # print points[0]
        # bots.add(points[0])
        # print(points[1])
        if points[1] == 'timestamp':
            continue
        timestamp = int(float(points[1]))
        if timestamp <= max and timestamp >= min:
            if points[0] in suitable_bots:
                # i = i + 1
                array.append(points)
    f.close()
    return array


def create_line(json_line, lat_long):
    timestamp = json_line["meta"]["secs"]
    botid = json_line["meta"]["botid"]
    orientation_delta_x = json_line["data"]["orientation_delta"]["x"]
    orientation_delta_y = json_line["data"]["orientation_delta"]["y"]
    orientation_delta_z = json_line["data"]["orientation_delta"]["z"]
    accel_vec_x = json_line["data"]["accel_vec"]["x"]
    accel_vec_y = json_line["data"]["accel_vec"]["y"]
    accel_vec_z = json_line["data"]["accel_vec"]["z"]
    print("created line")
    return [timestamp, botid, lat_long[0], lat_long[1], accel_vec_x, accel_vec_y, accel_vec_z, orientation_delta_x, orientation_delta_y, orientation_delta_z]


used_timestamps = set()

def get_something(timestamp, botid, loc_data):
    global counter
    for points in iter(loc_data):
        # points = line.split(",")
        loc_time = int(float(points[1]))
        # counter += 1
        # print(timestamp, loc_time, timestamp == loc_time)
        # print(str(botid), points[0])
        if str(botid) == points[0] and timestamp == loc_time:
            used_timestamps.add(timestamp)
            # coordinates_long,coordinates_lat
            return [points[2], points[3]]
        # else:
        #     # print("not it")
        #     return []
    return []


def get_timestamp(point_ts):
    return point_ts.split(".")[0]


def make_data():
    global counter
    accumulator = []
    accumulator.append(new_csv_header)
    for line in iter(sensor_data):
        # print("iter")
        counter += 1
        json_line = json.loads(line)
        timestamp = json_line["meta"]["secs"]
        if json_line["data"]['standstill_detected'] == True:
            # ignore stanststill
            continue
        if timestamp in used_timestamps:
            # ignore used seconds
            print("ignore", timestamp)
            continue
        botid = json_line["meta"]["botid"]
        lat_long = get_something(timestamp, botid, loc_data)
        if len(lat_long) == 0:
            continue
        new_line = create_line(json_line, lat_long)
        print("created line", new_line)
        accumulator.append(new_line)
    # process accumulator
    # print(accumulator)
    csvfile = './starship/output.csv'
    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(accumulator)


loc_data = filter_localisation(open(location_path))
print("location data len ", len(loc_data))
print(loc_data[2])
make_data()
print(counter)
print(used_timestamps)
