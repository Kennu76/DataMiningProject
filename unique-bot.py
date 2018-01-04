
f = open('/Users/tonis.kasekamp/other/data/starship_localisation_data/tallinn_location_july.csv')

i = 1
bots = set()

for line in iter(f):
    # if i == 10:
    #     break
    points = line.split(",")
    # print points[0]
    bots.add(points[0])
    i = i + 1

f.close()

print bots

actual_bots = set(['6D7', '6D8', 'Simulator LauriE', '6D100', '6D101', '6D46', '6D47', '6D89', '6D42', '6D83', 'Simulator Andy', '6D87', '6D84', '6D85', '6D24', '6D69', '6D20', '6D22', '6D23', '6D61', '6D63', '6D64', '6D65', '6E6', '6E7', '6E4', '6E5', '6E2', 'botid', 'Simulator Lindsay', '6D90', '6D54', '6D11', '6D76', '6D37', '6D34', '6D19', '6D18', '6D31', '6D15', '6D14', '6D17', '6D16', '6D77', '6D10', '6D13'])

# dataset at 07-02 only contains bot 6D1
