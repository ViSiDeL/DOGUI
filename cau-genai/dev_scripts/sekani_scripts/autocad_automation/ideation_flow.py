import os
from ai_interface import call_ai_model
from file_io import save_script, execute_script

def run_ideation(project_name):
    print(f"\n🧠 IDEATION: Designing for project '{project_name}'")

    object_description = input("Describe what you want to design (e.g., 'Draw a stud wall'): ")

    # Optional: enrich this with project context from DB
    full_prompt = f"""
    I am designing a {object_description}.
    Please determine what dimensions, specs, or materials are required.
    Then return a PyAutoCAD-compatible Python script that draws the object in 2D or 3D.
    """

    print("\nSending to AI model...\n")
    ai_script = call_ai_model(full_prompt)

    script_path = save_script(project_name, ai_script)
    print(f"✅ Script saved at {script_path}")

    execute_script(script_path)
    print("✅ Script executed. CAD drawing should now be visible.")

if __name__ == "__main__":
    project_name = input("Enter your project name: ")
    run_ideation(project_name)
