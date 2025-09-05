import os
from ai_interface import call_ai_model
from file_io import save_script, execute_script, save_prompt_log

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

def run_ideation(project_name):
    print(f"\n\U0001F9E0 IDEATION PHASE – Project: {project_name}\n")

    object_description = input("Describe what you want to design (e.g., 'Draw a stud wall'): ")

    full_prompt = f"""
    You are an AI CAD assistant. Based on the user's design request, generate a Python script using the pyautocad library.
    The user wants to design: {object_description}

    Ask for specs such as dimensions or materials as needed. Then, return a complete PyAutoCAD script that can be saved and executed.
    Use AutoCAD’s model space, and avoid UI interactions.
    """

    print("\nSending to AI model...\n")
    ai_script = call_ai_model(full_prompt)

    # Save AI prompt & response
    save_prompt_log(project_name, full_prompt, ai_script)

    # Save script to file
    script_path = save_script(project_name, ai_script)
    print(f"\n✅ Script saved at: {script_path}")

    # Execute it
    execute_script(script_path)
    print("✅ AutoCAD execution complete.\n")


if __name__ == "__main__":
    project_name = input("Enter your project name: ")
    run_ideation(project_name)
