"""
A class Amity that contains all the functionality of the app.
"""
import os
from termcolor import cprint, colored
from random import choice
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from classes.room import LivingSpace, Office
from classes.person import Staff, Fellow
from database.models import RoomModel, PersonModel, Base


class Amity(object):
    """Contains all functionalities of class Amity """
    changes = False
    loaded_database = ""
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
            room_name = room_name.lower()
            if room_name not in [room.room_name
               for room in (self.offices + self.livingspaces)]:
                if room_type == "office":
                    new_office = Office(room_name)
                    self.offices.append(new_office)
                    self.changes = True
                    message += "{} added successfully!\n".format(
                     room_name.title())
                elif room_type in ["living_space", "livingspace"]:
                    new_living_space = LivingSpace(room_name)
                    self.livingspaces.append(new_living_space)
                    self.changes = True
                    message += "{} added successfully!\n".format(
                     room_name.title())
                else:
                    message += "Invalid room type. " + \
                      "A room can either be of type office or living_space!\n"
            else:
                message += "Room {} already exists!\n".format(
                 room_name.title())
        return message

    def add_person(self, person_name, person_type, wants_accommodation):
        """A method that is used to add a person into the system"""
        is_digit = any(char.isdigit() for char in person_name)
        if is_digit:
            return colored("Invalid name. Use letters only", 'red')
        else:
            person_name = person_name.title()
            person_type = person_type.lower()
            if person_type not in ["fellow", "f", "staff", "s"]:
                return colored("Invalid role. You can either be a " +
                               "fellow/staff.", 'red')
            else:
                wants_accommodation = (wants_accommodation.lower()
                                       if wants_accommodation is not None
                                       else "no")
                if wants_accommodation not in ["yes", "y", "n", "no"]:
                    return colored("Invalid accomodate option. " +
                                   "It can either be yes or no.", 'red')
                else:
                    return self.save_person(person_name, person_type,
                                            wants_accommodation)

    def save_person(self, person_name, person_type, wants_accommodation):
        person_name = person_name.title()
        if person_type in ["staff", "s"]:
            if wants_accommodation in ["yes", "y"]:
                return colored("Staff cannot be accomodated!\n", 'yellow')
            else:
                new_person = Staff(person_name)
                new_person.person_id = "SOO" + str(len(self.staffs)+1)
                self.staffs.append(new_person)
                self.changes = True
                cprint("{} added successfully! Your ID: {}"
                       .format(person_name, new_person.person_id), 'green')
                return self.allocate_office(new_person)

        else:
            new_person = Fellow(person_name, wants_accommodation)
            new_person.person_id = "FOO" + str(len(self.fellows)+1)
            self.fellows.append(new_person)
            self.changes = True
            cprint("{} added successfully! Your ID: {}"
                   .format(person_name, new_person.person_id), 'green')
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
            return colored(" Allocated office: {}\n ".format(
              random_office.room_name), 'green')
        else:
            self.waiting_list["office"].append(new_person)
            self.waiting_list["office"] = list(
             set(self.waiting_list["office"]))
            return colored("No available offices. Added to " +
                           "the office waiting list\n", 'yellow')

    def allocate_living_space(self, new_person):
        """A method that allocates a living space"""
        livingspace_with_space = []
        for livingspace in self.livingspaces:
            if len(livingspace.occupants) < livingspace.room_capacity:
                livingspace_with_space.append(livingspace)
        if livingspace_with_space:
            random_livingspace = choice(livingspace_with_space)
            random_livingspace.occupants.append(new_person.person_name)
            new_person.living_space = random_livingspace
            return colored("Allocated livingspace: {} \n".
                           format(random_livingspace.room_name), "green")
        else:
            self.waiting_list["livingspace"].append(new_person)
            self.waiting_list["livingspace"] = list(
             set(self.waiting_list["livingspace"]))
            return colored("No available livingspaces. Added to the "
                           "livingspaces waiting list\n", 'yellow')

    def print_room(self, room_name):
        """A method that prints room occupants in a room"""
        found = False
        room_obj = ""
        for room in (self.offices + self.livingspaces):
            if room_name == room.room_name:
                found = True
                room_obj = room
        if found:
            if len(room_obj.occupants) == 0:
                return colored("The room is empty!\n", 'yellow')
            else:
                for occupant in room_obj.occupants:
                    print(occupant)
                return colored("Room occupants printed successfully!\n",
                               'green')
        else:
            return colored("The room does not exist!\n", "yellow")

    def reallocate_person(self, person_id, room_name):
        """A method that reallocates a person from one room to another"""
        room_name = room_name.lower()
        person_id = person_id.upper()
        if person_id in [person.person_id for person in
           (self.fellows + self.staffs)]:
            if room_name in [room.room_name for room in
               (self.offices + self.livingspaces)]:
                if person_id[:3] == "FOO":
                    if room_name in [room.room_name for room in self.offices]:
                        return self.reallocate_fellow_office(person_id,
                                                             room_name)
                    else:
                        return self.reallocate_fellow_livingspace(person_id,
                                                                  room_name)
                else:
                    if room_name in [room.room_name for room in self.offices]:
                        return self.reallocate_staff(person_id, room_name)
                    else:
                        return colored("Staff cannot be accomodated!",
                                       'yellow')

            else:
                return colored("The room does not exist!", 'yellow')
        else:
            return colored("The person identifier(id) used does not exist!",
                           'yellow')

    def reallocate_fellow_office(self, person_id, room_name):
        """A method that reallocates fellows"""
        fellow_object = [fellow for fellow in self.fellows
                         if fellow.person_id == person_id]
        fellow_name = fellow_object[0].person_name
        if fellow_object[0].office is None:
            return colored("{} has not been allocated an office yet\n".format(
             fellow_name), 'yellow')
        elif fellow_object[0].office.room_name == room_name:
            return colored("A person cannot be reallocated to the same room",
                           'yellow')
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
                self.changes = True
                return colored("{} has been reallocated from {} to {}".format(
                 fellow_name, previous_office, room_name), 'green')
            else:
                return colored("Room capacity full!", 'yellow')

    def reallocate_fellow_livingspace(self, person_id, room_name):
        """A method that reallocates fellows"""
        fellow_object = [fellow for fellow in self.fellows
                         if fellow.person_id == person_id]
        fellow_name = fellow_object[0].person_name
        if fellow_object[0].living_space is None:
            return colored("{} has not been allocated a" +
                           "livingspace yet\n".format(fellow_name), 'yellow')
        elif fellow_object[0].living_space.room_name == room_name:
            return colored("A person cannot be reallocated to the " +
                           "same room", 'yellow')
        else:
            previous_living_space = fellow_object[0].living_space.room_name
            previous_living_space_object = [lspace for lspace in
                                            self.livingspaces if
                                            lspace.room_name ==
                                            previous_living_space]
            previous_living_space_object[0].occupants.remove(fellow_name)
            living_space_object = [lspace for lspace in self.livingspaces
                                   if lspace.room_name == room_name]
            if len(living_space_object[0].occupants) < 4:
                living_space_object[0].occupants.append(fellow_name)
                fellow_object[0].living_space.room_name == room_name
                self.changes = True
                return colored("{} has been reallocated from {} to {}".format(
                  fellow_name, previous_living_space, room_name), 'green')
            else:
                return colored("Room capacity full!", 'yellow')

    def reallocate_staff(self, person_id, room_name):
        """A method that reallocates staff from one office to another"""
        staff_object = [staff for staff in self.staffs
                        if staff.person_id == person_id]
        staff_name = staff_object[0].person_name
        if staff_object[0].office is None:
            return colored("{} has not been allocated an office yet\n".format(
               staff_name), 'yellow')
        elif staff_object[0].office.room_name == room_name:
            return colored("A person cannot be reallocated to the same room",
                           'yellow')
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
                self.changes = True
                return colored("{} has been reallocated from {} to {}".format(
                 staff_name, previous_office, room_name), 'green')
            else:
                return colored("Room capacity full!", 'yellow')

    def print_allocated(self, file_name=None):
        """A method that prints allocated people in rooms"""
        output = ""
        office_available = [office for office in self.offices
                            if len(office.occupants) >= 0]
        lspace_available = [lspace for lspace in self.livingspaces
                            if len(lspace.occupants) >= 0]
        if len(office_available) == 0 and len(lspace_available) == 0:
            return colored("No rooms allocated\n", 'yellow')
        if len(office_available) > 0:
            output += ("*"*50 + "\n")
            output += ("OFFICE ALLOCATIONS" + "\n")
            output += ("*"*50 + "\n")
            for office in office_available:
                output += ("\n" + "{}".format(office.room_name.upper()))
                output += ("\n" + "-"*50 + "\n")
                if len(office.occupants) == 0:
                    output += ("\n" + "NONE" + "\n")
                else:
                    for occupant in office.occupants:
                        output += ("{}, ".format(occupant))
                output += ("\n")
        else:
            output += colored("No offices available", 'yellow')
        if len(lspace_available) > 0:
            output += ("\n")
            output += ("*"*50 + "\n")
            output += ("LIVINGSPACE ALLOCATIONS" + "\n")
            output += ("*"*50 + "\n")
            for lspace in lspace_available:
                output += ("\n" + "{}".format(lspace.room_name.upper()))
                output += ("\n" + "-"*50 + "\n")
                if len(lspace.occupants) == 0:
                    output += ("\n" + "NONE" + "\n")
                else:
                    for occupant in lspace.occupants:
                        output += ("{}, ".format(occupant))
                    output += ("\n")
        else:
            output += colored("No livingspaces available", 'yellow')
        if file_name is None:
            print(output)
            return colored("\nData printed successfully\n", 'green')
        else:
            save_to = open(file_name + ".txt", "w")
            save_to.write(output)
            save_to.close()
            return colored("Data saved in {} successfully".format(file_name),
                           'green')

    def print_unallocated(self, file_name=None):
        """A method that prints unallocated people"""
        output = ""
        unallocated_office = [person for person in self.waiting_list["office"]]
        unallocated_lspace = [person
                              for person in self.waiting_list["livingspace"]]
        if len(unallocated_office) == 0 and len(unallocated_lspace) == 0:
            return colored("No one in the waiting list", 'yellow')
        if len(unallocated_office) > 0:
            output += ("*"*50 + "\n")
            output += ("OFFICE UNALLOCATIONS" + "\n")
            output += ("*"*50 + "\n")
            output += (" ID   " + "  Person name" + "\n")
            for name in unallocated_office:
                output += ("{} -> {} \n".format(name.person_id,
                                                name.person_name))
            output += ("\n")
        else:
            output += colored("\nNo one in the office waiting list", 'yellow')
        if len(unallocated_lspace) > 0:
            output += ("\n" + "*"*50 + "\n")
            output += ("LIVINGSPACE UNALLOCATIONS" + "\n")
            output += ("*"*50 + "\n")
            output += (" ID   " + "  Person name" + "\n")
            for name in unallocated_lspace:
                output += ("{} -> {} \n".format(name.person_id,
                           name.person_name))
        else:
            output += colored("\nNo one in the living_space waiting list",
                              'yellow')
        if file_name is None:
            print(output)
            return colored("Data printed successfully\n", 'green')
        else:
            save_to = open(file_name + ".txt", "w")
            save_to.write(output)
            save_to.close()
            return colored("Data saved in {} successfully".format(file_name),
                           'green')

    def allocate_person_office(self, person_id):
        """A method that allocates a person in the waiting list to an office"""
        person_id = person_id.upper()
        found = False
        person_obj = None
        for person in self.waiting_list["office"]:
            if person.person_id == person_id:
                found = True
                person_obj = person
                self.allocate_office(person)
                break
        if not found:
            return colored("The person is not in the office waiting list",
                           'yellow')
        if person_obj.office is None:
            return colored("No available offices", 'yellow')
        else:
            self.waiting_list["office"].remove(person_obj)
            return colored("{} has been allocated to office {}".format(
             person_obj.person_name, person_obj.office.room_name), 'green')

    def allocate_person_livingspace(self, person_id):
        """A method that allocates person in waiting list a livingspace"""
        person_id = person_id.upper()
        found = False
        person_obj = None
        for person in self.waiting_list["livingspace"]:
            if person.person_id == person_id:
                found = True
                person_obj = person
                self.allocate_living_space(person)
                break
        if not found:
            return colored("The person is not in the livingspace waiting list",
                           'yellow')
        if person_obj.living_space is None:
            return colored("No available livingspaces", "yellow")
        else:
            self.waiting_list["livingspace"].remove(person_obj)
            return colored("{} has been allocated to livingspace {}".format(
             person_obj.person_name, person_obj.living_space.room_name),
             'green')

    def loads_people(self, file_name):
        """A method that adds people from a text file"""
        try:
            read_file = open(file_name + '.txt', 'r')
            people = read_file.readlines()
            if len(people) == 0:
                return colored('Empty file. No one has been added.', 'yellow')
            for person in people:
                splitwords = person.split()
                if len(splitwords) in range(3, 5):
                    if len(splitwords) == 3:
                        wants_accommodation = 'n'
                    else:
                        wants_accommodation = splitwords[3]
                    person_name = splitwords[0] + ' ' + splitwords[1]
                    person_type = splitwords[2]
                    print(self.add_person(person_name, person_type,
                          wants_accommodation))
                else:
                    print(colored('Invalid input!\n', 'red'))
            return colored('People added successfully', 'green')
        except FileNotFoundError:
            return colored('The file does not exist.', 'yellow')

    def save_state(self, database_name):
        """A method that saves changes to the database"""
        try:
            os.remove("database/" + database_name + ".db")
        except FileNotFoundError:
            pass
        engine = create_engine('sqlite:///database/' + database_name
                               + '.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        all_rooms = self.offices + self.livingspaces
        all_people = self.fellows + self.staffs
        for room in all_rooms:
            new_room = RoomModel(room_name=room.room_name,
                                 room_type=room.room_type,
                                 room_capacity=room.room_capacity,
                                 occupants=','.join(room.occupants))
            session.add(new_room)
        session.commit()
        for person in all_people:
            new_person = PersonModel(
                person_id=person.person_id,
                person_name=person.person_name,
                person_type=person.person_type,
                office_allocated=(None if person.office is None
                                  else person.office.room_name),
                livingspace_allocated=(None if person.person_type == 'staff'
                                       else (None if person.living_space is
                                             None else
                                             person.living_space.room_name)),
                wants_accomodation=('no' if person.person_type == 'staff'
                                    else person.accommodate))
            session.add(new_person)
        session.commit()
        session.close()
        self.changes = False
        return colored('The state has been saved successfully!', 'green')

    def load_state(self, database_name):
        """A method that loads state of the  database"""
        if self.changes:
            choice = input("Do you want to save the changes?").upper()
            if choice in ["YES", "Y"]:
                self.save_state(self.loaded_database)
            elif choice not in ["NO", "N"]:
                return colored("Invalid input", 'red')

        if not os.path.isfile('./database/{}.db'.format(database_name)):
            return colored('The database does not exist!', 'yellow')
        engine = \
            create_engine('sqlite:///database/{}.db'.format(database_name))
        Session = sessionmaker(bind=engine)
        session = Session()
        rooms = session.query(RoomModel).all()
        people = session.query(PersonModel).all()
        self.offices = []
        self.livingspaces = []
        for room in rooms:
            if room.room_type == 'office':
                office = Office(room.room_name)
                office.occupants = (room.occupants.split(',')
                                    if room.occupants else [])
                self.offices.append(office)
            else:
                living_space = LivingSpace(room.room_name)
                living_space.occupants = (room.occupants.split(',')
                                          if room.occupants else [])
                self.livingspaces.append(living_space)
        self.fellows = []
        self.staffs = []
        self.waiting_list = {'office': [], 'livingspace': []}
        for person in people:
            if person.person_type == 'staff':
                staff = Staff(person.person_name)
                staff.person_id = person.person_id
                staff.person_name = person.person_name
                office = [office for office in self.offices
                          if office.room_name == person.office_allocated]
                staff.office = (office[0] if office else None)
                self.staffs.append(staff)
                if staff.office is None:
                    self.waiting_list['office'].append(staff)
            else:
                fellow = Fellow(person.person_name)
                fellow.person_id = person.person_id
                fellow.person_name = person.person_name
                office = [office for office in self.offices
                          if office.room_name == person.office_allocated]
                fellow.office = (office[0] if office else None)
                living_space = [living_space for living_space in
                                self.livingspaces if living_space
                                .room_name == person.livingspace_allocated]
                fellow.living_space = (living_space[0]
                                       if living_space else None)
                fellow.accommodate = person.wants_accomodation
                self.fellows.append(fellow)
                if fellow.office is None:
                    self.waiting_list['office'].append(fellow)
                if fellow.living_space is None and \
                   fellow.accommodate in ['y', 'yes']:
                    self.waiting_list['livingspace'].append(fellow)
        self.loaded_database = database_name
        return colored('The database has loaded successfully!', 'green')
