import bpy
from mathutils import *
from math import *
import bmesh, os, sys, os.path
import subprocess

from . import config
from . import util

class Sector:
  def __init__(self):
    self.blendpath = ""
    self.latLon = [0, 0] #lattitude and longitude?
    self.origin = Vector()
    
    self.editing = False
    
    self.matrix = Matrix()
    self.matrix.to_4x4()
    self.imatrix = Matrix()
    self.imatrix.to_4x4()
    
    self.matrixInst = Matrix()
    self.imatrixInst = Matrix()
    
    self.matrixInst.to_4x4()
    self.imatrixInst.to_4x4()
  
  def fromCollection(self, col):
    name = col.name[1:]
    name = name.split("_")
    
    u = int(util.fromRadix(name[0])+0.00001)
    v = int(util.fromRadix(name[1])+0.00001)
    
    self.latLon = util.uvToLatLon(u, v)
    self.update()
    
    print(u, v, self.latLon)
    
  def getCollection(self):
    self.update()
    
    name = self.genName()
    if name not in bpy.data.collections:
      col = bpy.data.collections.new(name)
      col.id_data.use_fake_user = True
    
    col = bpy.data.collections[name]
    off = self.origin
    col.instance_offset[0] = off[0]
    col.instance_offset[1] = off[1]
    col.instance_offset[2] = off[2]
   
    col.gamesector.isSector = True
    
    return col
  
  def _hideInstance(self, state):
    ctx = bpy.context
    scene = ctx.scene
    col = self.getCollection()
    
    for ob in scene.objects:
      if not ob.data and ob.instance_collection == col:
        ob.hide_set(state)
  
  def _getParentEmpty(self):
    name = "_par_" + self.genName()
    ob = None
    
    if not name in bpy.data.objects:
      ob = bpy.data.objects.new(name, None)
    else:
      ob = bpy.data.objects[name]
    
    ob.rotation_mode = 'QUATERNION'
    
    scene = bpy.context.scene
    if ob.name not in scene.objects:
      scene.collection.objects.link(ob)
    return ob
    
  def startEdit(self, uoff=0, voff=0):
    self.editing = True
    self.update()
    self._hideInstance(True)
    
    col = self.getCollection()
    par = self._getParentEmpty()
    
    mat = self.imatrix
    loc, quat, scale = mat.decompose()
    
    par.location = Vector()
    par.rotation_quaternion = Vector([0, 0, 0, 1])
    
    for ob in col.objects:
      print(ob)
      if ob.parent is None:
        ob.parent = par
    
    par.location = loc
    par.rotation_quaternion = quat
    
  def endEdit(self):
    self._hideInstance(False)
    self.editing = False
    
    col = self.getCollection()
    par = self._getParentEmpty()
    
    for ob in col.objects:
      print(ob)
      if ob.parent == par:
        ob.parent = None
      
  def update(self):
    self.origin = util.sphereToWorld(self.latLon[0], self.latLon[1])
    mat = Matrix.Translation(self.origin)
    
    lat, lon = self.latLon
    lat = pi*lat/180.0;
    lon = pi*lon/180.0
    
    r1 = Matrix.Rotation(lat, 4, "Y")
    r2 = Matrix.Rotation(-lon, 4, "Z")
    r3 = Matrix.Rotation(pi*0.5, 4, "Y")
    
    rmat = Matrix()
    rmat.to_4x4()
    
    rmat = r2 @ r1 @ r3
    
    self.matrix = mat @ rmat 
    
    self.imatrix = Matrix(self.matrix)
    self.imatrix.invert()
  
  def saveExternal(self):
    editing = self.editing
    
    #make absolutely sure we aren't editing, i.e. are parented to editing empty
    self.endEdit()
    
    self.enforceSuffix()
    path = os.path.join(config.basepath, self.genBlendPath())
    path = os.path.abspath(path)
      
    bpy.ops.wm.save_as_mainfile(filepath=path, copy=True, check_existing=False)

    ret = subprocess.run([bpy.app.binary_path, path, "--python-text", "pruneSectors.py"])
    print(ret.stdout)
    print(ret.stderr)
    print("return code:", ret.returncode)
    
    if editing:
      self.startEdit()
  
  def delete(self):
    colmap = util.makeColMap()
    
    scene = bpy.context.scene
    col = self.getCollection()
    col.use_fake_user = False
    for ob in list(scene.objects):
      if col not in colmap[ob.name]:
        continue
        
        for col2 in colmap[ob.name]:
          if col2 == col:
            continue;
          
          col2.objects.unlink(ob)
  
  def loadExternal(self):
    pass
  
  def enforceSuffix(self):
    col = self.getCollection()
    suffix = self.genSuffix()
    
    for ob in col.objects:
      if suffix not in ob.name:
        ob.name += suffix
    
  def getUV(self):
    return util.latLonToUV(self.latLon[0], self.latLon[1], True)
  
  def genSuffix(self):
    return "_" + self.genName()
    
  def genBlendPath(self):
    self.blendpath = self.genName() + ".blend"
    return self.blendpath
    
  def genName(self):
    u, v = self.getUV()
    return "s" + util.toRadix(u) + "_" + util.toRadix(v)
    
