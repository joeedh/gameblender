import bpy, os.path, os

basepath = os.path.split(bpy.data.filepath)[0]
basepath = os.path.join(basepath, "data")

if not os.path.exists(basepath):
  os.mkdir(basepath)
  


