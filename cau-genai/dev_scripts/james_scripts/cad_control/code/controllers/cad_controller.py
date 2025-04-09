"""
Generic class makes suggestions to the user and controls the CAD software.

"""

class CADController:
    def draw(self, shape, dimensions):
        raise NotImplementedError("Subclasses must implement this method")

    def move(self, object_id, new_position):
        raise NotImplementedError("Subclasses must implement this method")