import os, sys
from datetime import datetime

if sys.platform == 'win32':
    try:
        import pythoncom
        from pyautocad import Autocad, APoint
    except ImportError as e:
        print(f"warning: required windows-only modules not found: {e}")

def initialize_autocad():
    if sys.platform == 'win32':
        try:
            # Initialize COM
            pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)

            # Initialize AutoCAD COM object
            acad = Autocad(create_if_not_exists=True)

            # Make sure AutoCAD is visible
            acad.visible = True

            # Create a new document (This avoids using ActiveDocument directly)
            acad.Application.Documents.Add()  # Add a new drawing
            acad.model = acad.ActiveDocument.ModelSpace  # Access the model space of the active document

            # Return the AutoCAD instance
            return acad
        except Exception as e:
            print(f"❌ Error initializing AutoCAD: {str(e)}")
    else:
        print("running on a non-windows platform. windows-specific functionality not available.")

def draw(acad):
    pass

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
    directory = os.path.join(os.path.dirname(__file__), 'assets')
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{project_name}_{timestamp}.dwg"
    filepath = os.path.join(directory, filename)
    acad.doc.SaveAs(filepath)
    print(f"✅ Saved: {filepath}")

def save_script_to_file(script_code: str, project_name="dogui_script"):
    directory = os.path.join(os.path.dirname(__file__), 'scripts')
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{project_name}_{timestamp}.py"
    filepath = os.path.join(directory, filename)
    with open(filepath, "w") as file:
        file.write(script_code)

    print(f"✅ DOGUI.AI-generated script saved to: {filepath}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        try:
            acad = initialize_autocad()
            draw_square(acad)
        except Exception as e:
            print(f"warning: running on a non-windows platform. windows-specific functionality not available: {e}")
