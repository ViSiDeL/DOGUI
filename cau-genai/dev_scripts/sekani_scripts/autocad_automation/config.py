import json

class ProjectConfig:
    def __init__(self, name="", width=0, height=0, unit="feet", type="floorplan"):
        self.name = name
        self.width = width
        self.height = height
        self.unit = unit
        self.type = type

    def __str__(self):
        return f"{self.name} ({self.width}x{self.height} {self.unit}) - {self.type}"

    def to_dict(self):
        return {
            "name": self.name,
            "width": self.width,
            "height": self.height,
            "unit": self.unit,
            "type": self.type
        }

    def to_json(self, filepath):
        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=4)

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
        return cls(**data)
