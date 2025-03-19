import json
from os.path import join, dirname

with open(join(dirname(__file__), './.', 'james.json'), "r") as file:
    data = json.load(file)

print(data)
print(type(data))  # Confirm it's a dictionary
