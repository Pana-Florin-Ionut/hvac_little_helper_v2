class Project:
    def __init__(self, client_name, project_name):
        self.client_name = client_name
        self.project_name = project_name

    def __repr__(self) -> str:
        return repr(f"Client: {self.client_name}, project: {self.project_name}")

    def generate_offer(self, offer):
        #here should have some functions to create the offer
        generated_offer = []
        for item in offer:
            print(item)
            generated_offer.append(item)
        return generated_offer

# project_1 = Project("Vasile", "Vasile's project")

# print(repr(project_1))
