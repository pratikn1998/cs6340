class CS6340:

    def __init__(self, first_name,last_name, grade):

        self._first_name = first_name

        self._last_name = last_name

        self._grade = grade

    

    def print_name(self):
        
        print(self._first_name + self._last_name)
    def get_grade(self):

        return self._grade
    def get_last_name(self):

        return self._last_name
    def get_first_name(self):

        return self._first_name
