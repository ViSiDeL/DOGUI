import unittest
from app.models.examples.ex_classes.example_class import ExampleClass

class TestExampleClass(unittest.TestCase):

    # Test case 1: Ensure that the ExampleClass initializes correctly
    def test_initialization(self):
        example = ExampleClass("Test Name")
        self.assertEqual(example.get_name(), "Test Name", "The name should be 'Test Name'.")

    # Test case 2: Ensure that get_name returns the correct value
    def test_get_name(self):
        example = ExampleClass("Another Name")
        self.assertEqual(example.get_name(), "Another Name", "get_name should return 'Another Name'.")

    # Test case 3: Check if name is not None when initialized
    def test_name_is_not_none(self):
        example = ExampleClass("Valid Name")
        self.assertIsNotNone(example.get_name(), "Name should not be None.")

    # Test case 4: Check if ExampleClass can handle an empty string as a name
    def test_empty_name(self):
        example = ExampleClass("")
        self.assertEqual(example.get_name(), "", "The name should be an empty string.")
    
    # Test case 5: Ensure that the name is a string
    def test_name_type(self):
        example = ExampleClass("Test Name")
        self.assertIsInstance(example.get_name(), str, "The name should be a string.")

if __name__ == '__main__':
    unittest.main()
