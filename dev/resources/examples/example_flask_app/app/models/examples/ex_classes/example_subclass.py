from .example_class import ExampleClass

class ExampleSubClass(ExampleClass):
    """
    This is a subclass of ExampleClass.
    It inherits the properties and methods of ExampleClass but overrides the action method.
    """
    
    def __init__(self, name, special_ability):
        """Initialize ExampleSubClass with a name and a special ability."""
        super().__init__(name)  # Call the parent class constructor
        self.special_ability = special_ability
    
    def action(self):
        """Perform a specialized action, overriding the base class method."""
        return f"{self.name} is using their special ability: {self.special_ability}."
