import math
from gpsproject import gpsproject as gps
lon1=float(input('Starting Longitude?'))
lat1=float(input('Starting Latitude?'))
dimension_x=int(input('Dimension of X axis?'))
dimension_y=int(input('Dimension of Y axis?'))
starting_x=int(input('Starting point: X axis'))
starting_y=int(input('Starting point: Y axis'))
points=[]
for i in range(0,dimension_x+1):
    x=gpsproject(starting_x,starting_y)
    points.append(x)
