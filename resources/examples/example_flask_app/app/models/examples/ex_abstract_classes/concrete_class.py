from .abstract_class import AbstractExample

class ConcreteExample(AbstractExample):
    """
    This class extends AbstractExample and provides an implementation of the abstract 'action' method.
    """

    def action(self):
        """Implement the required abstract method."""
        return f"{self.name} is performing a specific action from ConcreteExample."
