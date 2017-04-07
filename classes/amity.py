"""
A class Amity that contains all the functionality of the app.
"""
from classes.room import LivingSpace, Office

class Amity(object):
    """Contains all functionalities of class Amity """
    offices = []
    livingspaces = []
    rooms = []
    existing_rooms = []

    def create_room(self, room_type, room_names):
        """A method that is used to create a room"""
        room_type = room_type.lower()
        message = ""
        for room_name in room_names:
            if room_name not in self.existing_rooms:
                if room_type == "office":
                    new_office = Office(room_name)
                    self.offices.append(new_office)
                    self.rooms.append(new_office)
                    self.existing_rooms.append(room_name)
                    message += "{} added successfully!\n".format(room_name)
                elif room_type in ["living_space", "livingspace"]:
                    new_living_space = LivingSpace(room_name)
                    self.livingspaces.append(new_living_space)
                    self.rooms.append(new_living_space)
                    self.existing_rooms.append(room_name)
                    message += "{} added successfully!\n".format(room_name)
                else:
                    message += "Invalid room type. A room can either be of type office or living_space!\n"
            else:
                message += "Room {} already exists!\n".format(room_name)
        return message

    def add_person(self, person_name, person_type, accommodate):
        """A method that is used to add a person into the system"""
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

    def print_allocated(self, file_name=None):
        """A method that prints allocated people in rooms"""
        print(file_name)

    def print_unallocated(self, file_name=None):
        """A method that prints unallocated people"""
        print(file_name)

    def print_room(self, room_name):
        """A method that prints room occupants in a room"""
        print(room_name)

    def save_state(self, database_name):
        """A method that saves changes to the database"""
        print(database_name)

    def load_state(self, database_name):
        """A method that loads state of the  database"""
        print(database_name)
