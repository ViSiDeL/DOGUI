import os
# from draw import draw_line, draw_text
# from io import save_drawing
from config import ProjectConfig


def prompt_user_for_project_details():
    print("Let's create a new CAD project.")
    name = input("Project Name: ")
    project_type = input("Project Type (e.g., floorplan, part): ")
    width = float(input("Width: "))
    height = float(input("Height: "))
    unit = input("Units (feet, meters, etc.): ")

    return ProjectConfig(name, width, height, unit, project_type)

def ideation():
    print('Initializing Ideation - Stage 1\n')
    try:
        config = prompt_user_for_project_details()
        print('Project Created Successfully! Lets begin the ideation phase...')
        return(config)
    except Exception as e:
        raise ValueError("Invalid project details!") from e


# def generate_base_design(acad, project_name, width, height, unit="feet"):
#     """
#     Generates a base rectangular drawing based on user input.
#     """
#     print(f"🧠 Generating design for: {project_name} ({width} x {height} {unit})")

#     # Draw the base rectangle (floorplan or part outline)
#     draw_line(acad, (0, 0), (width, 0))             # Bottom
#     draw_line(acad, (width, 0), (width, height))    # Right
#     draw_line(acad, (width, height), (0, height))   # Top
#     draw_line(acad, (0, height), (0, 0))            # Left

#     draw_text(acad, f"{project_name}", (width / 4, height / 2), 10)

#     # Save file under user_projects/
#     folder = os.path.join(os.getcwd(), "user_projects")
#     os.makedirs(folder, exist_ok=True)

#     filename = f"{project_name.replace(' ', '_').lower()}.dwg"
#     full_path = os.path.join(folder, filename)

#     save_drawing(acad, full_path)
#     print(f"✅ Saved base design to {full_path}")

#     return full_path
if __name__ == "__main__":
    phase1 = ideation()
    print("\n>>>>>>>>Ideation Stage Complete<<<<<<<<\n")
    print(phase1.name)
