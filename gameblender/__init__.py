import bpy, imp

from . import config, util, ui, sector, ops, load, props, gen

imp.reload(config)
imp.reload(util)
imp.reload(props)
imp.reload(ops)
imp.reload(ui)
imp.reload(load)
imp.reload(sector)
imp.reload(gen)

bpy_exports = props.bpy_exports + ops.bpy_exports + ui.bpy_exports

reg = False

def register():
  global reg
  
  if reg:
    return
  
  reg = True
  for cls in bpy_exports:
    if type(cls) == util.CustomReg:
      cls.reg()
    else:
      bpy.utils.register_class(cls)
      
def unregister():
  global reg
  if not reg:
    return
    
  reg = False
  for cls in bpy_exports:
    if type(cls) == util.CustomReg:
      cls.unreg()
    else:
      bpy.utils.unregister_class(cls)
      

