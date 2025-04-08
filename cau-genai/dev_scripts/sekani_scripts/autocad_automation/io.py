# autocad_automation/io.py
import os
from datetime import datetime

def generate_project_path(project_name, base_dir="C:\\Users\\Public\\Documents\\AutoCAD_Projects"):
    os.makedirs(base_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{project_name}_{timestamp}.dwg"
    return os.path.join(base_dir, filename)

def open_drawing(acad, filepath):
    """
    Open an existing .dwg file in AutoCAD.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"❌ File not found: {filepath}")
    
    doc = acad.app.Documents.Open(filepath)
    acad.doc = doc
    print(f"✅ Opened drawing: {filepath}")
    return doc


def save_drawing(acad, filepath):
    if acad.doc is not None:
        acad.doc.SaveAs(filepath)
        print(f"✅ Drawing saved as: {filepath}")
    else:
        raise Exception("❌ No document to save.")


