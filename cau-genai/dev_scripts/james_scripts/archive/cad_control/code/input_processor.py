
"""
This class processes the user input.

"""

class InputProcessor:
    def __init__(self):
        self.command_keywords = ["draw", "move", "delete", "rotate"]

    def process_input(self, user_input):
        """
        Determines if input is a CAD command or should be sent to Watson AI.
        """
        cleaned_input = user_input.strip().lower()

        # check if the input is a CAD command
        if any(word in cleaned_input for word in self.command_keywords):
            return "CAD", cleaned_input
        else:
            return "AI", cleaned_input
