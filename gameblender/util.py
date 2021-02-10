import bpy
from mathutils import *
from math import *
import bmesh

class CustomReg:
  def __init__(self, reg, unreg):
    self.reg = reg
    self.unreg = unreg

