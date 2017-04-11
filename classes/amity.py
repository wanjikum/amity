"""
A class Amity that contains all the functionality of the app.
"""
import itertools
from random import choice
from classes.room import LivingSpace, Office
from classes.person import Staff, Fellow


class Amity(object):
    """Contains all functionalities of class Amity """
    offices = []
    livingspaces = []
    fellows = []
    staffs = []
    waiting_list = {
        "office": [],
        "livingspace": []
    }

    def create_room(self, room_type, room_names):
        """A method that is used to create a room"""
        room_type = room_type.lower()
        message = ""
        for room_name in room_names:
            if room_name not in [room.room_name
               for room in itertools.chain(self.offices, self.livingspaces)]:
                if room_type == "office":
                    new_office = Office(room_name)
                    self.offices.append(new_office)
                    message += "{} added successfully!\n".format(room_name)
                elif room_type in ["living_space", "livingspace"]:
                    new_living_space = LivingSpace(room_name)
                    self.livingspaces.append(new_living_space)
                    message += "{} added successfully!\n".format(room_name)
                else:
                    message += "Invalid room type. " + \
                      "A room can either be of type office or living_space!\n"
            else:
                message += "Room {} already exists!\n".format(room_name)
        return message

    def add_person(self, person_name, person_type, wants_accommodation):
        """A method that is used to add a person into the system"""
        is_digit = any(char.isdigit() for char in person_name)
        if is_digit:
            return "Invalid name. Use letters only"
        else:
            # person_name = person_name.title()
            person_type = person_type.lower()
            if person_type not in ["fellow", "f", "staff", "s"]:
                return "Invalid role. You can either be a fellow/staff."
            else:
                wants_accommodation = (wants_accommodation.lower()
                                       if wants_accommodation is not None
                                       else "no")
                if wants_accommodation not in ["yes", "y", "n", "no"]:
                    return "Invalid accomodate option. " + \
                     "It can either be yes or no."
                else:
                    return self.save_person(person_name, person_type,
                                            wants_accommodation)

    def save_person(self, person_name, person_type, wants_accommodation):
        person_name = person_name.title()
        if person_type in ["staff", "s"]:
            if wants_accommodation in ["yes", "y"]:
                return "Staff cannot be accomodated!"
            else:
                new_person = Staff(person_name)
                self.staffs.append(new_person)
                print("{} added successfully!".format(person_name))
                # print("Your ID: {}".format(new_person.person_id))
                return self.allocate_office(new_person)

        else:
            new_person = Fellow(person_name, wants_accommodation)
            self.fellows.append(new_person)
            print("{} added successfully!".format(person_name))
            # print("Your ID: {}".format(new_person.person_id))
            if wants_accommodation in ["no", "n"]:
                return self.allocate_office(new_person)
            else:
                print(self.allocate_office(new_person))
                return self.allocate_living_space(new_person)

    def allocate_office(self, new_person):
        """A method that allocates an office"""
        office_with_space = []
        for office in self.offices:
            if len(office.occupants) < office.room_capacity:
                office_with_space.append(office)
        if office_with_space:
            random_office = choice(office_with_space)
            random_office.occupants.append(new_person.person_name)
            new_person.office = random_office
            return "Allocated office: {}\n".format(random_office.room_name)
        else:
            self.waiting_list["office"].append(new_person)
            return "No available offices. Added to the office waiting list\n"

    def allocate_living_space(self, new_person):
        """A method that allocates a living space"""
        livingspace_with_space = []
        for livingspace in self.livingspaces:
            if len(livingspace.occupants) < livingspace.room_capacity:
                livingspace_with_space.append(livingspace)
        if livingspace_with_space:
            random_livingspace = choice(livingspace_with_space)
            random_livingspace.occupants.append(new_person.person_name)
            new_person.livingspace = random_livingspace
            return "Allocated livingspace: {} \n". \
                format(random_livingspace.room_name)
        else:
            self.waiting_list["livingspace"].append(new_person)
            return "No available livingspaces. " + \
                "Added to the livingspaces waiting list\n"

    def print_room(self, room_name):
        """A method that prints room occupants in a room"""
        found = False
        for room in (self.offices + self.livingspaces):
            if room_name == room.room_name:
                found = True
        if found:
            if len(room.occupants) == 0:
                return "The room is empty!\n"
            else:
                for occupant in room.occupants:
                    print(occupant)
                return "Room occupants printed successfully!\n"
        else:
            return "The room does not exist!\n"

    def reallocate_person(self, person_id, room_name):
        pass

    def loads_people(self, file_name):
        """A method that adds people from a text file"""
        print(file_name)

    def print_allocated(self, file_name=None):
        """A method that prints allocated people in rooms"""
        print(file_name)

    def print_unallocated(self, file_name=None):
        """A method that prints unallocated people"""
        print(file_name)

    def save_state(self, database_name):
        """A method that saves changes to the database"""
        print(database_name)

    def load_state(self, database_name):
        """A method that loads state of the  database"""
        print(database_name)
