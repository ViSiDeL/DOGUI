# autocad_automation/draw.py
from pyautocad import APoint

def draw_line(acad, start=(0, 0), end=(100, 100)):
    acad.model.AddLine(APoint(*start), APoint(*end))

def draw_circle(acad, center=(50, 50), radius=25):
    acad.model.AddCircle(APoint(*center), radius)

def draw_text(acad, text, position=(10, 10), height=5):
    acad.model.AddText(text, APoint(*position), height)
