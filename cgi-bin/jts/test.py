import re, commands

s, o = commands.getstatusoutput("./run")
o = o.split("\n")[0].strip()

ReAllPoints = re.compile("[\(,][^\(,\)]*[\),]")

for point in ReAllPoints.findall(o):
    lon, lat = point[1:-1].split(" ")
    lat = float(lat)
    lon = float(lon)
    print lat, lon
    