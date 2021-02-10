import bpy
from mathutils import *
from math import *
import bmesh

from . import config

s = "0123456789"
for i in range(ord('a'), ord('z')+1):
  s += chr(i)
for i in range(ord('A'), ord('Z')+1):
  s += chr(i)
radixstr = s 
radixmap = [0 for x in range(255)]
for i in range(len(s)):
  radixmap[ord(s[i])] = i 
  
def toRadix(i):
  base = len(radixstr)
  s2 = ''
  
  while i > 0:
    i2 = floor(i / base)
    d = (i - (i2*base))
    s2 = radixstr[d] + s2
    i = i2
    
  return s2;

def makeColMap():
  colmap = {}
  
  for col in bpy.data.collections:
    for ob in col.all_objects:
      if ob.name not in colmap:
        colmap[ob.name] = set()
      colmap[ob.name].add(col)
      
  return colmap
  
def fromRadix(s1):
  n = 0
  i = len(s1)-1
  base = len(radixstr)
  
  for c in s1:
    d = radixmap[ord(c)]
    n += pow(base, i)*d
    i -= 1
  return n
  
class CustomReg:
  def __init__(self, reg, unreg):
    self.reg = reg
    self.unreg = unreg

def uvToLatLon(u, v):
  size = config.sectorSize

  lat, lon = u, v
  lat = (lat * size) / (config.worldRadius * pi) - 0.5;
  lon = (lon * size) / (config.worldRadius * 2.0 * pi) - 1.0;
  
  return [lat*180.0, lon*180.0];
  
def latLonToUV(lat, lon, doFloor=True):
    size = config.sectorSize

    u, v = lat, lon
    
    u = (u / 180.0 + 0.5) * config.worldRadius * pi
    v = (v / 180.0 + 1.0) * 2.0*config.worldRadius * pi
    
    u = (u / size)
    v = (v / size)
    
    if doFloor:
      u = int(floor(u+0.000001))
      v = int(floor(v+0.000001))
      
    return [u, v]  
    
def sphereToWorld(lat, lon):
  lat = pi*lat/180.0
  lon = pi*lon/180.0
  
  r = config.worldRadius
  
  lat -= pi*0.5
  x2 = sin(lat)*r
  z2 = cos(lat)*r 
  
  x = cos(lon)*x2
  y = -sin(lon)*x2
  
  co = Vector()
  co[0] = x
  co[1] = y
  co[2] = z2

  return co
  
def worldToSphere(co):
  co = Vector(co)

  lon = atan2(co[1], co[0])
  sign = -1 if lon < 0 else 1
  lon = pi*sign - lon
  
  co.normalize()
  lat = acos(co[2]*0.99999) / pi
  lat = -(lat-0.5)
  
  lat *= 180.0
  lon = (lon / pi) * 180.0
  
  return [lat, lon]
  