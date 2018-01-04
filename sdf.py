import json

sensor_path = '/Users/tonis.kasekamp/other/data/DataMiningProject/starship_sensors_data/dt=2017-07-03/ahrs.25.json'
sensor_data = open(sensor_path)

i = 1
bots = set()

max = 0
min = 1599073763
for line in iter(sensor_data):
    points = json.loads(line)
    # print points[0]
    bots.add(points['meta']['botid'])
    # print(points["meta"]["secs"])
    item = points["meta"]["secs"]
    if max < item:
        max = item
    if min > item:
        min = item
    i = i + 1

sensor_data.close()

print(min)
print(max)

print(bots)
print(i)

# first timestamp 1499093878
# last timestamp 1499073763
# ahrs 25 contains 553283 items
# min 1499073283
# max 1499104501
