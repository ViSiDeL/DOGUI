'''
Initialize AutoCAD and handle general connections
'''
# autocad_automation/core.py
from pyautocad import Autocad
import pythoncom

def get_acad_instance():
    pythoncom.CoInitialize()
    acad = Autocad(create_if_not_exists=True)
    acad.visible = True
    return acad

def ensure_document(acad):
    if acad.doc is None:
        acad.app.Documents.Add()
    return acad.doc
