import os

def save_script(project_name, code_str):
    project_dir = os.path.join(os.getcwd(), "generated_scripts", project_name.replace(" ", "_").lower())
    os.makedirs(project_dir, exist_ok=True)

    script_path = os.path.join(project_dir, f"{project_name.replace(' ', '_').lower()}_cad.py")
    with open(script_path, "w") as f:
        f.write(code_str)

    return script_path

def save_prompt_log(project_name, prompt, response):
    project_dir = os.path.join(os.getcwd(), "prompts", project_name.replace(" ", "_").lower())
    os.makedirs(project_dir, exist_ok=True)

    with open(os.path.join(project_dir, "prompt.txt"), "w") as f:
        f.write(prompt)

    with open(os.path.join(project_dir, "response.py"), "w") as f:
        f.write(response)

def execute_script(path):
    os.system(f"python \"{path}\"")