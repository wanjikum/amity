import unittest
import os
from io import StringIO
import sys

from classes.room import Room, Office, LivingSpace
from classes.person import Person, Fellow, Staff
from classes.amity import Amity


class CreateRoomTestCases(unittest.TestCase):
    """A class CreateRoom that has a collection of create_room testcases"""
    def setUp(self):
        """Keeps our code dry"""
        self.amity = Amity()
        self.bootcamp = self.amity.create_room("office", ["Bootcamp"])

    def tearDown(self):
        del self.amity
        Amity.offices = []
        Amity.livingspaces = []

    def test_create_room_type_office_successfully(self):
        """Test create a room_type office successfully"""
        response = self.amity.create_room("office", ["asmara"])
        self.assertEqual(response, "asmara added successfully!\n")

    def test_create_multiple_rooms_of_type_livingspace_successfully(self):
        """Test create multiple rooms of type office successfully"""
        livingspace_intial_count = len(self.amity.livingspaces)
        likoni_tsavo = self.amity.create_room("livingspace",
                                              ["likoni", "tsavo"])
        self.assertEqual(len(self.amity.livingspaces),
                         livingspace_intial_count+2)

    def test_create_duplicate_room(self):
        """Test an existing room is not recreated"""
        response = self.amity.create_room("office", ["Bootcamp"])
        self.assertEqual(response, "Room Bootcamp already exists!\n")

    def test_create_invalid_room_type(self):
        """Test create invalid room type """
        response = self.amity.create_room("kitchen", ["hog_centre"])
        self.assertEqual(response, "Invalid room type. A room can either be of"
                         + " type office or living_space!\n")


class AddPersonTestCases(unittest.TestCase):
    """A class CreateRoom that has a collection of create_room testcases"""
    def setUp(self):
        """Keeps our code dry"""
        self.amity = Amity()

    def tearDown(self):
        del self.amity
        Amity.staffs = []
        Amity.fellows = []

    def test_add_person_staff_successfully(self):
        """Test add staff successfully"""
        self.amity.add_person("felistas", "staff", "no")
        response = sys.stdout.getvalue().strip()
        self.assertIn(response, "Felistas added successfully! Your ID: SOO1")

    def test_add_person_staff_who_requires_accommodation(self):
        """Test reject accommodation for staff"""
        response = self.amity.add_person("felistas", "staff", "yes")
        self.assertEqual(response, "Staff cannot be accomodated!")

    def test_add_person_who_inputs_a_wrong_accomodation_value(self):
        """Test reject accommodation if option is neither yes/no"""
        response = self.amity.add_person("felistas", "staff", "who")
        self.assertEqual(response, "Invalid accomodate option. "
                         + "It can either be yes or no.")

    def test_reject_invalid_role(self):
        """Rejects adding a person whose person type is not fellow/staff"""
        response = self.amity.add_person("alex", "techie", "no")
        self.assertEqual(response,
                         "Invalid role. You can either be a fellow/staff.")

    def test_if_it_accepts_string_only_in_person_name(self):
        """Tests if it rejects names with numbers"""
        response = self.amity.add_person("ti67ji#", "staff", "no")
        self.assertEqual(response, "Invalid name. Use letters only")


class AllocateRoomPersonTestCases(unittest.TestCase):
    """A collection of create_room testcases"""
    def setUp(self):
        """Keeps our code dry"""
        self.amity = Amity()

    def tearDown(self):
        del self.amity

    def test_allocate_office_successfully(self):
        """Tests if a person is successfully allocated an office"""
        self.amity.create_room("office", ["accra"])
        response = self.amity.add_person("oliver", "staff", "no")
        self.assertEqual(response, "Allocated office: accra\n")

    def test_allocate_livingspace_successfully(self):
        """Tests if a person is successfully allocated to a livingspace"""
        self.amity.create_room("livingspace", ["left_wing"])
        response = self.amity.add_person("oliver", "fellow", "yes")
        self.assertEqual(response, "Allocated livingspace: left_wing \n")

    def test_allocate_livingspace_if_no_available_livingspaces(self):
        """Test reject livingspace allocation if no livingspace available"""
        response = self.amity.add_person("oliver", "fellow", "yes")
        self.assertEqual(response, "No available livingspaces. "
                         "Added to the livingspaces waiting list\n")

    def test_allocate_office_if_no_available_offices(self):
        """Test reject allocation if room is full"""
        response = self.amity.add_person("Alex", "staff", "no")
        self.assertEqual(response, "No available offices. "
                         "Added to the office waiting list\n")


