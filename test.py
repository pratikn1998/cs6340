class CS6340:
    def __init__(self, first_name,last_name, grade):
        self.first_name = first_name
        self.last_name = last_name
        self.grade = grade
    
    def print_name(self):
        print(self.first_name + self.last_name)