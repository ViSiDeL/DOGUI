"""

User Class - Controls user information for an active user session.

"""

class User:
    def __init__(self, user_id: int, username: str, role: str):
        self.user_id = user_id
        self.username = username
        self.role = role
        self.session_id = None

    # login routine
    def login(self, session):
        self.session_id = session

    # logout routine
    def logout(self):
        pass

    def save_project(self):
        pass

    def load_project(self):
        pass