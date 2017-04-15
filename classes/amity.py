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
    all_rooms = []
    fellows = []
    staffs = []
    all_people = []
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
               for room in self.all_rooms]:
                if room_type == "office":
                    new_office = Office(room_name)
                    self.offices.append(new_office)
                    self.all_rooms.append(new_office)
                    message += "{} added successfully!\n".format(room_name)
                elif room_type in ["living_space", "livingspace"]:
                    new_living_space = LivingSpace(room_name)
                    self.livingspaces.append(new_living_space)
                    self.all_rooms.append(new_living_space)
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
            person_name = person_name.title()
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
                new_person.person_id = "SOO" + str(len(self.staffs)+1)
                self.staffs.append(new_person)
                self.all_people.append(new_person)
                print("{} added successfully! Your ID: {}"
                      .format(person_name, new_person.person_id))
                return self.allocate_office(new_person)

        else:
            new_person = Fellow(person_name, wants_accommodation)
            new_person.person_id = "FOO" + str(len(self.fellows)+1)
            self.fellows.append(new_person)
            self.all_people.append(new_person)
            print("{} added successfully! Your ID: {}"
                  .format(person_name, new_person.person_id))
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
            print(random_office.occupants)
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
            print(random_livingspace.occupants)
            new_person.living_space = random_livingspace
            return "Allocated livingspace: {} \n". \
                format(random_livingspace.room_name)
        else:
            self.waiting_list["livingspace"].append(new_person)
            return "No available livingspaces. " + \
                "Added to the livingspaces waiting list\n"

    def print_room(self, room_name):
        """A method that prints room occupants in a room"""

        found = False
        for room in self.all_rooms:
            if room_name == room.room_name:
                found = True
        if found:
            if room.room_type == "office":
                for office in self.offices:
                    if office.room_name == room_name:
                        if len(office.occupants) == 0:
                            return "The room is empty!\n"
                        else:
                            # print(office.occupants)
                            for occupant in office.occupants:
                                print(occupant)
                            return "Room occupants printed successfully!\n"
            else:
                for lspace in self.livingspaces:
                    if lspace.room_name == room_name:
                        if len(lspace.occupants) == 0:
                            return "The room is empty!\n"
                        else:
                            for occupant in lspace.occupants:
                                print(occupant)
                            return "Room occupants printed successfully!\n"
        else:
            return "The room does not exist!\n"

    def reallocate_person(self, person_id, room_name):
        """A method that reallocates a person from one room to another"""
        room_name = room_name.lower()
        person_id = person_id.upper()
        if person_id in [person.person_id for person in self.all_people]:
            if room_name in [room.room_name for room in self.all_rooms]:
                if person_id[:3] == "FOO":
                    if room_name in [room.room_name for room in self.offices]:
                        return self.reallocate_fellow_office(person_id, room_name)
                    else:
                        return self.reallocate_fellow_livingspace(person_id, room_name)
                else:
                    if room_name in [room.room_name for room in self.offices]:
                        return self.reallocate_staff(person_id, room_name)
                    else:
                        return "Staff cannot be accomodated!"

            else:
                return "The room does not exist!"
        else:
            return "The person identifier(id) used does not exist!"

    def reallocate_fellow_office(self, person_id, room_name):
        """A method that reallocates fellows"""
        fellow_object = [fellow for fellow in self.fellows
                         if fellow.person_id == person_id]
        fellow_name = fellow_object[0].person_name

        if fellow_object[0].office.room_name == room_name:
            return "A person cannot be reallocated to the same room"
        else:
            previous_office = fellow_object[0].office.room_name
            previous_office_object = [office for office in self.offices
                                      if office.room_name == previous_office]
            previous_office_object[0].occupants.remove(fellow_name)
            office_object = [office for office in self.offices
                             if office.room_name == room_name]
            if len(office_object[0].occupants) < 6:
                office_object[0].occupants.append(fellow_name)
                fellow_object[0].office.room_name == room_name
                return "{} has been reallocated from {} to {}".format(
                 fellow_name, previous_office, room_name)
            else:
                return "Room capacity full!"

    def reallocate_fellow_livingspace(self, person_id, room_name):
        """A method that reallocates fellows"""
        fellow_object = [fellow for fellow in self.fellows
                         if fellow.person_id == person_id]
        fellow_name = fellow_object[0].person_name

        if fellow_object[0].living_space.room_name == room_name:
            return "A person cannot be reallocated to the same room"
        else:
            previous_living_space = fellow_object[0].living_space.room_name
            previous_living_space_object = [lspace for lspace in
            self.livingspaces if lspace.room_name == previous_living_space]
            previous_living_space_object[0].occupants.remove(fellow_name)
            living_space_object = [lspace for lspace in self.livingspaces
                                   if lspace.room_name == room_name]
            if len(living_space_object[0].occupants) < 4:
                living_space_object[0].occupants.append(fellow_name)
                fellow_object[0].living_space.room_name == room_name
                return "{} has been reallocated from {} to {}".format(
                  fellow_name, previous_living_space, room_name)
            else:
                return "Room capacity full!"


    def reallocate_staff(self, person_id, room_name):
        """A method that reallocates staff from one office to another"""
        staff_object = [staff for staff in self.staffs
                         if staff.person_id == person_id]
        staff_name = staff_object[0].person_name

        if staff_object[0].office.room_name == room_name:
            return "A person cannot be reallocated to the same room"

        else:
            previous_office = staff_object[0].office.room_name
            previous_office_object = [office for office in self.offices
                                      if office.room_name == previous_office]
            previous_office_object[0].occupants.remove(staff_name)
            office_object = [office for office in self.offices
                             if office.room_name == room_name]
            if len(office_object[0].occupants) < 6:
                office_object[0].occupants.append(staff_name)
                staff_object[0].office.room_name == room_name
                return "{} has been reallocated from {} to {}".format(
                 staff_name, previous_office, room_name)
            else:
                return "Room capacity full!"

    def print_allocated(self, file_name=None):
        """A method that prints allocated people in rooms"""
        office_available = [office for office in self.offices if len(office.occupants) >= 0]
        lspace_available = [lspace for lspace in self.livingspaces if len(lspace.occupants) >= 0]
        if office_available:
            print("*"*50)
            print("OFFICE ALLOCATIONS")
            print("*"*50)
            for office in office_available:
                print("\n{}".format(office.room_name.upper()))
                print("-"*50)
                if len(office.occupants) == 0:
                    print("NONE\n")
                else:
                    for occupant in office.occupants:
                        print("{},".format(occupant), end=' ')
                print("\n")
        if lspace_available:
            print("*"*50)
            print("LIVINGSPACE ALLOCATIONS")
            print("*"*50)
            for lspace in lspace_available:
                print("\n{}".format(lspace.room_name.upper()))
                print("-"*50)
                if len(lspace.occupants) == 0:
                    print("NONE\n")
                else:
                    for occupant in lspace.occupants:
                        print("{},".format(occupant), end=' ')
                    print("\n")
            return "\nData printed successfully \n"
        else:
            return "No rooms available"
        if file_name == None:
            return "I can do anything"
        else:
            return file_name

    def loads_people(self, file_name):
        """A method that adds people from a text file"""
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
