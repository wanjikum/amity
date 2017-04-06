"""
A class Amity that contains all the functionality of the app.
"""


class Amity(object):
    """Contains all functionalities of class Amity """
    offices = []
    livingspace = []

    def create_room(self, room_type, room_names):
        """A method that is used to create a room"""
        room_type = room_type.lower()
        message = []
        if room_type == "office":
            for room_name in room_names:
                if room_name in self.offices:
                    message.append("Office {} already exists!".format(room_name))
                self.offices.append(room_name)
                message.append("Office {} has been successfully created!".format(room_name))

        elif room_type == "living_space" or room_type == "livingspace":
            for room_name in room_names:
                if room_name in self.offices:
                    message.append("Office {} already exists!".format(room_name))
                    break
                self.livingspace.append(room_name)
                message.append("LivingSpace {} has been successfully created!".format(room_name))

        else:
            message.append("Invalid room type. A room can either be of type office or living_space")
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
