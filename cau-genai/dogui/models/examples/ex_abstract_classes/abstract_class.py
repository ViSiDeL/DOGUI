from abc import ABC, abstractmethod

class AbstractExample(ABC):
    """
    This is an abstract class.
    It defines a template for all subclasses, enforcing the implementation of the 'action' method.
    """

    def __init__(self, name):
        """Initialize with a name."""
        self.name = name

    @abstractmethod
    def action(self):
        """
        Abstract method that must be implemented by subclasses.
        """
        pass  # No implementation here, forces subclasses to define this method

    def describe(self):
        """A non-abstract method that subclasses inherit by default."""
        return f"This is an instance of an abstract class named {self.name}."
