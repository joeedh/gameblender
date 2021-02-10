import bpy, os.path, os
from math import *

basepath = os.path.split(bpy.data.filepath)[0]
basepath = os.path.join(basepath, "data")

if not os.path.exists(basepath):
  os.mkdir(basepath)

#z axis goes through planet poles  
worldUnit = "meter"

#smaller then earth to hopefully improve precision in 32-bit floats
worldRadius = 700*1000*0.5
sectorSize = 100.0
sectorHeight = 1000.0

dSectorLat = 360*sectorSize / (worldRadius*pi*2.0)
dSectorLon = 360*sectorSize / (worldRadius*pi*2.0)


