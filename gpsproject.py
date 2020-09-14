import math
#lon1=4.642005
#lat1=43.735832
class gpsproject:
    def __init__(self,lon1,lat1):
        self.bearing=None
        self.distance=None
        self.lon_init=math.radians(lon1)
        self.lat_init=math.radians(lat1)
        self.lon_project=None
        self.lat_project=None
        R = 6378.1 #Radius of the Earth in kms
    def project(self,distance,bearing):
        R = 6378.1
        self.distance=distance
        self.bearing=math.radians(bearing)

        self.lat_project = math.asin( math.sin(self.lat_init)*math.cos(self.distance/R) +
     math.cos(self.lat_init)*math.sin(self.distance/R)*math.cos(self.bearing))


        self.lon_project=self.lon_init + math.atan2(math.sin(self.bearing)*math.sin(self.distance/R)*math.cos(self.lat_init),
             math.cos(self.distance/R)-math.sin(self.lat_init)*math.sin(self.lat_project))

        self.lat_project = math.degrees(self.lat_project)
        self.lon_project = math.degrees(self.lon_project)
        return self.lon_project,self.lat_project
