"""
A class Amity that contains all the functionality of the app.
"""


class Amity(object):
    """Contains all functionalities of class Amity """
    offices = []

    def create_room(self, room_type, room_names):
        """A method that is used to create a room"""
        print(room_type)
        print(room_names)

    def add_person(self, person_name, person_type, accommodate):
        """A method that is used to add a person into the system"""
        # reject accommodate staff y/n for staff members
        print(person_name)
        print(person_type)
        print(accommodate)

    def reallocate_person(self, person_id, room_name):
        """A method that is used to reallocate a person"""
        print(person_id)
        print(room_name)

    def loads_people(self, file_name):
        """A method that adds people from a text file"""
        print(file_name)

    def print_allocated(self, file_name="none"):
        """A method that prints allocated people in rooms"""
        pass

    def print_unallocated(self, file_name="none"):
        """A method that prints unallocated people"""
        pass

    def print_room(self, room_name):
        """A method that prints room occupants in a room"""
        pass

    def save_state(self, database_name):
        """A method that saves changes to the database"""
        pass

    def load_state(self, database_name):
        """A method that loads state of the  database"""
        pass
