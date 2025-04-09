class ExampleClass:
    """
    This is a base example class.
    It represents a generic entity with a name and an action method.
    """
    
    def __init__(self, name):
        """Initialize the ExampleClass with a name."""
        self.name = name
    
    def describe(self):
        """Return a description of the class instance."""
        return f"This is an instance of ExampleClass named {self.name}."

    def action(self):
        """Perform a generic action."""
        return f"{self.name} is performing a generic action."

    def hello(self):
        return "Hello from ExampleClass!"
    
    def get_name(self):
        return self.name