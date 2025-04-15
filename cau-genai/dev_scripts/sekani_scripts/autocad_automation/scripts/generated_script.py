from pyautocad import Autocad, APoint
import pythoncom
import os
from datetime import datetime

def initialize_autocad():
    pythoncom.CoInitialize()
    acad = Autocad(create_if_not_exists=True)
    acad.visible = True
    return acad

def draw_square(acad, side_length=100):
    p1 = APoint(0, 0)
    p2 = APoint(side_length, 0)
    p3 = APoint(side_length, side_length)
    p4 = APoint(0, side_length)

    acad.model.AddLine(p1, p2)
    acad.model.AddLine(p2, p3)
    acad.model.AddLine(p3, p4)
    acad.model.AddLine(p4, p1)

    acad.model.AddText("2D Square", APoint(side_length/4, side_length/2), 5)

def save_drawing(acad, project_name="2D_Square"):
    directory = "C:\\Users\\sekani_b\\Desktop\\GitHub\\Projects\\IBM GEN AI\\CAU-GenAI\\cau-genai\\dev_scripts\\sekani_scripts\\autocad_automation\\assets"
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{project_name}_{timestamp}.dwg"
    filepath = os.path.join(directory, filename)
    acad.doc.SaveAs(filepath)
    print(f"✅ Saved: {filepath}")

if __name__ == "__main__":
    acad = initialize_autocad()
    draw_square(acad)
    save_drawing(acad)