class PrintRoomTestCases(unittest.TestCase):
    """A collection of print_room testscases"""
    def setUp(self):
        self.amity = Amity()
        self.amity.create_room("living_space", ["left_wing"])
        self.amity.add_person("Kenneth", "fellow", "yes")
        self.amity.add_person("Gideon", "fellow", "yes")
        self.amity.add_person("Kimokoti", "fellow", "yes")
        self.amity.add_person("Larry", "fellow", "yes")

    def tearDown(self):
        self.amity
        Amity.offices = []
        Amity.livingspaces = []

    def test_print_room_occupants_successfully(self):
        """Test if it prints the room occupants successfully"""
        response = self.amity.print_room("left_wing")
        self.assertEqual(response, "Room occupants printed successfully!\n")

    def test_print_room_reject_if_room_name_does_not_exist(self):
        """Test if rejects printing occupants in a unexisting room"""
        occupants = self.amity.print_room("kiki")
        self.assertEqual(occupants, "The room does not exist!\n")

    def test_print_room_if_empty(self):
        """Test response in print room empty if empty"""
        self.amity.create_room("living_space", ["right_wing"])
        response = self.amity.print_room("right_wing")
        self.assertEqual(response, "The room is empty!\n")


class RellocateRoomPersonTestCases(unittest.TestCase):
    """A collection of create_room testcases"""
    def setUp(self):
        """Keeps our code dry"""
        self.amity = Amity()

    def tearDown(self):
        del self.amity

    def test_reallocate_a_person_successfully(self):
        """Tests if a person is successfully reallocated"""
        self.amity.create_room("office", ["kisii"])
        charity_kisii = self.amity.reallocate_person(1, "kisii")
        self.assertEqual(charity_kisii,
                         "charity has been reallocated from kakamega to kisii")

    def test_reallocate_reject_a_person_with_invalid_identifier(self):
        """Tests if it does not reallocate a person with an invalid personid"""
        charity_kakamega = self.amity.reallocate_person(78, "kakamega")
        self.assertEqual(charity_kakamega,
                         "The person identifier(id) used does not exist!")

    def test_reallocate_reject_if_room_does_not_exist(self):
        """Tests if it rejects reallocation to a room which does not exist"""
        charity_likoni = self.amity.reallocate_person(1, "likoni")
        self.assertEqual(charity_likoni,
                         "The room does not exist!")

    def test_reallocate_reject_if_a_room_is_full(self):
        """Tests if rejects reallocate person to a room which is full"""
        self.amity.create_room("living_space", "marsabit")
        vanni = self.amity.add_person("vanni", "fellow", "yes")
        vanni_reallocate = self.amity.reallocate_person(6, "kiambu")
        self.assertEqual(vanni_reallocate,
                         "Room capacity full!")

    def test_reallocate_staff_from_office_to_living_space(self):
        """Tests rejects reallocation of staff from office to livingspace"""
        charity_kiambu = self.amity.reallocate_person(1, "kiambu")
        self.assertEqual(charity_kiambu,
                         "Staff cannot be accomodated!")

    def test_reallocate_rejects_reallocation_to_the_same_room(self):
        """Test rejects reallocation to the same room"""
        charity_kakamega = self.amity.reallocate_person(1, "kakamega")
        self.assertEqual(charity_kakamega,
                         "A person cannot be reallocated to the same room")


