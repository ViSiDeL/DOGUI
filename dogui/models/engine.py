"""

Design Engine class - Core design engine responsible for controlling the workflow and managing data flow

"""

from models.user import User

class DesignEngine:
    def __init__(self, engine_id: int, system_status: str, active_module: str):
        self.engine_id = engine_id
        self.system_status = system_status
        self.active_module = active_module
        self.current_users = {}

    def initialize_system(self):
        pass

    def control_workflow(self):
        pass

    def manage_data_flow(self):
        pass

    def optimize_process(self):
        pass

    """
    USER MANAGEMENT
    """

    def add_user(self, session_id, user_id, username, role):
        user_instance = User(user_id=user_id, username=username, role=role)
        user_instance.login(session_id)
        self.current_users[session_id] = user_instance
        # print(f"User {user_instance.username} added to active users.")

    def get_user(self, session_id):
        return self.current_users.get(session_id)

    def remove_user(self, session_id):
        if session_id in self.current_users:
            del self.current_users[session_id]
            print(f"User with session {session_id} logged out.")