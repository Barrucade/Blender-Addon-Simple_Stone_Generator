bl_info = {
    "name": "Ruzhang's Stone Generator",
    "author": "Ruzhang",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}

import bpy
from math import radians
from bpy.props import *


def main(context):
    for ob in context.scene.objects:
        print(ob)


class StoneGenerator(bpy.types.Operator):
    bl_idname = "object.stone_generator"
    bl_label = "Stone Generator"
    bl_options = {'REGISTER', 'UNDO'}
    
    #addon properties
    subdivision_scale : IntProperty(
        name = "Subdivision Scale",
        default = 3,
        min = 0,
        max = 5
        )
        
    
    
    noise_scale : FloatProperty(
        name = "Noise Scale",
        default = 0.8,
        min = 0.4,
        max = 2.0
        )
        
    flatness : FloatProperty(
        name = "Flat Scale",
        default = 0.6,
        min = 0.0,
        max = 1.0
        )
        
    global_trigger : BoolProperty(
        name = 'Change Shape by Location',
        default = False
        )
        
    flat_trigger : BoolProperty(
        name = 'Shade Flat',
        default = False
        )

    def execute(self, context):
        
        #create a basic cube
        bpy.ops.mesh.primitive_cube_add()
        rock = bpy.context.active_object
        
        #subdivision modifier
        mod_subsurf = rock.modifiers.new("My Modifier", 'SUBSURF')
        #subdivision value
        mod_subsurf.levels = self.subdivision_scale
        
        #smooth shade
        if self.flat_trigger == False:
            bpy.ops.object.shade_smooth()
        else:
            bpy.ops.object.shade_flat()
        
        #displace modifier
        mod_displace = rock.modifiers.new("My Displacement",'DISPLACE')
        
        if self.global_trigger == False:
            mod_displace.texture_coords = ('LOCAL')
        
        else:
            mod_displace.texture_coords = ('GLOBAL')
        
        #texture
        new_tex = bpy.data.textures.new("Distorted Texture", 'VORONOI')
       
        
        #texture noise
        new_tex.noise_scale = 2-self.noise_scale
        new_tex.distance_metric = ('DISTANCE_SQUARED')
        new_tex.contrast = 1-self.flatness
        
        
        #assign the texture to displacement modifier
        mod_displace.texture = new_tex
         
                
        return {'FINISHED'}





# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(StoneGenerator)
   


def unregister():
    bpy.utils.unregister_class(StoneGenerator)
    


if __name__ == "__main__":
    register()


    #bpy.ops.object.stone_generator()
