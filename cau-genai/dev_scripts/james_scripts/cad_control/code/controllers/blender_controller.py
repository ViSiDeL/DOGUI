"""
Blender specific CAD commands and prompts

"""

from cad_controller import CADController

class BlenderCADController(CADController):
    def draw(self, shape, dimensions):
        print(f"Using Blender API to draw {shape} with {dimensions}")