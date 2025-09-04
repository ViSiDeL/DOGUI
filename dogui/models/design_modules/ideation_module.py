class Ideation:

    def __init__(self, ideation_id,user_id):
        self.id = ideation_id
        self.user_id = user_id
        self.project_name = input("Please enter a name for your project:")
        self.project_deadline = input("Please enter the deadline for your project (Format:00/00/0000):")


    def __str__(self):
        pass

    def get_projectDetails(self):
        return f"User ID:{self.user_id}\nIdeation_ID:{self.id}\nProject Name:{self.project_name}\nProject Deadline:{self.project_deadline}"


if __name__ == "__main__":
    project1 = Ideation(1,205)
    print(project1.get_projectDetails())
