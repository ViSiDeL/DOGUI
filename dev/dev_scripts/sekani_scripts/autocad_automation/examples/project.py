from pyautocad import Autocad, APoint
import pythoncom
import os
from datetime import datetime

def initialize_autocad():
    pythoncom.CoInitialize()
    acad = Autocad(create_if_not_exists=True)
    acad.visible = True
    return acad

def create_new_project(acad, project_name="MyCADProject", directory="C:\\Users\\Public\\Documents\\AutoCAD_Projects"):
    # Ensure directory exists
    os.makedirs(directory, exist_ok=True)

    # Timestamped filename to prevent overwriting
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{project_name}_{timestamp}.dwg"
    filepath = os.path.join(directory, filename)

    # Add drawing if not already open
    if acad.doc is None:
        acad.app.Documents.Add()

    # Add some placeholder geometry
    acad.model.AddLine(APoint(0, 0), APoint(100, 100))
    acad.model.AddText("Project: " + project_name, APoint(10, 10), 5)

    # Save the drawing
    acad.doc.SaveAs(filepath)
    print(f"✅ Project saved as: {filepath}")
    return filepath

if __name__ == "__main__":
    acad = initialize_autocad()
    create_new_project(acad, project_name="PrototypeDesign")

