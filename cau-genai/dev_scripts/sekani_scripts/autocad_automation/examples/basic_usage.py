from autocad_automation.core import AutoCADController
from autocad_automation.project import create_project

# Initialize AutoCAD
cad = AutoCADController()

# Create a new project
create_project("SiteLayout")

# Add basic shapes
cad.add_line((0, 0), (100, 100))
cad.add_circle((50, 50), 25)
cad.add_rectangle((10, 10), 40, 20)
cad.add_text("Sample Project", (5, 5))
