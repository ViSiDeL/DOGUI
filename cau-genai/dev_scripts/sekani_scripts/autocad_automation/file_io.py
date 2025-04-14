import os

def save_script(project_name, code_str):
    directory = os.path.join(os.getcwd(), "generated_scripts")
    os.makedirs(directory, exist_ok=True)

    filename = f"{project_name.replace(' ', '_').lower()}.py"
    path = os.path.join(directory, filename)

    with open(path, "w") as f:
        f.write(code_str)

    return path

def execute_script(path):
    os.system(f"python {path}")
