import bpy
from mathutils import *
from math import *
import bmesh

from . import config
from . import util
from .sector import Sector

def height(lat, lon):
  return 0.0

def getMesh(name):
  if name in bpy.data.meshes:
    return bpy.data.meshes[name]
  
  mesh = bpy.data.meshes.new(name)
  return mesh 
  
def getObject(name, type):
  data = None
  if type == "MESH":
    data = getMesh(name)
  
  if name in bpy.data.objects:
    ob = bpy.data.objects[name]
    return ob 
  else:
    ob = bpy.data.objects.new(name, data)
  
  
  return ob 
def genSector(u, v, bm=None, steps=25):
  sector = Sector()
  
  sector.latLon = util.uvToLatLon(u, v)
  sector.update()
  
  sname = sector.genName()
  ob = None
  
  if bm is None:
    col = sector.getCollection()
    ob = getObject("floor" + sector.genSuffix(), "MESH")
    bm = bmesh.new()
    scene = bpy.context.scene
    
    if ob.name not in col.objects:
      col.objects.link(ob)
      
    if ob.name not in scene.objects:
      scene.collection.objects.link(ob)
  
  
  print(sector.latLon)
  
  di = config.dSectorLon / (steps-1)
  dj = config.dSectorLat / (steps-1)
  
  grid = [[None for x in range(steps)] for y in range(steps)]
  
  for i in range(steps):
    for j in range(steps):
      lon = sector.latLon[1] + i*di
      lat = sector.latLon[0] + j*dj
      h = height(lat, lon)
      
      co = util.sphereToWorld(lat, lon)
      vec = Vector(co)
      vec.normalize()
      
      co += vec*h
      
      v = bm.verts.new(co)
      
      grid[i][j] = v
  
  for i in range(steps-1):
    for j in range(steps-1):
      v1 = grid[i][j]
      v2 = grid[i][j+1]
      v3 = grid[i+1][j+1]
      v4 = grid[i+1][j]
      vs = [v1, v2, v3, v4]
      f = bm.faces.new(vs)
  
  if ob:
    bm.to_mesh(ob.data)
    ob.data.update()
    
  return sector
  