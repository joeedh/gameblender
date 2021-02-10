import bpy
from mathutils import *
from math import *
import bmesh
from bpy.props import *

from . import util

class SectorGroup (bpy.types.PropertyGroup):
  transformed : bpy.props.BoolProperty()
  transformMatrix : FloatVectorProperty(size=16, subtype="MATRIX")
  isSector : bpy.props.BoolProperty()
  
  def setMatrix(self, m):
    m2 = self.matrix
    
    for i in range(4):
      for j in range(4):
        m2[i][j] = m[i][j]
  
  def getMatrix(self):
    m = Matrix()
    m2 = self.matrix
    
    for i in range(4):
      for j in range(4):
        m[i][j] = m2[i][j]
    return m
    
def reg():
  bpy.types.Collection.gamesector = bpy.props.PointerProperty(type=SectorGroup)

def unreg():
  pass
  
bpy_exports = [SectorGroup, util.CustomReg(reg, unreg)]

