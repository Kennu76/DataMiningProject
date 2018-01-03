import json
import csv

sensor_path = '/Users/tonis.kasekamp/other/data/DataMiningProject/starship/example_sensor_data.json'
sensor_data = open(sensor_path)

# sensor_path
location_path = '/Users/tonis.kasekamp/other/data/starship_localisation_data/tallinn_location_july.csv'

loc_data = open(location_path)

loc_data_filter = []

new_csv_header = ['timestamp', 'botid','coordinates_long','coordinates_lat','accel_vec_x','accel_vec_y','accel_vec_z','orientation_delta_x','orientation_delta_y','orientation_delta_z']

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


# for line in iter(loc_data):
#     # if i == 10:
#     #     break
#     points = line.split(",")
#     if
#     if points[0] == '6D80':
#         loc_data_filter.append(line)

# print(len(loc_data_filter))
#
# for line in iter(sensor_data):
#     # print(line)
#     json_line = json.loads(line)
#     # print(json_line)
#     if json_line["data"]['standstill_detected'] == False:
#         print("stand")


def create_line(json_line, lat_long):
    timestamp = json_line["meta"]["secs"]
    botid = json_line["meta"]["botid"]
    orientation_delta_x = json_line["data"]["orientation_delta"]["x"]
    orientation_delta_y = json_line["data"]["orientation_delta"]["y"]
    orientation_delta_z = json_line["data"]["orientation_delta"]["z"]
    accel_vec_x = json_line["data"]["accel_vec"]["x"]
    accel_vec_y = json_line["data"]["accel_vec"]["y"]
    accel_vec_z = json_line["data"]["accel_vec"]["z"]
    return [timestamp, botid, lat_long[0], lat_long[1], accel_vec_x, accel_vec_y, accel_vec_z, orientation_delta_x, orientation_delta_y, orientation_delta_z]


used_timestamps = set()

def get_something(timestamp, botid, loc_data):
    for line in iter(loc_data):
        points = line.split(",")
        if botid == points[0] and timestamp == get_timestamp(points[1]):
            used_timestamps.add(timestamp)
            # coordinates_long,coordinates_lat
            return [points[2], points[3]]
        else:
            return []
    return []

def get_timestamp(point_ts):
    return point_ts.split(".")[0]

def make_data():
    accumulator = []
    accumulator.append(new_csv_header)
    for line in iter(sensor_data):
        json_line = json.loads(line)
        timestamp = json_line["meta"]["secs"]
        if json_line["data"]['standstill_detected'] == True:
            # ignore stanststill
            continue
        if timestamp in used_timestamps:
            # ignore used seconds
            continue
        botid = json_line["meta"]["botid"]
        lat_long = get_something(timestamp, botid, loc_data)
        if len(lat_long) == 0:
            continue
        new_line = create_line(json_line, lat_long)
        accumulator.append(new_line)
    # process accumulator
    print(accumulator)
    csvfile = './starship/output.csv'
    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(accumulator)

make_data()