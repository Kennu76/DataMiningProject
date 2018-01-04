import json

sensor_path = '/Users/tonis.kasekamp/other/data/DataMiningProject/starship_sensors_data/dt=2017-07-03/ahrs.25.json'
sensor_data = open(sensor_path)

i = 1
bots = set()

for line in iter(sensor_data):
    # if i == 10:
    #     break
    points = json.loads(line)
    # print points[0]
    bots.add(points['meta']['botid'])
    i = i + 1

sensor_data.close()

print(bots)