class LoadsPeopleTestCases(unittest.TestCase):
    """A collection of reallocate_room testcases"""
    def setUp(self):
        self.amity = Amity()

    def tearDown(self):
        self.amity

    def test_loads_people_from_a_txt_file_successfully(self):
        """Tests if it loads people from a txt file successfully"""
        # remember to add the exten .txt
        cohort_15 = self.amity.loads_people("cohort15")
        self.assertEqual(cohort_15, "People added successfully")

    def test_loads_an_empty_file(self):
        """Test if it loads people in an empty file and adds nothing"""
        empty_file = self.amity.loads_people("empty")
        self.assertEqual(empty_file, "Empty file. No one has been added.")

    def test_if_file_does_not_exist(self):
        """Tests if the file does not exist"""
        # Add the file path you said you wanted
        non_existing_file = self.amity.loads_people("non_existing")
        self.assertEqual(non_existing_file, "The file does not exist.")


class PrintAllocatedUnallocated(unittest.TestCase):
    """A collection of print allocated and unallocated testcases"""
    def setUp(self):
        self.amity = Amity()
        self.amity.create_room("living_space", "right_wing")
        self.amity.add_person("Kenneth", "fellow", "yes")
        self.amity.add_person("Gideon", "fellow", "yes")
        self.amity.add_person("Kimokoti", "fellow", "yes")
        self.amity.add_person("Larry", "fellow", "yes")
        self.amity.add_person("MaryAnne", "fellow", "yes")
        self.amity.add_person("Sarah", "fellow", "yes")

    def tearDown(self):
        self.amity

    def test_print_allocated_successfully(self):
        """Tests if it prints allocated people successfully"""
        allocated_people = self.amity.print_allocated()
        self.assertEqual(allocated_people, "Data printed successfully")

    def test_print_unallocated_successfully(self):
        """Tests if it prints unallocated people successfully"""
        unallocated_people = self.amity.print_unallocated()
        self.assertEqual(unallocated_people, "Data printed successfully")

    def test_print_allocated_successfully_to_text_file(self):
        """Tests if it prints allocated people to the specified file"""
        allocated_people = self.amity.print_allocated("allocated")
        # check if the file exists
        self.assertEqual(allocated_people,
                         "Data saved in allocated.txt successfully")

    def test_print_unallocated_successfully_to_text_file(self):
        """Tests if prints unallocated people to the specified file"""
        unallocated_people = self.amity.print_unallocated("unallocated")
        self.assertEqual(unallocated_people,
                         "Data saved in unallocated.txt successfully")



class SaveStateTestCases(unittest.TestCase):
    """A collection of loadstate testcases"""

    def setUp(self):
        self.amity = Amity()

    def tearDown(self):
        self.amity

    def test_save_state_successfully(self):
        """Test if it saves state successfully"""
        # look at this later and db extension
        save_state = self.amity.save_state("amity_database")
        self.assertEqual(save_state, "The state has been saved successfully!")

    def test_if_db_exists(self):
        """Tests if the db file exists"""
        self.amity.save_state("amity_database")
        file_path = os.path.abspath("amity_database.db")
        file_status = os.path.isfile(file_path)
        self.assertTrue(file_status)


class LoadStateTestCases(unittest.TestCase):
    """A collection of load state testcases"""

    def setUp(self):
        self.amity = Amity()

    def tearDown(self):
        self.amity

    def test_load_state_successfully(self):
        """Tests if load state successfully"""
        load_database = self.amity.load_state("amity_database")
        self.assertEqual(load_database,
                         "The database has loaded successfully!")

    def test_load_state_unsuccessfully(self):
        """Test if loads state unsuccessfully"""
        # This may be due to non existing db
        load_database = self.amity.load_state("dee")
        self.assertEqual(load_database,
                         "The database does not exist!")
